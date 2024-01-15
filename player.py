from wands import Wand
from spells import Spell, SPELL_TYPE_USELESS, SPELL_TYPE_UNFORGIVABLE

MAX_PLAYER_HEALTH = 500

class Player:
    def __init__(self, name: str, wand: Wand):
        self.name = name
        self.health = MAX_PLAYER_HEALTH
        self.wand = wand

        self.stunned_rounds = 0
        self.decreased_spell_speed = False
        self.decreased_spell_damage = False

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
    
    def cast_spell_result(self, spell: Spell, succes: bool):
        if (succes):
            message = "{name} casted '{spell}' with succes"
        else:
            if (spell.type == SPELL_TYPE_UNFORGIVABLE):
                message = "{name} tried to cast '{spell}' but didn't truly mean it. Cast FAILED!"
            elif (spell.type == SPELL_TYPE_USELESS):
                return "{name} must not be feeling well, since they casted a non existing spell. Cast FAILED!".format(name=self.name)
            else: message = "{name} tried to cast '{spell}' but mispronounced it. Cast FAILED!"
        return message.format(name=self.name, spell=spell.name)