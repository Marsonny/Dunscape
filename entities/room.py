from utils.validators import validate_if_string
from entities.items import Item
from entities.enemy import Enemy

class Room:
    def __init__(self, name, room_type):
        
        self.name = validate_if_string(name, "name", "Room")
        self.type = validate_if_string(room_type, "room_type", "Room")
        self.items_in_room = []
        self.enemy_in_room = []
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        
        self.n_locked = False
        self.w_locked = False
        self.e_locked = False
        self.s_locked = False
    
    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "items_in_room": [item.to_dict() for item in self.items_in_room],
            "enemy_in_room": [enemy.to_dict() for enemy in self.enemy_in_room],
            # Save the NAME of the connected room, or None if there's no connection
            "n_to": self.n_to.name if self.n_to else None,
            "s_to": self.s_to.name if self.s_to else None,
            "e_to": self.e_to.name if self.e_to else None,
            "w_to": self.w_to.name if self.w_to else None,
            "n_locked": self.n_locked,
            "w_locked": self.w_locked,
            "e_locked": self.e_locked,
            "s_locked": self.s_locked
        }
            
    def get_exit_description(self):
        """Generates a formatted string of all available exits and their status."""
        exit_lines = []
        directions = {
            "North": (self.n_to, self.n_locked),
            "West": (self.w_to, self.w_locked),
            "East": (self.e_to, self.e_locked),
            "South": (self.s_to, self.s_locked)
        }
        
        for direction, (linked_room, is_locked) in directions.items():
            if linked_room:
                status = ""
                if is_locked:
                    status += " (Locked)"
                if linked_room.enemy_in_room:
                    status += " !!! "
                exit_lines.append(f" {direction} : {linked_room.name} {linked_room.type}{status}")
            else:
                exit_lines.append(f" {direction} : Wall")
        return "\n".join(exit_lines)
        
    def link_room(self, other_room, direction, has_door):
        """ links each and every room, used in generate_dungeon function """
        if direction == "north":
            self.n_to = other_room
        elif direction == "south":
            self.s_to = other_room
        elif direction == "east":
            self.e_to = other_room
        elif direction == "west":
            self.w_to = other_room
        else:
            print("Invalid direction passed to link_room.")
            
    def room_description(self, name, type, itemsInRoom, enemyInRoom):
        """ Displays the all the things about the players currentRoom, the items and enemy in it. """
        print(f"---{name}----\nRoom type: {type}")
        if enemyInRoom:
            for enemy in enemyInRoom:
                print(f"There is a {enemy.name} in this room!")
                print(f"Enemy: {enemy.name}    Enemy Hp: {enemy.enemyHp}/{enemy.enemyMaxHp}")
                print()
        if itemsInRoom:
            print("Items: ")
            for item in itemsInRoom:
                print(f"- {item.name} : {item.description}")
        else:
            print("Items: \n- There are no more items in this room")

    def add_item(self, item):
        """ add 1 item each room, the item depends on the type of the room """
        self.items_in_room.append(item)
    
    def add_enemy(self, enemy):
        """ add 1 enemy to a room (Currently has 40% chance for a room to have an enemy) """
        self.enemy_in_room.append(enemy)