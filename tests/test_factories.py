import pytest
from utils.exceptions import SaveDataError
from entities.items import Item, Weapon, Tool, Consumable

def test_item_from_dict_creates_weapon():
    """Tests creating a Weapon from a dictionary."""
    # Create sample data for a Weapon
    weapon_data = {
        "class": "Weapon",
        "name": "Iron Sword",
        "description": "A basic sword.",
        "type": "weapon",
        "weaponDamage": 10,
        "durability": 25
    }

    # ACT: Call the factory method with the data.
    created_item = Item.from_dict(weapon_data)

    # ASSERT: Check if the created object is what we expect.
    # 1. Is it the correct class?
    assert isinstance(created_item, Weapon)
    
    # 2. Were the attributes assigned correctly?
    assert created_item.name == "Iron Sword"
    assert created_item.weaponDamage == 10


def test_item_from_dict_creates_tool():
    """Tests creating a Tool from a dictionary."""
    # ARRANGE
    tool_data = {
        "class": "Tool",
        "name": "Master key",
        "description": "Unlocks any door.",
        "type": "tool",
        "ability": "unlock_doors"
    }

    # ACT
    created_item = Item.from_dict(tool_data)

    # ASSERT
    assert isinstance(created_item, Tool)
    assert created_item.name == "Master key"
    assert created_item.ability == "unlock_doors"


def test_item_from_dict_creates_consumable():
    """Tests creating a Consumable from a dictionary."""
    # ARRANGE
    consumable_data = {
        "class": "Consumable",
        "name": "Health Potion",
        "description": "Heals 15 HP.",
        "type": "consumable",
        "effect": 15
    }

    # ACT
    created_item = Item.from_dict(consumable_data)

    # ASSERT
    assert isinstance(created_item, Consumable)
    assert created_item.name == "Health Potion"
    assert created_item.effect == 15
    
    # In dungeon_game/tests/test_factories.py

def test_item_from_dict_raises_error_for_unknown_class():
    """
    Tests that the factory raises a SaveDataError for an invalid class name.
    """
    # ARRANGE: Create data with a class name that doesn't exist.
    bad_data = {
        "class": "MagicWand",
        "name": "Stick of Power",
        "description": "It zaps.",
        "type": "weapon"
    }

    # ACT & ASSERT: Use pytest.raises to check for the expected error.
    with pytest.raises(SaveDataError):
        Item.from_dict(bad_data)
        
# In dungeon_game/tests/test_factories.py
# (at the end of the file)

from entities.enemy import Enemy, Boss

# ... (your existing 4 item factory tests go here) ...

def test_enemy_from_dict_creates_enemy():
    """Tests creating a normal Enemy from a dictionary."""
    # ARRANGE
    enemy_data = {
        "class": "Enemy",
        "name": "Goblin Scout",
        "enemyHp": 12,
        "enemyMaxHp": 12,
        "durabilityDamage": 5,
        "enemyType": "normal"
    }

    # ACT
    created_enemy = Enemy.from_dict(enemy_data)

    # ASSERT
    assert isinstance(created_enemy, Enemy)
    assert not isinstance(created_enemy, Boss) # Make sure it's NOT a Boss
    assert created_enemy.name == "Goblin Scout"
    assert created_enemy.enemyHp == 12


def test_enemy_from_dict_creates_boss():
    """Tests creating a Boss from a dictionary."""
    # ARRANGE
    boss_data = {
        "class": "Boss",
        "name": "King Goblin",
        "enemyHp": 100,
        "enemyMaxHp": 100,
        "durabilityDamage": 10,
        "enemyType": "boss",
        "normalAtk": 5,
        "abilities": ["Regenerate", "HeavySlam"],
        "base_abilityCooldown": 2,
        "abilityCooldown": 2
    }

    # ACT
    created_enemy = Enemy.from_dict(boss_data)

    # ASSERT
    assert isinstance(created_enemy, Boss)
    assert created_enemy.name == "King Goblin"
    assert created_enemy.normalAtk == 5
    assert created_enemy.abilities == ["Regenerate", "HeavySlam"]