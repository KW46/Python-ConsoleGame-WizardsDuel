from random import random
from Levenshtein import distance

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
    
##
## Spells
##
# Useless spells - These don't do anything useful in combat
spell_lumos             =   Spell("Lumos",              100, 000, 100, "Creates a small light at the tip of your wand", SPELL_TYPE_USELESS)
spell_nox               =   Spell("Nox",                100, 000, 100, "Counter spell of Lumos", SPELL_TYPE_USELESS)
spell_rennervate        =   Spell("Rennervate",         100, 000, 100, "Revives your opponent if they are stunned", SPELL_TYPE_USELESS)
spell_igni              =   Spell("Igno",               100, 000, 100, "Damages an enemy using fire. Except, this is a Witcher sign. It thus has no effect at all", SPELL_TYPE_USELESS)

# Defensive spell. Each cast from this category has a 5% chance of completely restoring health or 25% chance to heal 5% of maximum health
spell_finite_incantatem =   Spell("Finite Incantatem",  100, 000,  45,  "Cancel all effects casted upon you. If you are stunned/silenced, there's a 10% chance this spell might work", SPELL_TYPE_DEFENSE)
spell_impendimenta      =   Spell("Impendimenta",       100, 000,  60,  "Slows your opponent. EFFECT: Decrease opponent's spell speed by 33% in their next offensive move", SPELL_TYPE_DEFENSE)
spell_lumos_solem       =   Spell("Lumos Solem",        100, 000,  60,  "Blinds your opponent. EFFECT: Decrease opponent's spell damage by 33% in their next offensive move", SPELL_TYPE_DEFENSE)
spell_protego           =   Spell("Protego",            100, 000,  95,  "Create a shield that blocks most attacks", SPELL_TYPE_DEFENSE)

# Common combat spells. High chance of succes, deals some damage
spell_reducto           =   Spell("Reduto",              75, 150,  75,  "Blast an object near your opponent")
spell_rictusempra       =   Spell("Rictusempra",         85,  90,  90,  "Causes your opponent to curl up in laughter, making them tired")
spell_stupefy           =   Spell("Stupefy",             95,  75,  95,  "Knock over your opponent")

# Powerful combat spells. Medium chance of succes, deals more damage or stuns opponents
spelll_bombarda         =   Spell("Bombarda",            50, 180,  65,  "Creates an explosion near your opponent", SPELL_TYPE_POWERFUL)
spell_confringo         =   Spell("Confringo",           50, 200,  55,  "Creates an explosion directly at your opponent", SPELL_TYPE_POWERFUL)
spell_mimblewimble      =   Spell("Mimblewimble",        50,  -1,  45,  "Ties a knot in your opponents tongue, causing them to be unable to cast a spell for 1 move", SPELL_TYPE_POWERFUL)
spell_sectusempra       =   Spell("Sectusempra",         90, 400,  40,  "Slices your opponent", SPELL_TYPE_POWERFUL)
spell_silencio          =   Spell("Silencio",            35,  -3,  20,  "Silences your opponent, causing them unable to cast spells for 3 moves", SPELL_TYPE_POWERFUL)

# Unforgivable spells. Very low chance of success, instantly kills or deals alot of damage/stun amount
spell_avada_kedavra     =   Spell("Avada Kedavra",      100, 9999,  2,  "Instantly end your opponent", SPELL_TYPE_UNFORGIVABLE)
spell_crucio            =   Spell("Crucio",             100, 500,   5,  "Cause excruciating pain to your opponent, causing alot of damage and making them unable to cast spells for 5 moves", SPELL_TYPE_UNFORGIVABLE)
spell_imperio           =   Spell("Imperio",            100,  -1,   3,  "Muddle with your opponent's mind, convincing them to stop casting spells for 10 moves", SPELL_TYPE_UNFORGIVABLE)

# spell_none, used as a fallback if an invalid spell was cast ('no object'.method/attribute)
spell_none = Spell(__INVALID_SPELL, 0, 0, 0, "(internal) invalid spell", SPELL_TYPE_USELESS)

##
## Standalone spell functions
##
def find_spell_by_name(input: str):
    for i in Spell.spellList:
        if input.title() == i.name.title():
            return i
    return spell_none

def print_spells():
    header_spells_useless = "== USELESS SPELLS =="
    header_spells_defensive = "== DEFENSIVE SPELLS =="
    header_spells_common = "== COMMON COMBAT SPELLS =="
    header_spells_powerful = "== POWERFUL COMBAT SPELLS =="
    header_spells_unforgivable = "== UNFORGIVABLE CURSES =="

    for i in Spell.spellList:
        if i.type == SPELL_TYPE_UNFORGIVABLE or i.type == SPELL_TYPE_USELESS:
            continue
        
        if i.type == SPELL_TYPE_USELESS and header_spells_useless:
            print("\n"+header_spells_useless)
            header_spells_useless = ""
        elif i.type == SPELL_TYPE_DEFENSE and header_spells_defensive:
            print("\n"+header_spells_defensive)
            header_spells_defensive = ""
        elif i.type == SPELL_TYPE_COMMON and header_spells_common:
            print("\n"+header_spells_common)
            header_spells_common = ""
        elif i.type == SPELL_TYPE_POWERFUL and header_spells_powerful:
            print("\n"+header_spells_powerful)
            header_spells_powerful = ""
        elif i.type == SPELL_TYPE_UNFORGIVABLE and header_spells_unforgivable:
            print("\n"+header_spells_unforgivable)
            header_spells_unforgivable = ""

        print(i)