# In dungeon_game/tests/test_game_manager.py

import os
from logic.game_manager import save_game, load_game
from entities.player import Player
from entities.room import Room
from entities.items import Weapon

def test_save_and_load_restores_game_state():
    """
    An integration test for the entire save/load process.
    """
    # ARRANGE: Create a mini-dungeon and a player in a specific state.
    
    # 1. Create rooms and link them
    start_room = Room("Prison Cell", "normal")
    hallway = Room("Hallway", "normal")
    start_room.link_room(hallway, "north", False)
    hallway.link_room(start_room, "south", False)
    
    # 2. Create an item and place it
    sword = Weapon("Test Sword", "A sword for testing.", "weapon", 99, 50)
    hallway.items_in_room.append(sword)
    
    # 3. Create the list of all rooms in our mini-dungeon
    all_dungeon_rooms = [start_room, hallway]

    # 4. Create a player and modify their state
    default_class_data = { "base_maxHp": 100 }
    player = Player("TestSave", default_class_data)
    player.currentRoom = start_room
    player.currentHp = 75 # Player has taken some damage

    # 5. Define a test-specific save file name
    test_save_filename = "test_savegame.json"

    # ACT (Part 1): Save the game
    save_game(player, all_dungeon_rooms, test_save_filename)

    # ACT (Part 2): Load the game
    loaded_player, loaded_dungeon = load_game(test_save_filename)

    # ASSERT: Check if the loaded state matches the original state.
    
    # Player Assertions
    assert loaded_player is not None
    assert loaded_player.name == "TestSave"
    assert loaded_player.maxHp == 100
    assert loaded_player.currentHp == 75 # Was the damage saved?
    assert loaded_player.currentRoom.name == "Prison Cell" # Is the player in the right room?

    # Dungeon Assertions
    assert len(loaded_dungeon) == 2
    
    # Find the loaded hallway to inspect it
    loaded_hallway = None
    for room in loaded_dungeon:
        if room.name == "Hallway":
            loaded_hallway = room
            break
    
    assert loaded_hallway is not None
    assert len(loaded_hallway.items_in_room) == 1 # Is the sword still there?
    
    loaded_sword = loaded_hallway.items_in_room[0]
    assert isinstance(loaded_sword, Weapon)
    assert loaded_sword.name == "Test Sword"
    assert loaded_sword.weaponDamage == 99 # Was the sword's data restored?

    # CLEANUP: Remove the test save file so it doesn't clutter your directory.
    os.remove(test_save_filename)