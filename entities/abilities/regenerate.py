from .base_ability import Ability
class RegenerateAbility(Ability):
    """Restores 10% of the caster's maximum HP."""
    def use(self, caster, target):
        regenHp = caster.enemyMaxHp * 0.1
        caster.enemyHp = min(caster.enemyMaxHp, caster.enemyHp + regenHp)
        print(f"{caster.name} used Regenerate! It recovered {regenHp} HP.")