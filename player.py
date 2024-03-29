import random
from wands import Wand
from spells import SPELL_TYPE_NONE, SPELL_TYPE_USELESS, SPELL_TYPE_DEFENSE, SPELL_TYPE_UNFORGIVABLE#, SPELL_TYPE_COMMON, SPELL_TYPE_POWERFUL
from spells import Spell, spells, _INVALID_SPELL
from game_config import MAX_PLAYER_HEALTH, MAX_STUNNED_ROUNDS

class Player:
    def __init__(self, name: str, wand: Wand) -> None:
        self.name: str                              = name
        self.health: float                          = MAX_PLAYER_HEALTH
        self.wand: Wand                             = wand

        self.active_spell: Spell                    = spells[_INVALID_SPELL]
        self.active_spell_succes: bool              = False
        self.active_spell_levenshtein_distance: int = 0 # Penalty => If >0 then damage reduction, 15 per distance

        self.stunned_rounds: int                    = 0
        self.decreased_spell_speed: bool            = False
        self.decreased_spell_damage: bool           = False

        self.lumos: bool                            = False

    def give_health(self, health: int) -> float:
        self.health += health
        if self.health > MAX_PLAYER_HEALTH:
            self.health = MAX_PLAYER_HEALTH
        return self.health

    def take_health(self, health: int) -> float:
        self.health -= health
        if self.health < 0:
            self.health = 0
        return self.health
    
    def add_stunned_rounds(self, rounds: int) -> None:
        self.stunned_rounds += rounds + 1
        if (self.stunned_rounds > MAX_STUNNED_ROUNDS + 1):
            self.stunned_rounds = MAX_STUNNED_ROUNDS

    def get_spell_succes_rate(self, spell: Spell) -> float:
        if spell == None:
            return 0
        return 1 * self.wand.succes_rate * spell.succes_rate
    
    def get_queued_effects(self) -> str:
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

    def cast_spell_result(self, spell: Spell, succes: bool) -> str:
        if spell == None:
            return "<!> {name} can't cast anything but Finite Incantatem since they are stunned".format(name=self.name)

        if succes:
            message = "{name} casted '{spell}' with succes"
        else:
            if spell.type == SPELL_TYPE_UNFORGIVABLE:
                message = "{name} tried to cast '{spell}' but didn't truly mean it. Cast FAILED!"
            elif spell.type == SPELL_TYPE_NONE:
                if spell == spells[_INVALID_SPELL]:
                    return "{name} must not be feeling well, since they casted a non existing spell. Cast FAILED!".format(name=self.name)
            else: message = "{name} tried to cast '{spell}' but mispronounced it. Cast FAILED!"
        return message.format(name=self.name, spell=spell.get_spell_name())
    
    def cast_spell(self, opponent) -> None:
        spell_name = self.active_spell.get_spell_name()

        if self.active_spell is None:
            print("- {name} does nothing".format(name=self.name))
            return
        
        if self.stunned_rounds > 0 and self.active_spell is not spells["Finite Incantatem"]:
            print("<!> {name} tries to cast a spell but fails because they are stunned!".format(name=self.name))
            return

        if self.active_spell.type == SPELL_TYPE_USELESS:
            if self.active_spell is spells["Lumos"]:
                if self.lumos:
                    print("- {name} casts {spell} with no effect: {name} already has a brutal shining light at the tip of their wand!".format(name=self.name, spell=spell_name))
                else:
                    print("- {name} casts {spell}! Look at that brutal shining light at the tip of their wand. Absolutely gorgeous!".format(name=self.name, spell=spell_name))
                    self.lumos = True
            elif self.active_spell is spells["Nox"]:
                if not self.lumos:
                    print("- {name} shouts: {spell}! Nothing happened".format(name=self.name, spell=spell_name.upper()))
                else:
                    print("- {name} shouts {spell}! Their brutal shining light dissapears".format(name=self.name, spell=spell_name.upper()))
                    self.lumos = False
            elif self.active_spell is spells["Rennervate"]:
                if opponent.stunned_rounds == 0:
                    print("- {name} casts {spell} with no effect, because {name_o} is not currently stunned!".format(name=self.name, spell=spell_name, name_o=opponent.name))
                else:
                    print("- {name} casts {spell}! {name_o} is no longer stunned!".format(name=self.name, spell=spell_name, name_o=opponent.name))
                    opponent.stunned_rounds = 0
            elif self.active_spell is spells["Igni"]:
                print("- Geralt casts Igni. Wait. Geralt? White Wolf? The butcher of Blaviken? What is he doing here? Is he even here? What is going on?")
            else:
                print("<!> [debug]{name} casted SPELL_TYPE_USELESS {spell}. Behaviour unscripted!".format(name=self.name, spell=spell_name))                
        
        elif self.active_spell.type == SPELL_TYPE_DEFENSE:
            spell_succes = True
            if self.active_spell is spells["Finite Incantatem"]:
                if self.stunned_rounds > 0:
                    if not 10 > random.random() * 100:
                        spell_succes = False
                        print("- {name} has no luck. Casting {spell} had no effect".format(name=self.name, spell=spell_name))
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
            elif self.active_spell is spells["Impendimenta"]:
                if opponent.active_spell is spells["Protego"] and opponent.active_spell_succes:
                    print("- {name} casts {spell} on {name_o}. FAILURE! {name_o} blocks the attack!".format(name=self.name, name_o=opponent.name, spell=spell_name))
                else:
                    print("- {name} casts {spell} on {name_o}. {name_o} is slowed and their next offensive move will have a 33% slower spell speed!".format(name=self.name, name_o=opponent.name, spell=spell_name))
                    opponent.decreased_spell_speed = True                    
            elif self.active_spell is spells["Lumos Solem"]:
                # Light still goes through the shield, therefor always succeed blinding attempts
                print("- {name} casts {spell} on {name_o}. {name_o} is blinded and their next offensive move will have 33% less damage!".format(name=self.name, name_o=opponent.name, spell=spell_name))
                opponent.decreased_spell_damage = True
            elif self.active_spell is spells["Protego"] and self.active_spell_succes:
                print("- {name} casts {spell}".format(name=self.name, spell=spell_name))
            else:
                print("<!> [debug]{name} casted SPELL_TYPE_DEFENSE {spell}. Behaviour unscripted!".format(name=self.name, spell=spell_name))

        elif self.active_spell.type == SPELL_TYPE_UNFORGIVABLE:
            if self.active_spell is spells["Avada Kedavra"]:
                print("- THE NERVE! {name} casts the killing curse! See you in the after life {name_o}!".format(name=self.name, name_o=opponent.name))
                opponent.health = 0
            elif self.active_spell is spells["Crucio"]:
                print("- THE NERVE! {name} casts the torture curse. {name_o} is greatly hurt and falls to the ground. They are stunned for 5 (more) moves".format(name=self.name, name_o=opponent.name))
                opponent.add_stunned_rounds(5)
                opponent.take_health(self.active_spell.damage)
            elif self.active_spell is spells["Imperio"]:
                print("- THE NERVE! {name} casts the Imperius curse. \"Why don't you take a nice nap for {max_stunned_rounds} moves, {name_o}?\". {name_o} submits with pleasure".format(name=self.name, name_o=opponent.name, max_stunned_rounds=MAX_STUNNED_ROUNDS))
                opponent.add_stunned_rounds(MAX_STUNNED_ROUNDS)

        else:
            if self.active_spell is spells["Mimblewimble"]:
                if opponent.active_spell is spells["Protego"] and opponent.active_spell_succes:
                    print("- {name} casts {spell} on {name_o}. FAILURE! {name_o} blocks the attack!".format(name=self.name, spell=spell_name, name_o=opponent.name))
                else:
                    print("- {name} casts {spell} on {name_o}. {name_o}'s tongue is tied in a knot. That's annoying! {name_o} is silenced for 1 (more) move".format(name=self.name, spell=spell_name, name_o=opponent.name))
                    opponent.add_stunned_rounds(-self.active_spell.damage)                    
            elif self.active_spell is spells["Silencio"]:
                if opponent.active_spell is spells["Protego"] and opponent.active_spell_succes:
                    print("- {name} casts {spell} on {name_o}. FAILURE! {name_o} blocks the attack!".format(name=self.name, spell=spell_name, name_o=opponent.name))
                else:
                    if opponent.stunned_rounds == 0:
                        print("- {name} casts {spell} on {name_o}. SUCCES! {name_o} is silenced for 3 (more) moves".format(name=self.name, spell=spell_name, name_o=opponent.name))
                        opponent.add_stunned_rounds(-self.active_spell.damage)
                    else:
                        print("- {name} casts {spell} on {name_o}. FAILURE! {name_o} is already silenced!".format(name=self.name, spell=spell_name, name_o=opponent.name))                    
            else:
                damage_penalty = self.active_spell_levenshtein_distance * 15
                if damage_penalty != 0: print("<!> {name} was unclear in their pronunciation and receives a damage penalty of {damage_penalty}".format(name=self.name, damage_penalty=damage_penalty))

                if self.decreased_spell_damage:
                    self.decreased_spell_damage = False
                    damage_modifier = 0.67
                else:
                    damage_modifier = 1

                total_damage = self.active_spell.damage * self.wand.damage * damage_modifier - damage_penalty
                if total_damage < 0: total_damage = 0

                if opponent.active_spell is spells["Protego"] and opponent.active_spell_succes:
                    print("- {name} casts {spell} on {name_o}. FAILURE! {name_o} blocks the attack!".format(name=self.name, spell=spell_name, name_o=opponent.name))                
                else:
                    print("- {name} casts {spell} on {name_o} causing {dmg} damage!".format(name=self.name, spell=spell_name, name_o=opponent.name, dmg=total_damage))
                    opponent.take_health(total_damage)           