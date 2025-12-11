from entities.player import Player
from entities.items import Tool

def test_recalculate_stats_with_health_amulet():
    """
    Tests that the Amulet of Health correctly increases max HP by 50%.
    """
    # create a test player object    
    default_class_data = { "base_maxHp": 50 }
    player = Player("Test Dummy", default_class_data) 
    
    # create the sample tool to test 
    amulet = Tool("Amulet of Health", "Increases max HP.", "tool", "increase_max_hp")
    
    assert player.maxHp == 50

    player.toolSlot.append(amulet)

    # call the function to test
    player.recalculate_stats()

    expected_hp = 75
    assert player.maxHp == expected_hp

# To avoid a circular dependency, we can use a simple helper class
# for the test instead of importing a future PlayerClass from a new file.
# Or, even better, for now, let's just use a dictionary to represent the class data.
# This tests the Player's logic without needing the class system to be fully built yet.
# ... (your existing test_recalculate_stats_with_health_amulet goes here) ...

def test_player_creation_with_class_stats():
    """
    Tests that the Player's base stats are set correctly based on a class object.
    """
    # ARRANGE: Define the stat modifiers for our "Vanguard" class.
    # We'll use a simple dictionary for now to represent the class data.
    vanguard_class = {
        "name": "Vanguard",
        "base_maxHp": 70,       # Higher than default 50
        "base_damage": 3,       # Lower than default 5
        "base_speed": 15,       # Lower than default 20
        "base_defense": 0.8     # Lower is better (80% damage taken)
    }

    # ACT: Create a new Player, passing this class data to its constructor.
    player = Player(name="Sir Testalot", class_data=vanguard_class)

    # ASSERT: Check if the player's base stats match the class data.
    assert player.name == "Sir Testalot"
    assert player.base_maxHp == 70
    assert player.currentHp == 70 # Current HP should match the new max HP at start
    assert player.base_damage == 3
    assert player.base_speed == 15
    assert player.base_defense == 0.8