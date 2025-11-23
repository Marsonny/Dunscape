from entities.player import Player
from entities.items import Tool

def test_recalculate_stats_with_health_amulet():
    """
    Tests that the Amulet of Health correctly increases max HP by 50%.
    """
    # create a test player object    
    player = Player("Test Dummy", 50) 
    
    # create the sample tool to test 
    amulet = Tool("Amulet of Health", "Increases max HP.", "tool", "increase_max_hp")
    
    assert player.maxHp == 50

    player.toolSlot.append(amulet)

    # call the function to test
    player.recalculate_stats()

    expected_hp = 75
    assert player.maxHp == expected_hp