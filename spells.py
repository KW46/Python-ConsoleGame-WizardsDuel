import random
from game_config import CHANCE_HEAL_PARTLY, CHANCE_HEAL_FULLY, DEBUG_MODE, MAX_LEVENSHTEIN_DISTANCE

if MAX_LEVENSHTEIN_DISTANCE > 0:
    from Levenshtein import distance

SPELL_TYPE_NONE         = -1
SPELL_TYPE_USELESS      = 0
SPELL_TYPE_DEFENSE      = 1
SPELL_TYPE_COMMON       = 2
SPELL_TYPE_POWERFUL     = 3
SPELL_TYPE_UNFORGIVABLE = 4

_INVALID_SPELL = ".@wizardduel@__spell_invalid__" #Internal usage only

##
## Spell class
##
class Spell:
    #Class special methods
    """
        speed       (int)   Speed of the spell. This will determine what spell is casted first.
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
    def __init__(self, speed: int, damage: int, succes_rate: int, description: str, type: int = SPELL_TYPE_COMMON):
        self.speed = speed
        self.damage = damage
        self.succes_rate = succes_rate
        self.description = description
        self.type = type

    def __repr__(self):
        return "\n\t{desc}\n\tSUCCES RATE: {srate}%\tSPEED: {speed}\tDAMAGE: {dmg}".format(type=type, desc=self.description, srate=self.succes_rate, speed=self.speed, dmg=self.damage)
    
    def chance_heal_partly_succes(self):
        return self.type == SPELL_TYPE_DEFENSE and CHANCE_HEAL_PARTLY > random.random() * 100
    
    def chance_heal_fully_succes(self):
        return self.type == SPELL_TYPE_DEFENSE and CHANCE_HEAL_FULLY > random.random() * 100
    
    def get_spell_name(self):
        return str(list(i for i in spells if spells[i] == self)).strip("[]'")
    
##
## Spells
##
spells = {
    # Useless spells - These don't do anything useful in combat
    "Lumos":                Spell(100, 000, 100, "Creates a small light at the tip of your wand", SPELL_TYPE_USELESS),
    "Nox":                  Spell(100, 000, 100, "Counter spell of Lumos", SPELL_TYPE_USELESS),
    "Rennervate":           Spell(100, 000, 100, "Revives your opponent if they are stunned", SPELL_TYPE_USELESS),
    "Igni":                 Spell(100, 000, 100, "Damages an enemy using fire. Except, this is a Witcher sign. It thus has no effect at all", SPELL_TYPE_USELESS),

# Defensive spell. Each cast from this category has a 5% chance of completely restoring health or 25% chance to heal 5% of maximum health
    "Finite Incantatem":    Spell(100, 000,  45,  "Cancel all effects casted upon you. If you are stunned/silenced, there's a 10% chance this spell might work", SPELL_TYPE_DEFENSE),
    "Impendimenta":         Spell(94, 000,  60,  "Slows your opponent. EFFECT: Decrease opponent's spell speed by 33% in their next offensive move", SPELL_TYPE_DEFENSE),
    "Lumos Solem":          Spell(94, 000,  60,  "Blinds your opponent. EFFECT: Decrease opponent's spell damage by 33% in their next offensive move", SPELL_TYPE_DEFENSE),
    "Protego":              Spell(100, 000,  80,  "Create a shield that blocks most attacks", SPELL_TYPE_DEFENSE),

# Common combat spells. High chance of succes, deals some damage
    "Reducto":              Spell(75, 150,  85,  "Blast an object near your opponent"),
    "Rictusempra":          Spell(85,  90,  90,  "Causes your opponent to curl up in laughter, tiring them out"),
    "Stupefy":              Spell(95,  75,  95,  "Knock over your opponent"),

# Powerful combat spells. Medium chance of succes, deals more damage or stuns opponents
    "Bombarda":             Spell(50, 180,  75,  "Creates an explosion near your opponent", SPELL_TYPE_POWERFUL),
    "Confringo":            Spell(50, 200,  70,  "Creates an explosion directly at your opponent", SPELL_TYPE_POWERFUL),
    "Mimblewimble":         Spell(50,  -1,  70,  "Ties a knot in your opponents tongue, causing them to be unable to cast a spell for 1 (more) move", SPELL_TYPE_POWERFUL),
    "Sectumsempra":         Spell(90, 400,  35,  "Slices your opponent", SPELL_TYPE_POWERFUL),
    "Silencio":             Spell(35,  -3,  55,  "Silences your opponent, causing them unable to cast spells for 3 moves. <!>Only works if opponent is not stunned yet", SPELL_TYPE_POWERFUL),

# Unforgivable spells. Very low chance of success, instantly kills or deals alot of damage/stun amount
    "Avada Kedavra":        Spell(999, 999,  2,  "Instantly end your opponent", SPELL_TYPE_UNFORGIVABLE),
    "Crucio":               Spell(999, 500,   5,  "Cause excruciating pain to your opponent, causing alot of damage and making them unable to cast spells for 5 moves", SPELL_TYPE_UNFORGIVABLE),
    "Imperio":              Spell(999,  -1,   3,  "Muddle with your opponent's mind, convincing them to stop casting spells for 10 moves", SPELL_TYPE_UNFORGIVABLE),

# Internal usage
    _INVALID_SPELL:        Spell(0, 0, 0, "(internal) invalid spell", SPELL_TYPE_NONE)
}

# Set succes rates to 100% if debug mode is enabled
if DEBUG_MODE:
    for i in spells.items():
        i[1].succes_rate = 100

##
## Standalone spell functions
##
def random_combat_spell():
    return random.choice([i for i in spells.items() if i[1].type == SPELL_TYPE_COMMON]) # note: returns tuple ('spell_name', spell_obj)

def find_spell_by_name(input: str): # Returns a multidimensional tuple: ( ('spell_name', spell_object), levenshtein_distance )
    ret = (input, spells.get(input.title(), spells[_INVALID_SPELL]))
    dist = 0
    if ret[1] == spells[_INVALID_SPELL]:
        ret = (_INVALID_SPELL, ret[1])
        if MAX_LEVENSHTEIN_DISTANCE > 0:
            for i in spells.items():
                dist = distance(i[0].title(), input.title())
                if dist <= MAX_LEVENSHTEIN_DISTANCE:
                    ret = (i[0], i[1])
                    break
    return (ret, dist)

def print_spells():
    header_spells_useless = "== USELESS SPELLS =="
    header_spells_defensive = "== DEFENSIVE SPELLS =="
    header_spells_common = "== COMMON COMBAT SPELLS =="
    header_spells_powerful = "== POWERFUL COMBAT SPELLS =="
    header_spells_unforgivable = "== UNFORGIVABLE CURSES =="

    for i in spells.items():
        if i[1].type == SPELL_TYPE_UNFORGIVABLE or i[1].type == SPELL_TYPE_USELESS or i[1].type == SPELL_TYPE_NONE:
            continue
        
        if i[1].type == SPELL_TYPE_USELESS and header_spells_useless:
            print("\n"+header_spells_useless)
            header_spells_useless = ""
        elif i[1].type == SPELL_TYPE_DEFENSE and header_spells_defensive:
            print("\n"+header_spells_defensive)
            header_spells_defensive = ""
        elif i[1].type == SPELL_TYPE_COMMON and header_spells_common:
            print("\n"+header_spells_common)
            header_spells_common = ""
        elif i[1].type == SPELL_TYPE_POWERFUL and header_spells_powerful:
            print("\n"+header_spells_powerful)
            header_spells_powerful = ""
        elif i[1].type == SPELL_TYPE_UNFORGIVABLE and header_spells_unforgivable:
            print("\n"+header_spells_unforgivable)
            header_spells_unforgivable = ""

        print(
            str(i)
              .strip('(')
              .strip(')')
              .replace(',', ':', 1)
        )   