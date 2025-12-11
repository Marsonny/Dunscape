from utils.validators import validate_if_string, validate_if_number
from entities.abilities.base_ability import Ability
from utils.exceptions import SaveDataError
import random

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import Player

class Enemy:
    def __init__(self, name, enemyHp, enemyMaxHp, durabilityDamage, enemyType):
        self.name = validate_if_string(name, "name", "Enemy")
        self.enemyHp = validate_if_number(enemyHp, "enemyHp", "Enemy")
        self.enemyMaxHp = validate_if_number(enemyMaxHp, "enemyMaxHp", "Enemy")
        self.durabilityDamage = validate_if_number(durabilityDamage, "durabilityDamage", "Enemy")
        self.enemyType = validate_if_string(enemyType, "enemyType", "Enemy")
    
    def to_dict(self):
        return {
            "class": self.__class__.__name__, # Important for knowing if it's an Enemy or Boss
            "name": self.name,
            "enemyHp": self.enemyHp,
            "enemyMaxHp": self.enemyMaxHp,
            "durabilityDamage": self.durabilityDamage,
            "enemyType": self.enemyType
        }
    
    @classmethod
    def from_dict(cls, data):
        class_name = data.get('class')

        if class_name == 'Boss':
            # Create a Boss instance
            boss = Boss(
                name=data['name'],
                enemyHp=data['enemyHp'],
                enemyMaxHp=data['enemyMaxHp'],
                durabilityDamage=data['durabilityDamage'],
                enemyType=data['enemyType'],
                normalAtk=data['normalAtk'],
                abilities=data['abilities'],
                abilityCooldown=data['abilityCooldown']
            )
            # Restore its specific cooldown state
            boss.base_abilityCooldown = data['base_abilityCooldown']
            return boss
        elif class_name == 'Enemy':
            # Create a regular Enemy instance
            return Enemy(
                name=data['name'],
                enemyHp=data['enemyHp'],
                enemyMaxHp=data['enemyMaxHp'],
                durabilityDamage=data['durabilityDamage'],
                enemyType=data['enemyType']
            )
        else:
            raise SaveDataError(f"Unknown enemy class in save data: {class_name}")
        
class Boss(Enemy):
    def __init__(self, name, enemyHp, enemyMaxHp, durabilityDamage, enemyType, normalAtk, abilities : list[Ability], abilityCooldown):
        super().__init__(name, enemyHp, enemyMaxHp, durabilityDamage, enemyType)
        self.normalAtk = validate_if_number(normalAtk, "normalAtk", "Boss")
        self.abilities = abilities
        self.base_abilityCooldown = validate_if_number(abilityCooldown, "abilityCooldown", "Boss")
        self.abilityCooldown = self.base_abilityCooldown
    
    def to_dict(self):
        bossData = super().to_dict()
        bossData.update({
            "normalAtk": self.normalAtk,
            "abilities": self.abilities,
            "base_abilityCooldown": self.base_abilityCooldown,
            "abilityCooldown": self.abilityCooldown
        })
        return bossData
    
    def boss_status(self):
        print(f"{self.name}\Hp:{self.enemyHp}/{self.enemyMaxHp}     Ability Cooldown:{self.abilityCooldown}\nAtk Dmg: {self.normal_attack}")

    def normal_attack(self, player):
        print(f"The {self.name} performs a normal attack.")
        damage = player.boss_battle_speed_check(self, player)
        print(f"The {self.name} dealt {damage} points of damage to you.")
        player.currentHp -= damage
        
    def use_ability(self, player: 'Player'):
        if not self.abilities:
            print(f"{self.name} has no abilities to use!")
            return
            
        chosen_ability = random.choice(self.abilities)
        chosen_ability.use(caster=self, target=player)
            
    def attack(self, player):
        if self.abilityCooldown > 0:
            self.normal_attack(player)
            self.abilityCooldown -= 1
        else:
            self.use_ability(player)
            self.abilityCooldown = self.base_abilityCooldown 