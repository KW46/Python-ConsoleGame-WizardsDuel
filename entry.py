from game import intro_message_welcome, intro_get_username, intro_print_wands, intro_get_wand, intro_message_duel_start
from game import round_get_player_spells, round_set_player_spells_succes, round_get_player_spells_speed, round_cast_spells, start_round
from player import Player

current_round = 0

intro_message_welcome()

player1 = Player(None, None)
player2 = Player(None, None)

player1.name = intro_get_username(1)
player2.name = intro_get_username(2)

print("Welcome {p1_name} and {p2_name}! You're about to choose a wand to use in this duel! Available wands are:".format(p1_name=player1.name, p2_name=player2.name))
intro_print_wands()
player1.wand = intro_get_wand(player1)
player2.wand = intro_get_wand(player2)
print()
print("{name} will be fighting with an {wood} wand with a {core} core".format(name=player1.name, wood=player1.wand.get_wand_wood().lower(), core=player1.wand.get_wand_core().lower()))
print("{name} will be fighting with an {wood} wand with a {core} core".format(name=player2.name, wood=player2.wand.get_wand_wood().lower(), core=player2.wand.get_wand_core().lower()))

intro_message_duel_start()

try:
    while True:
        if player1.health == 0:
            print("END! {name} has been defeated. Congratulations {name2}!".format(name=player1.name, name2=player2.name))
            break
        elif player2.health == 0:
            print("END! {name} has been defeated. Congratulations {name2}!".format(name=player2.name, name2=player1.name))
            break

        current_round += 1
        start_round(current_round, player1, player2)

        round_get_player_spells(player1, player2)
        round_set_player_spells_succes(player1, player2)
        if not player1.active_spell_succes and not player2.active_spell_succes:
            continue
        if not player1.active_spell_succes and player2.active_spell_succes:
            player2.cast_spell(player1)
            continue
        elif player1.active_spell_succes and not player2.active_spell_succes:
            player1.cast_spell(player2)
            continue    
        
        fastest_caster, slowest_caster = round_get_player_spells_speed(player1, player2)
        round_cast_spells(fastest_caster, slowest_caster)

except KeyboardInterrupt:
    print()
    print("<!> Duel ended because both {} and {} suddenly decided to test out their apparition skill!".format(player1.name, player2.name))            