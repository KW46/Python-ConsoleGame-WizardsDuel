WAND_CORE_UNICORN   = 0 #Succes +3%
WAND_CORE_PHOENIX   = 1 #Speed  +4%
WAND_CORE_DRAGON    = 2 #Damage +5%

WAND_WOOD_ASH       = 0 #Succes -3%
WAND_WOOD_ELDER     = 1 #Speed  -4%
WAND_WOOD_APPLE     = 2 #Damage -5%

class Wand:
    def __init__(self, wand_core: int, wand_wood: int) -> None:
        self.core: int          = wand_core
        self.wood: int          = wand_wood

        self.succes_rate: float = 1
        self.speed: float       = 1
        self.damage: float      = 1

        if self.core == WAND_CORE_UNICORN:
            self.succes_rate *= 1.03
        elif self.core == WAND_CORE_PHOENIX:
            self.speed *= 1.04
        elif self.core == WAND_CORE_DRAGON:
            self.damage *= 1.05

        if self.wood == WAND_WOOD_ASH:
            self.succes_rate *= 0.97
        elif self.wood == WAND_WOOD_ELDER:
            self.succes_rate *= 0.96
        elif self.wood == WAND_WOOD_APPLE:
            self.damage *= 0.95

    def __repr__(self) -> str:
        return"\t{wood} wand with core: {core}\n\t\t-- SPEED: {info_speed}\tDAMAGE: {info_dmg}\tSUCCES RATE: {info_srate}".format(
            wood=self.get_wand_wood(), core=self.get_wand_core(), info_srate=round(self.succes_rate, 2), info_speed=self.speed, info_dmg=round(self.damage, 2)
        )
    
    def get_wand_core(self) -> str:
        if self.core == WAND_CORE_UNICORN: return "Unicorn hair"
        elif self.core == WAND_CORE_PHOENIX: return "Phoenix feather"
        elif self.core == WAND_CORE_DRAGON: return "Dragon heartstring"
        else: return "Muggle's electric wire"
    
    def get_wand_wood(self) -> str:
        if self.wood == WAND_WOOD_ASH: return "Ash"
        elif self.wood == WAND_WOOD_ELDER: return "Elder"
        elif self.wood == WAND_WOOD_APPLE: return "Apple"
        else: return "Common wood"

##
## Wands
##
wands = {
    1:  Wand(WAND_CORE_UNICORN, WAND_WOOD_ASH),
    2:  Wand(WAND_CORE_UNICORN, WAND_WOOD_ELDER),
    3:  Wand(WAND_CORE_UNICORN, WAND_WOOD_APPLE),

    4:  Wand(WAND_CORE_PHOENIX, WAND_WOOD_ASH),
    5:  Wand(WAND_CORE_PHOENIX, WAND_WOOD_ELDER),
    6:  Wand(WAND_CORE_PHOENIX, WAND_WOOD_APPLE),

    7:  Wand(WAND_CORE_DRAGON, WAND_WOOD_ASH),
    8:  Wand(WAND_CORE_DRAGON, WAND_WOOD_ELDER),
    9:  Wand(WAND_CORE_DRAGON, WAND_WOOD_APPLE)
}