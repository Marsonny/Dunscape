from entities.items import Consumable, Weapon, Tool
from entities.room import Room
from entities.enemy import Enemy, Boss
from entities.abilities.regenerate import RegenerateAbility
from entities.abilities.heavy_slam import HeavySlamAbility
from entities.abilities.weaken import WeakenAbility
from entities.abilities.sharpen import SharpenAbility

PLAYER_CLASSES = {
    "vanguard": {
        "name": "Vanguard",
        "description": "A defensive powerhouse. High HP and defense, low speed and damage.",
        "base_maxHp": 70,
        "base_damage": 3,
        "base_speed": 15,
        "base_defense": 0.8  # Takes only 80% of damage
    },
    "shadow": {
        "name": "Shadow",
        "description": "A master of stealth. Excels at sneak attacks, but is frail.",
        "base_maxHp": 40,
        "base_sneakMultiplier": 4.0, # High sneak damage
        "base_sneakAccuracy": 0.5,   # High sneak chance
        "base_speed": 25
    },
    "reaver": {
        "name": "Reaver",
        "description": "A high-risk, high-reward attacker. High damage, low defense.",
        "base_maxHp": 50,
        "base_damage": 8,            # Very high starting damage
        "base_defense": 1.2          # Takes 120% of damage
    },
    "pathfinder": {
        "name": "Pathfinder",
        "description": "A resourceful survivor. Better at escaping and adapting to found gear.",
        "base_maxHp": 50,
        "base_escapeChance": 0.5,    # High chance to run
        "base_speed": 22
        # Note: We can add a passive for weapon durability later
    }
}

#item(consumables)
consumable_pool = [
    Consumable("Moldy Bread", "A hard piece of bread. Barely edible. (Heals 5 HP)", "consumable", 5),
    Consumable("Weak Healing Salve", "A smelly paste made from common herbs. (Heals 8 HP)", "consumable", 8),
    Consumable("Foraged Berries", "A handful of wild red berries. Might be poisonous? (Heals 3 HP)", "consumable", 3),
    Consumable("Standard Health Potion", "A bottle of fizzing red liquid. A welcome sight. (Heals 15 HP)", "consumable", 15),
    Consumable("Roasted Rat Meat", "A grim meal, but nourishing. (Heals 9 HP)", "consumable", 9),
    Consumable("Fungal Spore", "A glowing mushroom cap. Tastes like dirt. (Heals 4 HP)", "consumable", 4),
    Consumable("Strong Health Potion", "A larger bottle of a more vibrant red liquid. (Heals 25 HP)", "consumable", 25),
    Consumable("Goblin Grog", "A murky, potent brew. Smells terrible but is surprisingly effective. (Heals 12 HP)", "consumable", 12),
    Consumable("Waterskin", "Water from an unknown source. Surprisingly refreshing. (Heals 8 HP)", "consumable", 8),
    Consumable("Hardtack Biscuit", "A dry, hard biscuit. A staple for doomed adventurers. (Heals 8 HP)", "consumable", 8),
    Consumable("Mysterious Mushroom", "A purple mushroom with orange spots. You feel compelled to eat it. (Heals 2 HP)", "consumable", 2),
    Consumable("Elixir of Vigor", "A tiny vial containing a golden, glowing liquid. Reserved for dire emergencies. (Heals 45 HP)", "consumable", 45)
]

#item(weapons)
weapon_pool = [
    Weapon("Rusty Dagger", "A small, pitted dagger. Better than nothing. (Dmg: 5   Dur: 20)", "weapon", 5, 20),
    Weapon("Iron Shortsword", "A standard-issue shortsword. Reliable and sharp. (Dmg: 10   Dur: 25)", "weapon", 10, 25),
    Weapon("Goblin Club", "A crude, heavy club that smells awful. (Dmg: 15   Dur: 25)", "weapon", 15, 25),
    Weapon("Wooden Training Staff", "A long, smooth staff, surprisingly sturdy. (Dmg: 5   Dur: 20)", "weapon", 5, 20),
    Weapon("Stone War Hammer", "A heavy block of granite affixed to a thick handle. Slow but powerful. (Dmg: 20   Dur: 20)", "weapon", 20, 20),
    Weapon("Elven Shortbow", "A gracefully curved bow made of yew. Requires arrows. (Dmg: 12   Dur: 15)", "weapon", 12, 15),
    Weapon("Orcish Cleaver", "A brutal, heavy-bladed weapon designed for chopping. (Dmg: 15   Dur: 25)", "weapon", 15, 25)
]

#item(tools)
tool_pool = [
    Tool("Master key", "A mysterious key that changes shape to unlock any doors with ease", "tool", "unlock_doors"),
    Tool("Amulet of Health", "A warm, glowing stone that slightly increases your maximum HP when held.", "tool", "increase_max_hp"),
    Tool("Boots of Silence", "Soft leather boots that muffle the sound of your footsteps.", "tool", "improve_sneaking"),
    Tool("Assassin's Cloak", "A dark cloak that make the user blends with the shadow.", "tool", "improve_sneak_accuracy"),
    Tool("Knight's ring", "A ring given to knights that failed to protect their master with their weapon.", "tool", "impove_durability"), 
    Tool("Goddess necklace", "A necklace depicting a forgotten goddess of the old world. ", "tool", "improve_defense"),
    Tool("Ring of Blades", "A ring that looks like swords bought together to form a ring.", "tool", "increase_weapon_damage"), 
    Tool("Boots of swiftness", "A lightweight Boots with a strange wing design on the side.", "tool", "improve_speed"),
    Tool("Cloak of invisibility", "A cloak that makes you invisible, making it easy to run from enemies", "tool", "improve_escape_chance")
]

#rooms 

all_rooms = [
    Room("Room 1", "normal"),
    Room("Room 2", "normal"),
    Room("Room 3", "normal"),
    Room("Room 4", "armory"),
    Room("Room 5", "normal"),
    Room("Room 6", "armory"),
    Room("Room 7", "normal"),
    Room("Room 8", "treasury"),
    Room("Room 9", "normal"),
    Room("Room 10", "normal"),
    Room("Room 11", "normal"),
    Room("Room 12", "treasury"),
    Room("Room 13", "armory"),
    Room("Room 14", "normal"),
    Room("Room 15", "treasury"),
    Room("Room 16", "normal")
]

fixed_rooms = [
    Room("Prison Cell", "normal"),
    Room("Throne Room", "normal"),
    Room("Courtyard", "normal")
]

#enemies
enemy_pool = [
    #Weak Enemies
    Enemy("Giant Rat", 8, 8, 5, "normal"),
    Enemy("Small Slime", 10, 10, 5, "normal"),
    Enemy("Goblin Scout", 12, 12, 5, "normal"),
    Enemy("Cave Bat", 6, 6, 1, "normal"),
    Enemy("Frenzied Skeleton", 15, 15, 5, "normal"),

    #Medium Enemies
    Enemy("Orc Grunt", 25, 25, 8, "normal"),
    Enemy("Dungeon Guard", 22, 22, 7, "normal"),
    Enemy("Giant Spider", 18, 18, 7, "normal"),
    Enemy("Shadow Lurker", 20, 20, 8, "normal"),
    Enemy("Armored Ghoul", 25, 25, 8, "normal"),

    #Strong Enemies 
    Enemy("Hobgoblin Captain", 35, 35, 10, "normal"),
    Enemy("Stone Golem", 40, 40, 15, "normal"),
    Enemy("Cave Troll", 40, 40, 13, "normal"),
    Enemy("Animated Armor", 40, 40, 13, "normal"),
    Enemy("Cursed Knight", 38, 38, 13, "normal")
]

# boss enemies 
boss_pool = [
    Boss("King Goblin", 100, 100, 10, "boss", 5, 
         [RegenerateAbility(), HeavySlamAbility(), WeakenAbility()], 2),
    Boss("Steel Golem", 150, 150, 25, "boss", 10, 
         [SharpenAbility(), HeavySlamAbility()], 1)
]