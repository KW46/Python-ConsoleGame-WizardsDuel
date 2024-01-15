from wands import Wand
from spells import *

MAX_PLAYER_HEALTH = 1000

class Player:
    def __init__(self, name: str, wand: Wand):
        self.name = name
        self.health = MAX_PLAYER_HEALTH
        self.wand = wand
        self.active_spell = spell_none
        self.active_spell_levenshtein_distance = 0 # Penalty => If >0 then damage reduction, 15% per distance

        self.stunned_rounds = 0
        self.decreased_spell_speed = False
        self.decreased_spell_damage = False

        self.lumos = False

    def give_health(self, health: int):
        self.health += health
        if self.health > MAX_PLAYER_HEALTH:
            self.health = MAX_PLAYER_HEALTH
        return self.health

    def take_health(self, health: int):
        self.health -= health
        if self.health < 0:
            self.health = 0
        return self.health
    
    def get_spell_succes_rate(self, spell: Spell):
        return 1 * self.wand.succes_rate * spell.succes_rate
    
    def get_queued_effects(self):
        output = ""
        effect_slowed = "Slowed"
        effect_blinded = "Blinded"

        if self.decreased_spell_speed:
            output = effect_slowed
        if self.decreased_spell_damage:
            if not output:
                output = effect_blinded
            else: output += ", " + effect_blinded
        
        if not output: output = "None"
        return output

    def cast_spell_result(self, spell: Spell, succes: bool):
        if succes:
            message = "{name} casted '{spell}' with succes"
        else:
            if spell.type == SPELL_TYPE_UNFORGIVABLE:
                message = "{name} tried to cast '{spell}' but didn't truly mean it. Cast FAILED!"
            elif spell.type == SPELL_TYPE_USELESS:
                return "{name} must not be feeling well, since they casted a non existing spell. Cast FAILED!".format(name=self.name)
            else: message = "{name} tried to cast '{spell}' but mispronounced it. Cast FAILED!"
        return message.format(name=self.name, spell=spell.name)
    
    def cast_spell(self, opponent): #: Player ?
        spell_name = self.active_spell.name.lower()

        if self.active_spell == spell_none:
            print("- {name} does nothing".format(name=self.name))
            return
        
        if self.stunned_rounds > 0 and self.active_spell != spell_finite_incantatem:
            print("<!> {name} tries to cast a spell but fails because they are stunned!".format(name=self.name))
            return

        if self.active_spell.type == SPELL_TYPE_USELESS:
            if self.active_spell == spell_lumos:
                if self.lumos:
                    print("- {name} casts {spell} with no effect: {name} already has a brutal shining light at the tip of their wand!".format(name=self.name, spell=spell_name))
                else:
                    print("- {name} casts {spell}! Look at that brutal shining light at the tip of their wand. Absolutely gorgeous!".format(name=self.name, spell=spell_name))
                    self.lumos = True
            elif self.active_spell == spell_nox:
                if not self.lumos:
                    print("- {name} shouts: {spell}! Nothing happened".format(name=self.name, spell=spell_name.upper()))
                else:
                    print("- {name} shouts {spell}! Their brutal shining light dissapears".format(name=self.name, spell=spell_name.upper()))
                    self.lumos = False
            elif self.active_spell == spell_rennervate:
                if opponent.stunned_rounds == 0:
                    print("- {name} casts {spell} with no effect, because {name_o} is not currently stunned!".format(name=self.name, spell=spell_name, name_o=opponent.name))
                else:
                    print("- {name} casts {spell}! {name_o} is no longer stunned!".format(name=self.name, spell=spell_name, name_o=opponent.name))
                    opponent.stunned_rounds = 0
            elif self.active_spell == spell_igni:
                print("- Geralt casts Igni. Wait. Geralt? White Wolf? The butcher of Blaviken? What is he doing here? Is he even here? What is going on?")
            else:
                print("<!> [debug]{name} casted SPELL_TYPE_USELESS {spell}. Behaviour unscripted!".format(name=self.name, spell=spell_name))                
        
        elif self.active_spell.type == SPELL_TYPE_DEFENSE:
            spell_succes = True
            if self.active_spell == spell_finite_incantatem:
                if self.stunned_rounds > 0:
                    if not 10 > random.random() * 100:
                        spell_succes = False
                    else:
                        print("- {name} got lucky! Attempting to cast {spell} broke the silence!".format(name=self.name, spell=spell_name))
            
                if spell_succes and (self.decreased_spell_damage or self.decreased_spell_speed):
                    print("- {name} casts {spell} and removes queued effects!".format(name=self.name, spell=spell_name))
                    self.decreased_spell_damage = False
                    self.decreased_spell_speed = False
                elif spell_succes and not self.decreased_spell_damage and not self.decreased_spell_speed:
                    if self.stunned_rounds > 0:
                        self.stunned_rounds = 0
                    else:
                        print("- {name} casts {spell}. {name_o} is looking confused. What spell did {name} try to cancel?".format(name=self.name, spell=spell_name, name_o=opponent.name))
                elif not spell_succes:
                    print("- {name}: (nothing, still stunned)".format(name=self.name))
            elif self.active_spell == spell_impendimenta:
                if opponent.active_spell != spell_protego:
                    print("- {name} casts {spell} on {name_o}. {name_o} is slowed and their next offensive move will have a 33% slower spell speed!".format(name=self.name, name_o=opponent.name, spell=spell_name))
                    opponent.decreased_spell_speed = True
                else:
                    print("- {name} casts {spell} on {name_o}. FAILURE! {name_o} blocks the attack!".format(name=self.name, name_o=opponent.name, spell=spell_name))
            elif self.active_spell == spell_lumos_solem:
                # Light still goes through the shield, therefor always succeed blinding attempts
                print("- {name} casts {spell} on {name_o}. {name_o} is blinded and their next offensive move will have 33% less damage!".format(name=self.name, name_o=opponent.name, spell=spell_name))
                opponent.decreased_spell_damage = True
            elif self.active_spell == spell_protego:
                print("- {name} casts {spell}".format(name=self.name, spell=spell_name))
            else:
                print("<!> [debug]{name} casted SPELL_TYPE_DEFENSE {spell}. Behaviour unscripted!".format(name=self.name, spell=spell_name))

        elif self.active_spell.type == SPELL_TYPE_UNFORGIVABLE:
            if self.active_spell == spell_avada_kedavra:
                print("- THE NERVE! {name} casts the killing curse! See you in the after life {name_o}!".format(name=self.name, name_o=opponent.name))
                opponent.health = 0
            elif self.active_spell == spell_crucio:
                print("- THE NERVE! {name} casts the torture curse. {name_o} is greatly hurt and falls to the ground. They are stunned for 5 (more) moves".format(name=self.name, name_o=opponent.name))
                opponent.stunned_rounds += 5
            elif self.active_spell == spell_imperio:
                print("- THE NERVE! {name} casts the Imperius curse. \"Why don't you take a nice nap for 10 moves, {name_o}?\". {name_o} submits with pleasure".format(name=self.name, name_o=opponent.name))
                opponent.stunned_rounds = 10

        else:
            if self.active_spell == spell_mimblewimble:
                if opponent.active_spell != spell_protego:
                    print("- {name} casts {spell} on {name_o}. {name_o}'s tongue is tied in a knot. That's annoying! {name_o} is silenced for 1 (more) move".format(name=self.name, spell=spell_name, name_o=opponent.name))
                else:
                    print("- {name} casts {spell} on {name_o}. FAILURE! {name_o} blocks the attack!".format(name=self.name, spell=spell_name, name_o=opponent.name))
            elif self.active_spell == spell_silencio:
                if opponent.active_spell != spell_protego:
                    if opponent.stunned_rounds == 0:
                        print("- {name} casts {spell} on {name_o}. SUCCES! {name_o} is silenced for 3 (more) moves".format(name=self.name, spell=spell_name, name_o=opponent.name))
                        opponent.stunned_rounds += 3
                    else:
                        print("- {name} casts {spell} on {name_o}. FAILURE! {name_o} is already silenced!".format(name=self.name, spell=spell_name, name_o=opponent.name))
                else:
                    print("- {name} casts {spell} on {name_o}. FAILURE! {name_o} blocks the attack!".format(name=self.name, spell=spell_name, name_o=opponent.name))
            else:
                damage_penalty = self.active_spell_levenshtein_distance * 15
                if damage_penalty != 0: print("<!> {name} was unclear in their pronunciation and receives a damage penalty of {damage_penalty}".format(name=self.name, damage_penalty=damage_penalty))

                total_damage = self.active_spell.damage * self.wand.damage - damage_penalty
                if total_damage < 0: total_damage = 0

                if opponent.active_spell == spell_protego:
                    print("- {name} casts {spell} on {name_o}. FAILURE! {name_o} blocks the attack!".format(name=self.name, spell=spell_name, name_o=opponent.name))
                else:
                    print("- {name} casts {spell} on {name_o} causing {dmg} damage!".format(name=self.name, spell=spell_name, name_o=opponent.name, dmg=total_damage))
                    opponent.take_health(total_damage)