import random
from player import Player
from wands import wands
from spells import Spell, spells, random_combat_spell, print_spells, find_spell_by_name
from spells import _INVALID_SPELL, SPELL_TYPE_COMMON, SPELL_TYPE_POWERFUL
from game_config import MIN_USERNAME_LEN, MAX_PLAYER_HEALTH

INPUT_MESSAGES = (
    "{name}, what's your spell? ",
    "{name}, how will you obliviate your opponent? ",
    "{name}, go for it! Enter a spell! ",
    "{name}, hit me with your best spell: ",
    "{name}, go time! ",
    "{name}, it's your turn to enter a spell: "
)

##
## Intro functions
##
def intro_message_welcome() -> None:
    print()
    print("Welcome! You're about to perform a wizard duel!")
    print("After joining in, you have to select a wand. Your wand will affect the power of your spells. Spells have three atrributes that modify the power of spells:")
    print("1- DAMAGE: Damage can either deal damage to health points, or it can stun your a player for X amount of moves (DAMAGE below zero = amount of moves a player is stunned)")
    print("2- SUCCES CHANCE: How much succes chance of performing a spell. Some spells are difficult to pronounce and thus could fail..")
    print("3- SPEED: If both players succesfully cast a spell, the spell with the greatest speed will succeed and the other one will not")
    print()

def intro_message_duel_start() -> None:
    print("<!> If you need a list of available spells, enter: help (this will not take away a move)")
    print("<!> If you need information of a specific spell, enter: help SPELL_NAME")
    print("<!> You can press enter (without typing a spell) to cast a random basic combat spell")
    print()
    print("Alright! Time to duel!")

def intro_get_username(playerid: int) -> str:
    while True:
        user_input = input("Player {id} - What's your name? ".format(id=playerid))

        if len(user_input) < MIN_USERNAME_LEN:
            print("<!> Oops! Names must be at least {len} characters long!".format(len=MIN_USERNAME_LEN))
        else: break
    
    return user_input

def intro_print_wands() -> None:
    for i in wands.items():
        print("{wand_id}:{wand_desc}".format(wand_id=i[0], wand_desc=i[1]))

def intro_get_wand(player: Player) -> Spell:
    while (True):
        try:
            user_input = int(input("What wand do you want {name}? (Enter one of the numbers): ".format(name=player.name)))
        except ValueError:
            continue
        if user_input < 1 or user_input > len(wands):
            continue
        break

    return wands[user_input]

##
## Game round functions
##
def start_round(round: int, player1: Player, player2: Player) -> None:
    if (player1.stunned_rounds > 0): player1.stunned_rounds -= 1
    if (player2.stunned_rounds > 0): player2.stunned_rounds -= 1    

    print()
    print("== Round {round} ==".format(round=round))
    print("-- Current stats:\n\
          - {p1_name}: Health: {p1_hp} | Queued effects: {p1_effects} | Round being stunned: {p1_stunned}\n\
          - {p2_name}: Health: {p2_hp} | Queued effects: {p2_effects} | Rounds being stunned: {p2_stunned}".format(
              round=round,
              p1_name=player1.name, p1_hp=player1.health, p1_effects=player1.get_queued_effects(), p1_stunned=player1.stunned_rounds,
              p2_name=player2.name, p2_hp=player2.health, p2_effects=player2.get_queued_effects(), p2_stunned=player2.stunned_rounds
          )
    )

def print_turn_message(player: Player) -> None:
    return random.choice(INPUT_MESSAGES).format(name=player.name)

def get_player_spell_from_input(player: Player) -> tuple:
    while True:
        player_input = input(print_turn_message(player))

        if not player_input:
            spell_name, spell_obj = random_combat_spell()
            return ((spell_name, spell_obj), 0)
        
        if player_input == "help":
            print_spells()
            continue
        elif player_input.find("help", 0) != -1:
            spell_name, spell_obj = find_spell_by_name(player_input[5:])[0]
            if spell_obj is spells[_INVALID_SPELL]:
                print("<!> Spell '{what}' does not exist!".format(what=player_input))
            else:
                print("'{spell_name}':{spell_desc}".format(spell_name=spell_name, spell_desc=spell_obj))
        else:
            return find_spell_by_name(player_input)
        
def round_get_player_spells(player1: Player, player2: Player) -> None:
    spell, dist = get_player_spell_from_input(player1)
    player1.active_spell = spells.get(spell[0])
    player1.active_spell_levenshtein_distance = dist

    spell, dist = get_player_spell_from_input(player2)
    player2.active_spell = spells.get(spell[0])
    player2.active_spell_levenshtein_distance = dist

    if (player1.stunned_rounds > 0 and player1.active_spell is not spells["Finite Incantatem"]):
        player1.active_spell = None
    if (player2.stunned_rounds > 0 and player2.active_spell is not spells["Finite Incantatem"]):
        player2.active_spell = None    

def round_set_player_spells_succes(player1: Player, player2: Player) -> None:
    player1.active_spell_succes = player1.get_spell_succes_rate(player1.active_spell) > random.random() * 100
    player2.active_spell_succes = player2.get_spell_succes_rate(player2.active_spell) > random.random() * 100
    print(player1.cast_spell_result(player1.active_spell, player1.active_spell_succes))
    print(player2.cast_spell_result(player2.active_spell, player2.active_spell_succes))

    if player1.active_spell_succes and player1.active_spell.chance_heal_partly_succes():
        player1.give_health(MAX_PLAYER_HEALTH * 0.05)
        print("<!> {name} casted {spell} above expectations, and receives {hp} health!".format(name=player1.name, spell=player1.active_spell.get_spell_name(), hp=MAX_PLAYER_HEALTH*0.05))
    elif player1.active_spell_succes and player1.active_spell.chance_heal_fully_succes() and player1.health < MAX_PLAYER_HEALTH:
        player1.give_health(MAX_PLAYER_HEALTH)
        print("<!> {name} casted {spell} outstanding! {name} now has full health!".format(name=player1.name, spell=player1.active_spell.get_spell_name(), hp=MAX_PLAYER_HEALTH*0.05))
    #
    if player2.active_spell_succes and player2.active_spell.chance_heal_partly_succes():
        player2.give_health(MAX_PLAYER_HEALTH * 0.05)
        print("<!> {name} casted {spell} above expectations, and receives {hp} health!".format(name=player2.name, spell=player2.active_spell.get_spell_name(), hp=MAX_PLAYER_HEALTH*0.05))
    elif player2.active_spell_succes and player2.active_spell.chance_heal_fully_succes() and player2.health < MAX_PLAYER_HEALTH:
        player2.give_health(MAX_PLAYER_HEALTH)
        print("<!> {name} casted {spell} outstanding! {name} now has full health!".format(name=player2.name, spell=player2.active_spell.get_spell_name(), hp=MAX_PLAYER_HEALTH*0.05))            

def round_get_player_spells_speed(player1: Player, player2: Player) -> tuple:
    player1.active_spell_speed = player1.active_spell.speed * player1.wand.speed
    player2.active_spell_speed = player2.active_spell.speed * player2.wand.speed

    if player1.decreased_spell_speed and (player1.active_spell.type == SPELL_TYPE_COMMON or player1.active_spell.type == SPELL_TYPE_POWERFUL):
        print("<!> {name} is slowed, spell speed decreased by 33%!".format(name=player1.name))
        player1.active_spell_speed *= 0.67
        player1.decreased_spell_speed = False
    if player2.decreased_spell_speed and (player2.active_spell.type == SPELL_TYPE_COMMON or player2.active_spell.type == SPELL_TYPE_POWERFUL):
        print("<!> {name} is slowed, spell speed decreased by 33%!".format(name=player2.name))
        player2.active_spell_speed *= 0.67
        player2.decreased_spell_speed = False

    if player1.decreased_spell_damage and (player1.active_spell.type == SPELL_TYPE_COMMON or player1.active_spell.type == SPELL_TYPE_POWERFUL):
        print("<!> {name} is blinded, spell damage decreased by 33%!".format(name=player1.name))
    if player2.decreased_spell_damage and (player2.active_spell.type == SPELL_TYPE_COMMON or player2.active_spell.type == SPELL_TYPE_POWERFUL):
        print("<!> {name} is blinded, spell damage decreased by 33%!".format(name=player2.name))       

    fastest_caster = player1
    slowest_caster = player2
    if player2.active_spell_speed > player1.active_spell_speed:
        fastest_caster = player2
        slowest_caster = player1

    print("- {p1_name}'s spell speed is {p1_spd}. {p2_name}'s spell speed is {p2_spd}. {fastest} is the fastest caster this round!".format(
        p1_name=player1.name, p1_spd=player1.active_spell_speed,
        p2_name=player2.name, p2_spd=player2.active_spell_speed,
        fastest=fastest_caster.name
    ))

    return (fastest_caster, slowest_caster)

def round_cast_spells(player1: Player, player2: Player) -> None:
    player1.cast_spell(player2)
    if player2.health > 0:
        player2.cast_spell(player1)