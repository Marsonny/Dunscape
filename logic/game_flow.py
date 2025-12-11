from logic.game_manager import save_game
from entities.enemy import Boss
from entities.player import Player



def separator():
    print("\n" + "-"*75 + "\n")

def display_game_intro():
    """
    Displays the introductory text and instructions for the player at the start of the game.
    """
    separator()
    print("You awaken on a cold, stone floor. The air is thick with the smell of dust and despair.")
    print("Your memories are a blur, but one thing is clear: you are trapped in a dark, shifting dungeon.")
    print("Your goal is simple: escape.")
    print("\nThere are two paths to freedom, but neither will be easy:")
    print()
    print("  1. The Path of the Warrior:")
    print("     Confront the master of this dungeon, a powerful foe who resides in the Throne Room.")
    print("     Only by defeating this boss can you truly conquer this place and claim your freedom through strength.")
    print()
    print("  2. The Path of the Escape Artist:")
    print("     Seek out a legendary artifact known as the 'Master key'. It is said to unlock any door.")
    print("     Find it, and you may be able to open the final gate in the Courtyard and slip away before the master knows you were ever free.")
    print()
    print("Explore the dungeon, gather weapons, tools, and consumables to aid your escapes.")
    print("Be wary of the monsters that lurk in rooms. Sometimes, fighting is not the only option—running may be the wiser choice.")
    separator()
    print("--- Basic Commands ---")
    print("  - move [north/south/east/west] : Travel between rooms. Initiates enemy encounter")
    print("  - take                         : Pick up an item from a room.")
    print("  - use item                     : Use a consumable from your inventory.")
    print("  - sneak                        : Attempt a surprise attack on an enemy before initiating enemy encounter")
    print("  - run                          : Attempt to flee from a room.")
    print("  - save                         : save game and exit")
    separator()

def boss_battle(player, boss):
    def player_boss_status(player, boss):
        print(f"{player.name}: {player.currentHp}/{player.maxHp}                {boss.name}: {boss.enemyHp}/{boss.enemyMaxHp}")
        player.view_equipment()
    
    def player_turn(player,boss, playerTurn):
        while playerTurn:
            action = input("What would you do? (attack    use item)\n    >>>")
            if action.lower() == "attack":
                player.attack(boss)
                playerTurn = False
            elif action.lower() == "use item":
                player.use_consumable(player.consumableSlot, player.currentHp, player.maxHp)
                playerTurn = False
            else:
                print("invalid action")
                continue
    
    while True:
        print(f"-------- [BOSS BATTLE] --------")
        player_boss_status(player, boss)
        print(f"It is your turn {player.name}!")
        player_turn(player,boss, playerTurn=True)
        separator()
        
        if boss.enemyHp > 0:
            print(f"Boss turn!")
            boss.attack(player)
            separator()
        
        if player.currentHp <= 0:
            print(f"You have been defeated by the {boss.name}.")
            print("GAME OVER")
            return False
            
        elif boss.enemyHp <= 0:
            print(f"You have defeated the {boss.name}. You Won!!! Congratulations!!!")
            del player.currentRoom.enemy_in_room[0]
            return True
            
        else:
            continue

def game_loop(player1, still_has_enemies, all_dungeon_rooms):

    no_of_enemies = still_has_enemies
    game_is_running = True
    player_has_won = False
    while game_is_running:
        
        separator()

        if player_has_won:
            print(f"{player1.name}, you have cleared the dungeon. Congratulations!")
            game_is_running = False 
            continue 
        elif player1.currentRoom.name == "Courtyard":
            print("You have found the exit and escaped the dungeon!")
            player_has_won = True
            continue
        elif player1.currentHp <= 0:
            print("You have been defeated. Better luck next time.")
            game_is_running = False 
            continue
        
        player1.player_status()
        
        # print(f"Number of enemies remaining: {still_has_enemies}")
        
        separator()
        
        if player1.currentRoom.enemy_in_room:
            hasEnemy = True
        else:
            hasEnemy = False
            
        player1.currentRoom.room_description(player1.currentRoom.name, player1.currentRoom.type, player1.currentRoom.items_in_room, player1.currentRoom.enemy_in_room)
        action = input("What will you do? (Move   Sneak    Take    Use Item    run    save)\n        >>>")
        
        if action.lower() == "move" and hasEnemy == True:
            if player1.currentRoom.enemy_in_room[0].enemyType == "normal":
                print("Move failed, the enemy notices you and attacks!!!")
                hasEnemy = player1.battle(player1.currentRoom.enemy_in_room[0], hasEnemy, still_has_enemies)
                separator()
            else:
                print("Move failed, the dungeon boss notices you!!!")
                boss = player1.currentRoom.enemy_in_room[0]
                player_has_won = boss_battle(player1, boss)

            
        elif action.lower() == "move" and not hasEnemy:
            print(player1.currentRoom.get_exit_description())

            direction_choice = input("Where do you want to go? (north    west    east    south\n        >>> ")

            player1.move(direction_choice)
            separator()
            
        elif action.lower() == "sneak":
            player_has_won = player1.sneak_attack(hasEnemy, player1.currentRoom.enemy_in_room, still_has_enemies, player_has_won, boss_battle)
            separator()
            
        elif action.lower() == "take":
            if player1.currentRoom.items_in_room:
                player1.take_item(player1.currentRoom.items_in_room[0])
                separator()
                
            else:
                print(f"No more items in {player1.currentRoom.name} to take.")
                separator()
        
        elif action.lower() == "use item":
            player1.use_consumable(player1.consumableSlot, player1.currentHp, player1.maxHp)
            separator()
        
        elif action.lower() == "run" and hasEnemy:
            enemy = player1.currentRoom.enemy_in_room[0]
            run_chance = player1.escapeChance
            player_has_won = player1.try_run(enemy, hasEnemy, no_of_enemies, run_chance, player_has_won, boss_battle)
        
        elif action.lower() == "run" and not hasEnemy:
            print(f"There are no enemy in {player1.currentRoom.name}. Just move.")
            
        elif action.lower() == "save":
            save_game(player1, all_dungeon_rooms)
            game_is_running = False
        
        else:
            print("Invalid action")
            separator()
            
