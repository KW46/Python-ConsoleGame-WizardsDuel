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
def round_end(player1: Player, player2: Player):
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