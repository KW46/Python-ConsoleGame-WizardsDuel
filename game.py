from player import *
from spells import *
from wands import *

##
## Definitions
##
input_messages = (
    "{name}, what's your spell? ",
    "{name}, how will you obliviate your opponent? ",
    "{name}, go for it! Enter a spell! ",
    "{name}, hit me with your best spell: ",
    "{name}, go time! ",
    "{name}, it's your turn to enter a spell: "
)
def print_turn_message(player: Player):
    return random.choice(input_messages).format(name=player.name)

current_round = 0
def round_end():
    if (player1.stunned_rounds > 0): player1.stunned_rounds -= 1
    if (player2.stunned_rounds > 0): player2.stunned_rounds -= 1

    print("<!> Round {round} ended! Current stats:\n\
          - {p1_name}: Health: {p1_hp} | Queued effects: {p1_effects} | Round being stunned: {p1_stunned}\n\
          - {p2_name}: Health: {p2_hp} | Queued effects: {p2_effects} | Rounds being stunned: {p2_stunned}".format(
              round=current_round,
              p1_name=player1.name, p1_hp=player1.health, p1_effects=player1.get_queued_effects(), p1_stunned=player1.stunned_rounds,
              p2_name=player2.name, p2_hp=player2.health, p2_effects=player2.get_queued_effects(), p2_stunned=player2.stunned_rounds
          )
    )

def get_player_spell_from_input(player: Player):
    while True:
        player_input = input(print_turn_message(player))

        if not player_input:
            return [random_combat_spell(), 0]
        else:
            if player_input == "help":
                print_spells()
                continue
            elif player_input.find("help", 0) != -1:
                find_what = player_input[5:]
                spell = find_spell_by_name(find_what)

                if spell == spell_none:
                    print("<!> Spell '{what}' does not exist!".format(what=find_what))
                else:
                    print(spell)
                continue
            else:
                return find_spell_by_name(player_input)

##
## ENTRY
##
print()
print("Welcome! You're about to perform a wizard duel!")
print("After joining in, you have to select a wand. Your wand will affect the power of your spells. Spells have three atrributes that modify the power of spells:")
print("1- DAMAGE: Damage can either deal damage to health points, or it can stun your a player for X amount of moves (DAMAGE below zero = amount of moves a player is stunned)")
print("2- SUCCES CHANCE: How much succes chance of performing a spell. Some spells are difficult to pronounce and thus could fail..")
print("3- SPEED: If both players succesfully cast a spell, the spell with the greatest speed will succeed and the other one will not")
print()
#GET: USERNAMES
while True:
    player1_name = input("Player 1 - What's your name? ")
    player2_name = input("And now player 2 - What's your name? ")

    if len(player1_name) < 2 or len(player2_name) < 2:
        print("<!> Oops! Names must be at least 2 characters long! Please try again")
    else: break

#GET: WANDS
print("Welcome {p1_name} and {p2_name}! You're about to choose a wand to use in this duel! Available wands are:".format(p1_name=player1_name, p2_name=player2_name))
for i in Wand.wandList:
    print(i)

#Player 1
while (True):
    try:
        wand_input = int(input("What wand do you want {name}? (Enter one of the numbers): ".format(name=player1_name)))
    except ValueError:
        continue
    if wand_input < 1 or wand_input > len(Wand.wandList):
        continue

    player1_wand = Wand.wandList[wand_input-1]
    break
#Player 2
while (True):
    try:
        wand_input = int(input("What wand do you want {name}? (Enter one of the numbers): ".format(name=player2_name)))
    except ValueError:
        continue
    if wand_input < 1 or wand_input > len(Wand.wandList):
        continue

    player2_wand = Wand.wandList[wand_input-1]
    break

player1 = Player(player1_name, player1_wand)
player2 = Player(player2_name, player2_wand)

print()
print("{name} will be fighting with an {wood} wand with a {core} core".format(name=player1.name, wood=player1.wand.get_wand_wood().lower(), core=player1.wand.get_wand_core().lower()))
print("{name} will be fighting with an {wood} wand with a {core} core".format(name=player2.name, wood=player2.wand.get_wand_wood().lower(), core=player2.wand.get_wand_core().lower()))
print("<!> If you need a list of available spells, enter: help (this will not take away a move)")
print("<!> If you need information of a specific spell, enter: help SPELL_NAME")
print("<!> You can press enter (without typing a spell) to cast a random basic combat spell")
print()
print("Alright! Time to duel!")

game_running = True
try:
    while (game_running):
        current_round += 1
        if (current_round != 1):
            # Weird, right? To have round_end() at the start of a round.
            # There will be multiple conditions where the current iteration will end.
            # I'm lazy, hence why it's here :-)
            round_end() 
        
        print("== Round {round} ==".format(round=current_round))
        player1_spell, player1_spell_levenshtein_distance = get_player_spell_from_input(player1)
        player2_spell, player2_spell_levenshtein_distance = get_player_spell_from_input(player2)

        # OUTCOME: SPELLS
        #   > Get spell succes
        player1_spell_succes = player1.get_spell_succes_rate(player1_spell) > random.random() * 100
        player2_spell_succes = player2.get_spell_succes_rate(player2_spell) > random.random() * 100

        print(player1.cast_spell_result(player1_spell, player1_spell_succes))
        print(player2.cast_spell_result(player2_spell, player2_spell_succes))

        #   > Add health if defensive spell was lucky (partial heal, fully heal)
        if player1_spell_succes and player1_spell.chance_heal_partly_succes():
            player1.give_health(MAX_PLAYER_HEALTH * 0.05)
            print("<!> {name} casted {spell} above expectations, and receives {hp} health!".format(name=player1.name, spell=player1_spell.name, hp=MAX_PLAYER_HEALTH*0.05))
        elif player1_spell_succes and player1_spell.chance_heal_fully_succes() and player1.health < MAX_PLAYER_HEALTH:
            player1.give_health(MAX_PLAYER_HEALTH)
            print("<!> {name} casted {spell} outstanding! {name} now has full health!".format(name=player1.name, spell=player1_spell.name, hp=MAX_PLAYER_HEALTH*0.05))
        #
        if player2_spell_succes and player2_spell.chance_heal_partly_succes():
            player2.give_health(MAX_PLAYER_HEALTH * 0.05)
            print("<!> {name} casted {spell} above expectations, and receives {hp} health!".format(name=player2.name, spell=player2_spell.name, hp=MAX_PLAYER_HEALTH*0.05))
        elif player2_spell_succes and player2_spell.chance_heal_fully_succes() and player2.health < MAX_PLAYER_HEALTH:
            player2.give_health(MAX_PLAYER_HEALTH)
            print("<!> {name} casted {spell} outstanding! {name} now has full health!".format(name=player2.name, spell=player2_spell.name, hp=MAX_PLAYER_HEALTH*0.05))            

        #   > Determine instant winner or skip to next round
        if not player1_spell_succes and not player2_spell_succes:
            continue
        if not player1_spell_succes and player2_spell_succes:
            player2.cast_spell(player2_spell, player1)
            pass
        elif player1_spell_succes and not player2_spell_succes:
            player1.cast_spell(player1_spell, player2)
            pass

        #   > Determine fastest spell
        #       <!> Spells with speed 100 will always be casted
        #   > Determine priority
        #       1. Unforgivables
        #       2. Protego 
        #       3. (fastest_spell)
        #       4. (other_player)
        
        # CAST SPELLS
        #   >

except KeyboardInterrupt:
    print()
    print("<!> Duel ended because both {} and {} suddenly decided to test out their apparition skill!".format(player1.name, player2.name))