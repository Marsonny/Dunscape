from entities.abilities.heavy_slam import HeavySlamAbility
from entities.player import Player
from entities.enemy import Boss

def test_heavy_slam_ability():
    """
    Tests that the HeavySlamAbility correctly damages the player.
    """
    # ARRANGE
    # Create a mock player and a mock boss to be the target and caster.
    # We use a default class dict for the player.
    player = Player("Test Target", {"base_maxHp": 100})
    
    # The boss needs a normalAtk value for the ability to use.
    # The other stats don't matter for this specific test.
    boss = Boss("Test Caster", 1, 1, 1, "boss", 10, [], 1)
    
    # Create an instance of the ability we are testing.
    heavy_slam = HeavySlamAbility()

    # The player starts with full HP.
    assert player.currentHp == 100

    # ACT
    # Execute the ability, with the boss as the caster and player as the target.
    heavy_slam.use(caster=boss, target=player)

    # ASSERT
    # Heavy Slam damage is caster's normalAtk * 3. So, 10 * 3 = 30 damage.
    # The player's HP should be 100 - 30 = 70.
    assert player.currentHp == 70