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
    
    def get_queued_effects(self):
        output = ""
        effect_slowed = "Slowed"
        effect_blinded = "Blinded"

        if (self.decreased_spell_speed):
            output = effect_slowed
        if (self.decreased_spell_damage):
            if not output:
                output = effect_blinded
            else: output += ", " + effect_blinded
        
        if not output: output = "None"
        return output

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
    
    def cast_spell(self, spell: Spell, opponent): #: Player ?
        # Below is pretty much a placeholder and will be implemented after placing all cast_spell()s in game.py
        print("> {} hits {} and does {} damage!".format(self.name, opponent.name, spell.damage))
        opponent.health -= spell.damage