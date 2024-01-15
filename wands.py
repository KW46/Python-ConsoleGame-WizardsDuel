WAND_CORE_UNICORN   = 0 #Succes +3%
WAND_CORE_PHOENIX   = 1 #Speed  +4%
WAND_CORE_DRAGON    = 2 #Damage +5%

WAND_WOOD_ASH       = 0 #Succes -3%
WAND_WOOD_ELDER     = 1 #Speed  -4%
WAND_WOOD_APPLE     = 2 #Damage -5%

class Wand:
    _next_wand_id = 1
    wandList = []

    def __init__(self, wand_core: int, wand_wood: int):
        self.id = Wand._next_wand_id

        self.core = wand_core
        self.wood = wand_wood

        self.succes_rate = 1
        self.speed = 1
        self.damage = 1

        if self.core == WAND_CORE_UNICORN:
            self.succes_rate *= 1.03
        elif self.core == WAND_CORE_PHOENIX:
            self.speed *= 1.04
        elif self.core == WAND_CORE_DRAGON:
            self.speed *= 1.05

        if self.wood == WAND_WOOD_ASH:
            self.succes_rate *= 0.97
        elif self.wood == WAND_WOOD_ELDER:
            self.succes_rate *= 0.96
        elif self.wood == WAND_WOOD_APPLE:
            self.damage *= 0.95

        Wand.wandList.append(self)
        Wand._next_wand_id += 1

    def __repr__(self):
        return"\t{id}: {wood} wand with core: {core}\n\t\t-- SPEED: {info_speed}\tDAMAGE: {info_dmg}\tSUCCES RATE: {info_srate}".format(
            id=self.id, wood=self.get_wand_wood(), core=self.get_wand_core(), info_srate=round(self.succes_rate, 2), info_speed=self.speed, info_dmg=self.damage
        )
    
    def get_wand_core(self):
        if self.core == WAND_CORE_UNICORN: return "Unicorn hair"
        elif self.core == WAND_CORE_PHOENIX: return "Phoenix feather"
        elif self.core == WAND_CORE_DRAGON: return "Dragon heartstring"
        else: return "Muggle's electric wire"
    
    def get_wand_wood(self):
        if self.wood == WAND_WOOD_ASH: return "Ash"
        elif self.wood == WAND_WOOD_ELDER: return "Elder"
        elif self.wood == WAND_WOOD_APPLE: return "Apple"
        else: return "Common wood"

##
## Wands
##
wand_1 = Wand(WAND_CORE_UNICORN, WAND_WOOD_ASH)
wand_2 = Wand(WAND_CORE_UNICORN, WAND_WOOD_ELDER)
wand_3 = Wand(WAND_CORE_UNICORN, WAND_WOOD_APPLE)

wand_4 = Wand(WAND_CORE_PHOENIX, WAND_WOOD_ASH)
wand_5 = Wand(WAND_CORE_PHOENIX, WAND_WOOD_ELDER)
wand_6 = Wand(WAND_CORE_PHOENIX, WAND_WOOD_APPLE)

wand_7 = Wand(WAND_CORE_DRAGON, WAND_WOOD_ASH)
wand_8 = Wand(WAND_CORE_DRAGON, WAND_WOOD_ELDER)
wand_9 = Wand(WAND_CORE_DRAGON, WAND_WOOD_APPLE)        