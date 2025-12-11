from .base_ability import Ability
class WeakenAbility(Ability):
    def use(self, caster, target):
        defDown = target.playerDefense * 0.1
        target.playerDefense += defDown
        print(f"{caster.name} used Weaken! Your damage taken is increased.")