import random
import json
from entities.room import Room
from entities.items import Item
from entities.player import Player
from entities.enemy import Enemy, Boss
from utils.exceptions import SaveDataError

def generate_dungeon(all_rooms, all_consumable, all_weapon, all_tool, special_rooms, all_enemy, bosses, grid_size=4):
    """
    Randomly generates a dungeon layout, links the rooms, and places items and enemies.
    Returns the starting room for the player.
    """
    # 1. Select a subset of rooms
    # Ensure we don't try to pick more rooms than are available
    num_rooms_to_generate = grid_size * grid_size
    if len(all_rooms) < num_rooms_to_generate:
        raise ValueError("Not enough rooms in the pool to fill the grid!")
    
    selected_rooms = random.sample(all_rooms, k=num_rooms_to_generate)
    
    # 2. Organize rooms into a grid (list of lists)
    grid = []
    for i in range(grid_size):
        row = selected_rooms[i * grid_size : (i + 1) * grid_size]
        grid.append(row)
        
    # --- Deliberately place special rooms ---
    # For simplicity, let's place the start and end rooms.
    # We can replace random rooms at specific grid coordinates.
    start_row, start_col = grid_size -1, grid_size - 1
    exit_row, exit_col = 0, 0
    
    starting_room = special_rooms[0]
    throne_room = special_rooms[1]
    exit = special_rooms[2]
    
    grid[start_row][start_col] = starting_room
    grid[exit_row][exit_col] = throne_room
    
    # 3. Link the rooms
    for row in range(grid_size):
        for col in range(grid_size):
            current_room = grid[row][col]
            
            # Link to the North
            if row > 0:
                north_room = grid[row - 1][col]
                if random.random() <= 0.15:
                    current_room.n_locked = True
                else:
                    current_room.n_locked = False
                current_room.link_room(north_room, "north", current_room.n_locked)
             
                
            # Link to the South
            if row < grid_size - 1:
                south_room = grid[row + 1][col]
                if random.random() <= 0.15:
                    current_room.s_locked = True
                else:
                    current_room.s_locked = False
                current_room.link_room(south_room, "south", current_room.s_locked)
             
                
            # Link to the West
            if col > 0:
                west_room = grid[row][col - 1]
                if random.random() <= 0.15:
                    current_room.w_locked = True
                else:
                    current_room.w_locked = False
                current_room.link_room(west_room, "west", current_room.w_locked)
                
            # Link to the East
            if col < grid_size - 1:
                east_room = grid[row][col + 1]
                if random.random() <= 0.15:
                    current_room.e_locked = True
                else:
                    current_room.e_locked = False
                current_room.link_room(east_room, "east", current_room.e_locked)
    
    throne_room.n_locked = True
    exit.s_locked = True    
    throne_room.link_room(exit, "north", throne_room.n_locked)
    exit.link_room(throne_room, "south", exit.s_locked)
 
    # if throne_room.enemy_in_room:
    #     throne_room.enemy_in_room.clear()

    # boss = random.choice(bosses)
    # throne_room.enemy_in_room.append(boss)
    # print(throne_room.enemy_in_room[0].name)
        
        
    available_weapons = all_weapon.copy()
    available_tools = all_tool.copy()
    available_consumables = all_consumable.copy()
    available_enemies = all_enemy.copy()
    
    random.shuffle(available_weapons)
    random.shuffle(available_tools)
    random.shuffle(available_consumables)
    random.shuffle(available_enemies)

    items_in_dungeon = []
    enemy_in_dungeon = []
    doors_in_dungeon = []
    for row in grid:
        for room in row:
            if room.type == "normal" and available_consumables:
                room.items_in_room.clear()
                room.enemy_in_room.clear()
                item = available_consumables.pop()
                items_in_dungeon.append(item.name)
                room.add_item(item)
                doors_in_dungeon += [room.name, (room.n_locked, room.s_locked, room.w_locked, room.e_locked)]
                if random.random() <= 0.5:
                    enemy = available_enemies.pop()
                    enemy_in_dungeon.append(enemy.name)
                    room.add_enemy(enemy)
            elif room.type == "armory" and available_weapons:
                room.items_in_room.clear()
                room.enemy_in_room.clear()
                item = available_weapons.pop()
                items_in_dungeon.append(item.name)
                room.add_item(item)
                doors_in_dungeon += [room.name, (room.n_locked, room.s_locked, room.w_locked, room.e_locked)]
                if random.random() <= 0.5:
                    enemy = available_enemies.pop()
                    enemy_in_dungeon.append(enemy.name)
                    room.add_enemy(enemy)
            elif room.type == "treasury" and available_tools:
                room.items_in_room.clear()
                room.enemy_in_room.clear()
                item = available_tools.pop()
                items_in_dungeon.append(item.name)
                room.add_item(item)
                doors_in_dungeon += [room.name, (room.n_locked, room.s_locked, room.w_locked, room.e_locked)]
                if random.random() <= 0.5:
                    enemy = available_enemies.pop()
                    enemy_in_dungeon.append(enemy.name)
                    room.add_enemy(enemy)
                    
    if throne_room.enemy_in_room:
        throne_room.enemy_in_room.clear()

    boss = random.choice(bosses)
    throne_room.enemy_in_room.append(boss)
    print(throne_room.enemy_in_room[0].name)
                    
    all_rooms_in_dungeon = [room for row in grid for room in row]
    all_rooms_in_dungeon.insert(0, exit)
    
    # starting_room.items_in_room[0] = all_tool[0]
    # print(items_in_dungeon)
    # print(enemy_in_dungeon)
    # print(doors_in_dungeon)
    return starting_room, len(enemy_in_dungeon), all_rooms_in_dungeon

def save_game(player, all_dungeon_rooms, filename="savegame.json"):
    """Saves the entire game state, including the player and the dungeon map."""
    try:
        # Create a list of dictionaries, one for each room
        dungeon_data = [room.to_dict() for room in all_dungeon_rooms]

        # Combine player and dungeon data into a single object
        game_state = {
            "player": player.to_dict(),
            "dungeon": dungeon_data
        }
        
        with open(filename, "w") as f:
            json.dump(game_state, f, indent=4)
        print(f"Game saved successfully to {filename}")

    except (IOError, TypeError) as e:
        print(f"Error saving game: {e}")
        
def load_game(filename="savegame.json"):
    """
    Loads the entire game state from a file.
    Returns the player object and the list of all dungeon rooms on success.
    Returns None, None on failure.
    """
    try:
        with open(filename, 'r') as f:
            game_state = json.load(f)

        # --- 1. RECONSTRUCT ROOMS (FIRST PASS: CREATE OBJECTS) ---
        dungeon_data = game_state['dungeon']
        all_rooms_map = {}
        for room_data in dungeon_data:
            room = Room(room_data['name'], room_data['type'])
            all_rooms_map[room.name] = room

        # --- 2. POPULATE AND LINK ROOMS (SECOND PASS) ---
        for room_data in dungeon_data:
            room = all_rooms_map[room_data['name']]
            
            # Re-create items and enemies
            room.items_in_room = [Item.from_dict(item_data) for item_data in room_data['items_in_room']]
            room.enemy_in_room = [Enemy.from_dict(enemy_data) for enemy_data in room_data['enemy_in_room']]
            
            # Link rooms using the map we created
            room.n_to = all_rooms_map.get(room_data['n_to'])
            room.s_to = all_rooms_map.get(room_data['s_to'])
            room.e_to = all_rooms_map.get(room_data['e_to'])
            room.w_to = all_rooms_map.get(room_data['w_to'])

            # Restore locked status
            room.n_locked = room_data['n_locked']
            room.s_locked = room_data['s_locked']
            room.e_locked = room_data['e_locked']
            room.w_locked = room_data['w_locked']

        # --- 3. RECONSTRUCT PLAYER ---
        player_data = game_state['player']
        player = Player(player_data['name'], player_data['maxHp']) # Start with name and maxHp
        player.currentHp = player_data['currentHp']
        
        # Find the player's current room object from our reconstructed map
        room_name = player_data['currentRoom']
        if room_name in all_rooms_map:
            player.currentRoom = all_rooms_map[room_name]
        else:
            raise SaveDataError(f"Saved room '{room_name}' not found in the loaded dungeon map.")

        # Re-create inventory
        player.weaponSlot = [Item.from_dict(item_data) for item_data in player_data['inventory']['weapon']]
        player.toolSlot = [Item.from_dict(item_data) for item_data in player_data['inventory']['tool']]
        player.consumableSlot = [Item.from_dict(item_data) for item_data in player_data['inventory']['consumable']]
        
        

        print("Game loaded successfully!")
        player.recalculate_stats() # VERY IMPORTANT!
        
        # Return the fully reconstructed player and the list of rooms
        return player, list(all_rooms_map.values())

    except FileNotFoundError:
        print("No save file found. Starting a new game.")
        return None, None
    except (json.JSONDecodeError, SaveDataError, KeyError) as e:
        print(f"Error loading game: {e}. The save file might be corrupted. Starting a new game.")
        return None, None