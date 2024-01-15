from wands import Wand
from spells import Spell, SPELL_TYPE_USELESS, SPELL_TYPE_UNFORGIVABLE

MAX_PLAYER_HEALTH = 500

class Player:
    def __init__(self, name: str, wand: Wand):
        self.name = name
        self.health = MAX_PLAYER_HEALTH
        self.wand = wand

        self.stunned_rounds = 0
        self.lumos = False

    def give_health(self, health: int):
        self.health += health
        if self.health > MAX_PLAYER_HEALTH:
            self.health = MAX_PLAYER_HEALTH
        return self.health

    def take_health(self, health: int):
        self.health -= health
        if self.health < 0:
            self.health = 0
        return self.health
    
    def get_spell_succes_rate(self, spell: Spell):
        return 1 * self.wand.succes_rate * spell.succes_rate