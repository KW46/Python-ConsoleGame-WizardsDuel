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