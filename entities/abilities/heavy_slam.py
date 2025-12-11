from __future__ import annotations
from typing import TYPE_CHECKING
from .base_ability import Ability

if TYPE_CHECKING:
    from entities.player import Player
    from entities.enemy import Boss

class HeavySlamAbility(Ability):
    """A powerful attack that deals 3x the caster's normal attack damage."""
    
    def use(self, caster: Boss, target: Player):
        damage = caster.normalAtk * 3
        print(f"{caster.name} used Heavy Slam!")
        print(f"It dealt {damage} points of damage to you.")
        target.currentHp -= damage