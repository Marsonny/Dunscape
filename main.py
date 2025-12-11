from entities.player import Player
from logic.game_manager import generate_dungeon, load_game   
from logic.game_flow import game_loop, display_game_intro, separator
from data.game_data import (
    consumable_pool, weapon_pool, tool_pool, all_rooms,
    fixed_rooms, enemy_pool, boss_pool, PLAYER_CLASSES
)

def new_or_load(choice):

    choice = choice.strip().lower()
    
    if choice == "new":
        print("Let's start your adventure!")
        return True
    elif choice == "load":
        print("Checking if save file exist")
        return False
    
def main():
    player_name = input("What is your name?\n        >>>")
    
    while True:
        
        gameChoice = input(f"Welcome {player_name}.\nWould you like to start a new game or load a saved one? (new / load)\n        >>>")
        player = None
        all_dungeon_rooms = None
        still_has_enemies = 0

        if gameChoice.strip().lower() == "load":
            # Try to load the game. Our new function returns both player and rooms.
            player, all_dungeon_rooms = load_game()
            
            # print(all_dungeon_rooms)
            
        # If loading failed (returned None) or user chose "new", we start a new game.
        if player is None or all_dungeon_rooms is None:
            if gameChoice.strip().lower() != "load": # Avoid showing intro if load failed
                display_game_intro()

                # --- NEW: Character Creation Loop ---
                print("Choose your class:")
                for key, value in PLAYER_CLASSES.items():
                    print(f"  - {key.capitalize()}: {value['description']}")
                
                chosen_class_key = ""
                while chosen_class_key not in PLAYER_CLASSES:
                    chosen_class_key = input("Enter the name of the class you choose:\n>>> ").lower()
                    if chosen_class_key not in PLAYER_CLASSES:
                        print("Invalid class. Please choose from the list.")
                
                class_data = PLAYER_CLASSES[chosen_class_key]
                player = Player(player_name, class_data)
                # --- END OF NEW: Character Creation Loop ---

                input(f"\nYou have chosen the path of the {class_data['name']}. Press Enter to begin your escape...")
            
            else: # This handles the case where loading failed
                print("Could not load save file. Starting a new game is the only option.")
                # In a more advanced version, we would loop back to the main menu here.
                # For now, we'll just exit.
                return 

            start_room, still_has_enemies, all_dungeon_rooms = generate_dungeon(
                all_rooms, consumable_pool, weapon_pool, tool_pool, 
                fixed_rooms, enemy_pool, boss_pool
            )
            player.currentRoom = start_room
        
        # Now, we have a valid player and dungeon, either new or loaded. Start the game.
        game_loop(player, still_has_enemies, all_dungeon_rooms)

        # The rest of the logic for playing again can be handled outside the main loop
        # or you can wrap this in a while loop if you want a "play again" feature that
        # always starts a new game.
        while True:
            play_again = input(f"\nWould you like to play again, {player_name}? (y/n) ").strip().lower()
            
            if play_again == "y":
                print("Great choice! Let's start a new adventure.")
                separator()
                break 
            elif play_again == "n":
                print("Goodbye then, adventurer. Thank you for playing!")
                return
            else:
                print("Invalid choice. Please enter 'y' or 'n'.")

if __name__ == "__main__":
    main()
    