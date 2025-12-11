from __future__ import annotations
from typing import TYPE_CHECKING

# This is a common pattern to avoid circular import errors with type hints.
if TYPE_CHECKING:
    from entities.player import Player
    from entities.enemy import Boss

class Ability:
    """A base class for all abilities in the game."""
    
    def use(self, caster: Boss, target: Player):
        """
        Executes the ability's logic.
        This method must be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the 'use' method.")