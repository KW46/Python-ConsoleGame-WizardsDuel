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

current_round = 1
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
        
        # INPUT: Player 1

        # INPUT: Player 2

        # OUTCOME: SPELLS
        #   > Get spell succes
        #   > Add health if defensive spell was lucky (partial heal, fully heal)
        #   > Determine instant winner or skip to next round
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