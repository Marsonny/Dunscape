from .base_ability import Ability
class SharpenAbility(Ability):
   def use(self, caster, target):
       caster.enemyMaxHp -= (caster.enemyMaxHp * 0.05)
       caster.normalAtk += 5
       print(f"{caster.name} used Sharpen! Its max HP is reduced, but its attack power increased.")