from random import random

SPELL_TYPE_USELESS      = 0
SPELL_TYPE_DEFENSE      = 1
SPELL_TYPE_COMMON       = 2
SPELL_TYPE_POWERFUL     = 3
SPELL_TYPE_UNFORGIVABLE = 4

# If SPELL_TYPE_DEFENSE is casted, always these chances to heal partly (restore 5% of max hp) or completely
CHANCE_HEAL_PARTLY      = 25
CHANCE_HEAL_FULLY       = 5

__INVALID_SPELL = ".@wizardduel@__spell_invalid__" #Internal usage only

##
## Spell class
##
class Spell:
    spellList = []

    #Class special methods
    """
        name        (str)   Name of the spell as used in combat
        speed       (int)   Speed of the spell. This will determine what spell hits who in a single move. The spell of the wizard with the lowest spell speed won't hit the player.
                            If spells have the same speed, both will be executed        
        damage      (int)   Damage that the spell does. 
                            <!> Negative damage takes away moves from opponent (eg -2 = cancel 2 moves of opponent)
        succes_rate (int)   How much chance for the spell to be succesfully cast. If it fails, spell won't be cast (thus spells with a succes_rate of 0 would never be executed, and 100=always succes)
        description (str)   Description of the spell
        type        (int)   Type of the spell:
                            - SPELL_TYPE_USELESS: Spell that do nothing in combat
                            - SPELL_TYPE_DEFENSE: Defensive spell - Prevent incoming damage. Has 25% chance to restore 5% of caster total health and 5% chance to fully restore health
                            - SPELL_TYPE_COMMON: Common combat spell - Deals some damage
                            - SPELL_TYPE_POWER: Powerful combat spell - deals alot of damage or takes away a few moves from opponent
                            - SPELL_TYPE_UNFORGIVABLE: deals alot of damage or takes away alot of moves from opponent
    """
    def __init__(self, name: str, speed: int, damage: int, succes_rate: int, description: str, type: int = SPELL_TYPE_COMMON):
        self.name = name
        self.speed = speed
        self.damage = damage
        self.succes_rate = succes_rate
        self.description = description
        self.type = type

        Spell.spellList.append(self)

    def __repr__(self):
        return " ['{spell}']\n\t{desc}\n\tSUCCES RATE: {srate}%\tSPEED: {speed}\tDAMAGE: {dmg}".format(spell=self.name, type=type, desc=self.description, srate=self.succes_rate, speed=self.speed, dmg=self.damage)
    
    def chance_heal_partly_succes(self):
        return self.type == SPELL_TYPE_DEFENSE and CHANCE_HEAL_PARTLY > random.random() * 100
    
    def chance_heal_fully_succes(self):
        return self.type == SPELL_TYPE_DEFENSE and CHANCE_HEAL_FULLY > random.random() * 100