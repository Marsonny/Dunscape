from utils.validators import validate_if_string, validate_if_number
from entities.items import Item, Weapon, Tool, Consumable
from entities.room import Room
from entities.enemy import Enemy, Boss
import random

    
class Player:
    def __init__(self, name: str, class_data: dict):
        
        self.name = validate_if_string(name, "name", "Player")
        self.player_class = validate_if_string(class_data.get('name'), "player_class", "Player")
        self.base_maxHp = validate_if_number(class_data.get('base_maxHp', 50), "base_maxHp", "Player")
        self.base_damage = validate_if_number(class_data.get('base_damage', 5), "base_damage", "Player")
        self.base_sneakMultiplier = validate_if_number(class_data.get('base_sneakMultiplier', 2.0), "base_sneakMultiplier", "Player")
        self.base_speed = validate_if_number(class_data.get('base_speed', 20), "base_speed", "Player")
        self.base_defense = validate_if_number(class_data.get('base_defense', 1.0), "base_defense", "Player")
        self.base_sneakAccuracy = validate_if_number(class_data.get('base_sneakAccuracy', 0.3), "base_sneakAccuracy", "Player")
        self.base_escapeChance = validate_if_number(class_data.get('base_escapeChance', 0.3), "base_escapeChance", "Player")
        
        self.maxHp = self.base_maxHp
        self.currentHp = self.maxHp
        self.currentDamage = self.base_damage
        self.sneakMultiplier = self.base_sneakMultiplier
        
        self.playerSpeed = self.base_speed
        self.playerDefense = self.base_defense 
        self.sneakAccuracy = self.base_sneakAccuracy
        self.escapeChance = self.base_escapeChance
        
        
        self.weaponDurability = 0 
        self.canUnlockDoors = False
        self.unbreakableWpn = False
        self.currentRoom : Room = None
        self.weaponSlot : list[Weapon] = []
        self.toolSlot : list[Tool] = []
        self.consumableSlot : list[Consumable] = []
    
    def to_dict(self):
        return {
            "class" : self.__class__.__name__,
            "name" : self.name,
            "currentHp" : self.currentHp,
            "currentRoom" : self.currentRoom.name,
            "base_stats": {
                'base_maxHp': self.base_maxHp,
                'base_damage': self.base_damage,
                'base_sneakMultiplier': self.base_sneakMultiplier,
                'base_speed': self.base_speed,
                'base_defense': self.base_defense,
                'base_sneakAccuracy': self.base_sneakAccuracy,
                'base_escapeChance': self.base_escapeChance
            },
            "inventory" : {
                "weapon": [item.to_dict() for item in self.weaponSlot],
                "tool" : [item.to_dict() for item in self.toolSlot],
                "consumable" : [item.to_dict() for item in self.consumableSlot]
            }
        }

    def recalculate_stats(self):
        """
        Resets stats to their base values and then applies all
        bonuses from currently equipped items.
        """
        # 1. Reset all stats to their base values
        self.maxHp = self.base_maxHp
        self.currentDamage = self.base_damage
        self.sneakMultiplier = self.base_sneakMultiplier
        self.playerSpeed = self.base_speed
        self.playerDefense = self.base_defense
        self.canUnlockDoors = False
        self.sneakAccuracy = self.base_sneakAccuracy
        self.escapeChance = self.base_escapeChance
        
        # 2. Apply weapon stats
        if self.weaponSlot:
            weapon = self.weaponSlot[0]
            self.currentDamage += weapon.weaponDamage
            self.weaponDurability = weapon.durability
            self.unbreakableWpn = False
        else:
            self.weaponDurability = 0
            
        # 3. Apply tool stats by looping through them
        if self.toolSlot:
            tool = self.toolSlot[0]
            # This is where the bug is fixed!
            if tool.ability == "increase_max_hp":
                self.maxHp += (self.base_maxHp * 0.50)
                print("Max Hp increased by 50%")
            elif tool.ability == "improve_sneaking":
                self.sneakMultiplier = 5.0
                print("Sneak atack damage multiplier is now 5 fold.")
            elif tool.ability == "improve_speed":
                self.playerSpeed = 60
                print("Speed has improved Greatly. Dodging enemy attacks is now easier.")
            elif tool.ability == "increase_weapon_damage":
                self.currentDamage += 15
                print("Damage has increased by 15 points")
            elif tool.ability == "impove_durability":
                if self.weaponSlot:
                    self.unbreakableWpn = True
                    print("Equipped weapons are now unbreakable.")
                else:
                    print("No weapon equipped. Tool did nothing.")
            elif tool.ability == "unlock_doors":
                self.canUnlockDoors = True
                print("Locked door can now be unlocked.")
            elif tool.ability == "improve_defense":
                self.playerDefense = 0.50
                print("Player defense greatly increased.")      
            elif tool.ability == "improve_sneak_accuracy":
                self.sneakAccuracy = 0.8
                print("Accuracy of sneak attack greatly increased.")   
            elif tool.ability == "improve_escape_chance":
                self.escapeChance = 0.8
                print("Escaping ability greatly enhanced.")       

        # Ensure current HP doesn't exceed the new max HP
        if self.currentHp > self.maxHp:
            self.currentHp = self.maxHp
            
    def player_status(self):
        """ Displays some of the player stats """
        print(f"{self.name}     Class: {self.player_class}\nHp: {self.currentHp}/{self.maxHp}    Weapon Damage: {self.currentDamage}    Weapon Durability: {self.weaponDurability}")
        print(f"Damage Receive: {self.playerDefense *100}%    Speed: {self.playerSpeed}    Sneak Atk Mult: {self.sneakMultiplier}x")
        print(f"Master Key: {self.canUnlockDoors}    Escape chance: {self.escapeChance *100}%    Sneak Accuracy: {self.sneakAccuracy * 100}%")
        self.view_equipment()
        
    def view_equipment(self):
        """ display the players weapon, tool and consumable slots """
        print("---Weapon Slot---")
        if self.weaponSlot:
            weapon = self.weaponSlot[0]
            print(f"   <<< [{weapon.name}] >>>")
        else:
            print("   <<< [] >>>")
        
        print("---Tool Slot---")
        if self.toolSlot:
            tool = self.toolSlot[0]
            print(f"   <<< [{tool.name}] >>>")
        else:
            print("   <<< [] >>>")
        
        print("---consumable Slot---")
        if self.consumableSlot:
            consumable = self.consumableSlot[0] 
            print(f"   <<< [{consumable.name}] >>>")
        else:
            print("   <<< [] >>>")
           
    def take_item(self, item):
        """ Checks the item type and place it in the correct item slot """
        if item.type == "weapon" and len(self.weaponSlot) < 1:
            self.weaponSlot.append(item)
            self.currentRoom.items_in_room.remove(item)
            print(f"You have equipped a {item.name} in your weapon slot. Damage increased by {item.weaponDamage} points.")
            self.currentDamage += item.weaponDamage
            self.weaponDurability = item.durability
            self.recalculate_stats()
        elif item.type == "tool" and len(self.toolSlot) < 1:
            self.toolSlot.append(item)
            self.currentRoom.items_in_room.remove(item)
            print(f"You have equipped the {item.name} in your tool slot.")
            self.recalculate_stats()
        elif item.type == "consumable" and len(self.consumableSlot) < 1:
            self.consumableSlot.append(item)
            self.currentRoom.items_in_room.remove(item)
            print(f"You have taken the {item.name} and put it in your consumable slot.")
            self.recalculate_stats()
        else:
            action = input(f"{item.type} slot is full. Would you like to replace your current {item.type} with this {item.name}?(y/n)\n        >>>")
            if action.lower() == "y":
                self.drop_item(item, self.weaponSlot, self.toolSlot, self.consumableSlot, self.currentRoom.items_in_room)
                # self.check_equipment(weaponSlot, toolSlot)
            elif action.lower() == "n":
                print(f"You kept your current {item.type}.")
                
    def weaponBreak(self, durabilityDamage):
        """ checks if current weapon is broken or not """
        if self.weaponSlot:
            weapon = self.weaponSlot[0]
            for weapon in self.weaponSlot:
                # weapon.durability -= durabilityDamage
                if self.unbreakableWpn:
                    self.weaponDurability -= 0
                else:
                    weapon.durability -= durabilityDamage
                    self.weaponDurability = weapon.durability
                print(f"current durability stat: {self.weaponDurability}")
                if self.weaponDurability <= 0 and weapon.durability <= 0:
                    print(f"Your {self.weaponSlot[0].name} broke!")
                    self.weaponDurability = 0
                    self.currentDamage -= weapon.weaponDamage
                    del self.weaponSlot[0]
        
                else:
                    print(f"Your {weapon.name}'s durability has taken {durabilityDamage} points of durability damage.")
            
                
    def use_consumable(self, slot, currentHp, maxHp):
        """ Checks if the consumable slot is not empty, and use the item if true, else display a message """
        if len(slot) > 0:
                
            for item in slot:
                if currentHp == maxHp:
                    print(f"Hp is still full. You put the {item.name} back in your consumable slot")
                else:
                    print(f"You used {item.name}, {item.effect}hp has been restored")
                    self.currentHp += item.effect
                    if self.currentHp > self.maxHp:
                        self.currentHp = self.maxHp
                    slot.remove(item) 
                    # self.player_status(currentHp, maxHp, currentDamage=self.weaponSlot)
        else:
            print("You have no consumable item in your consumable slot")
    
    def drop_item(self, item, weaponSlot, toolSlot, consumableSlot, roomSlot):
        """ used whenever the player decides to pick an item for a slot even when said slot is already used """
        if item.type == "weapon":
            del weaponSlot[0]
            weaponSlot.append(item)
            roomSlot.remove(item)
            print(f"You have changed your {item.type} in your weapon slot. Damage increased by {item.weaponDamage} points.")
            self.recalculate_stats()
        elif item.type == "tool":
            del toolSlot[0]
            toolSlot.append(item)
            roomSlot.remove(item)
            print(f"You have changed your {item.type} in your tool slot.")
            self.recalculate_stats()
        elif item.type == "consumable":
            del consumableSlot[0]
            consumableSlot.append(item)
            roomSlot.remove(item)
            print(f"You have changed your {item.type} in your consumable slot.")
          
                    
    def battle(self, enemy, hasEnemy, noOfEnemies):
        damage = 0
        """ handles the battle event between the player and the enemy """
        speed = self.playerSpeed * 0.01
        if self.weaponSlot:
            for weapon in self.weaponSlot:
                print(f"You used your {weapon.name} to attack the {enemy.name}")
                enemy.enemyHp -= self.currentDamage
                print(f"{enemy.name} has suffered {self.currentDamage} points of damage.")
                print(f"{enemy.name} has {enemy.enemyHp} Hp remaining")
            if enemy.enemyHp > 0:
                print(f"The {enemy.name} fights back.")
                damage = self.speed_check(enemy)
                self.currentHp -= damage
                print(f"You suffered {enemy.enemyHp} points of damage.")
                if self.currentHp <= 0:
                    print(f"The {enemy.name} has defeated you. you have died.")
                    self.currentHp = 0
                    print("GAME OVER")
                else:
                    print(f"You have defeated the {enemy.name}.")
                    self.weaponBreak(enemy.durabilityDamage)
                    self.currentRoom.enemy_in_room.remove(enemy)
                    noOfEnemies -= 1
                    hasEnemy = False
                    return hasEnemy
            else:
                print(f"You have defeated the {enemy.name}.")
                self.weaponBreak(enemy.durabilityDamage)
                self.currentRoom.enemy_in_room.remove(enemy)
                hasEnemy = False
                return hasEnemy
        else:
            print(f"You have no weapon, you used your fist to attack the {enemy.name}.")
            print(f"The {enemy.name} fights back.")
            damage = self.speed_check(enemy)
            damage -= self.currentDamage
            self.currentHp -= damage
            print(f"You suffered {damage} points of damage.")
            if self.currentHp <= 0:
                print(f"The {enemy.name} has defeated you. you have died.")
                self.currentHp = 0
                print("GAME OVER")
            else:
                print(f"You have defeated the {enemy.name}.")
                self.currentRoom.enemy_in_room.remove(enemy)
                noOfEnemies -= 1
                hasEnemy = False
                return hasEnemy
                
             
    def move(self, direction):
        """Moves the player in a given direction after checking for locks and validity."""
        direction = direction.lower()
        
        # Data-driven lookup instead of if/elif chain
        direction_map = {
            "north": ("n_to", "n_locked", "s_locked"),
            "west": ("w_to", "w_locked", "e_locked"),
            "east": ("e_to", "e_locked", "w_locked"), 
            "south": ("s_to", "s_locked", "n_locked")
           
        }

        if direction not in direction_map:
            print(f"'{direction}' is not a valid direction.")
            return

        room_attr, lock_attr, prev_lock_attr = direction_map[direction]
        
        # getattr is a built-in function to get an attribute from an object by its string name
        next_room = getattr(self.currentRoom, room_attr)
        is_locked = getattr(self.currentRoom, lock_attr)

        if next_room is None:
            print("You can't go that way. It's a solid wall.")
        elif is_locked:
            print("The door is locked.")
            if self.canUnlockDoors:
                print("Using your Master Key, you unlock the door.")
                setattr(self.currentRoom, lock_attr, False) # Unlock the door
                self.currentRoom = next_room
                setattr(self.currentRoom, prev_lock_attr, False)
                print(f"You moved {direction}, you are now in {self.currentRoom.name}")
            else:
                print("You don't have a way to unlock it.")
        else:
            self.currentRoom = next_room
            setattr(self.currentRoom, prev_lock_attr, False)
            print(f"You moved {direction}, you are now in {self.currentRoom.name}")
            
    def sneak_attack(self, hasEnemy, enemyList, noOfEnemies, player_has_won, boss_battle_func):
        """ handles the sneak action, which lets the player deal preemptive damage with a 30% chance of success"""
        for enemy in enemyList:
            if hasEnemy:
                print(f"You tried to sneak attack the {enemy.name}...")
                if random.random() <= self.sneakAccuracy:
                    sneakDamage = self.currentDamage * self.sneakMultiplier
                    print(f"It succeeds, you dealt {sneakDamage} points of damage")
                    enemy.enemyHp -= sneakDamage
                    if enemy.enemyHp > 0:
                        print(f"{enemy.name} has {enemy.enemyHp} Hp remaining")
                        if enemy.enemyType == "normal":
                            self.battle(enemy, hasEnemy, noOfEnemies)
                        else:
                            player_has_won = boss_battle_func(self, enemy)
                            return player_has_won
                    else:
                        print(f"You defeated the {enemy.name}.")
                        self.weaponBreak(enemy.durabilityDamage)
                        del self.currentRoom.enemy_in_room[0]
                else:
                    print(f"It failed. The enemy now notices you.")
                    if enemy.enemyType == "normal":
                        self.battle(enemy, hasEnemy, noOfEnemies)
                    else:
                        player_has_won = boss_battle_func(self, enemy)
                        return player_has_won
        else:
            print(f"There are no enemy in {self.currentRoom.name}")
            
    def try_run(self,enemy, hasEnemy, noOfEnemies, runChance, player_has_won, boss_battle_func):
        print(f"You are trying to run from {self.currentRoom.name}")
        print(self.currentRoom.get_exit_description())
        run_direction = input("Which direction are you tyring to go?\n     >>>")
        if random.random() <= runChance:
            print(f"You tried to run {run_direction}. It succeeds.")
            self.move(run_direction)
        else:
            if enemy.enemyType == "normal":
                print(f"You tried to run {run_direction}. It Failed. The enemy notices you and attacks.")
                self.battle(enemy, hasEnemy, noOfEnemies)
            else:
                print(f"You tried to run {run_direction}. It Failed. The {enemy.name} notices you!!!")
                player_has_won = boss_battle_func(self, enemy)
                return player_has_won
                
    def speed_check(self, enemy):
        speed = self.playerSpeed * 0.01
        if random.random() <= speed:
            print(f"Your speed helped you dodge some of the {enemy.name}'s attacks.")
            enemy.enemyHp *= (1 - speed)
        enemy.enemyHp *= self.playerDefense
        return enemy.enemyHp
    
    def boss_battle_speed_check(self, boss, player):
        speed = player.playerSpeed * 0.01
        if random.random() <= speed:
            print(f"Your speed helped you dodge some of the {boss.name}'s attacks.")
            damage =  boss.normalAtk * (1 - speed)
            damage *= self.playerDefense
        else:
            damage = boss.normalAtk * self.playerDefense
        return damage
    
    def attack(self, enemy):
        print(f"You attacked the {enemy.name}.")
        enemy.enemyHp -= self.currentDamage
        print(f"You dealt {self.currentDamage} points of damage.")