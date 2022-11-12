from system.event.event_receiver import *
from system.core.character import *
from gui.scenes.fight.fight_view_controller import *
from gui.event_receiver import *

class FightEventReceiver(EventReceiverInterface):
    def __init__(self, controller : FightViewController, event_receiver : SystemEventReceiver):
        self.controller = controller
        self.event_receiver = event_receiver

    def on_start(self):
        self.event_receiver.on_start()

    def on_end(self, winner_faction : int):
        self.event_receiver.on_end(winner_faction)

    def on_attack(self, attacker : Character, targets):
        self.controller.show_effect(attacker, CharacterPortrait.EFFECT_MOVE_FORWARD)
        self.event_receiver.on_attack(attacker, targets)

    def on_damage(self, character : Character, damage : int):
        self.controller.show_effect(character, CharacterPortrait.EFFECT_BLOOD)
        self.event_receiver.on_damage(character, damage)

    def on_block(self, character : Character):
        self.controller.show_effect(character, CharacterPortrait.EFFECT_BLOOD)
        self.event_receiver.on_block(character)

    def on_cast_spell(self, attacker : Character, targets, spell_name : str):
        self.controller.show_effect(attacker, CharacterPortrait.EFFECT_MOVE_BACKWARD)
        self.event_receiver.on_cast_spell(attacker, targets, spell_name)

    def on_spell_effect(self, targets, effect : str):
        self.controller.update_arena()
        self.event_receiver.on_spell_effect(targets, effect)

    def on_magic_block(self, character : Character):
        self.controller.show_effect(character, CharacterPortrait.EFFECT_BLOOD)
        self.event_receiver.on_magic_block(character)

    def on_wait(self, character : Character):
        self.event_receiver.on_wait(character)

    def on_death(self, character : Character):
        self.controller.update_hud()
        self.controller.update_arena()
        self.event_receiver.on_death(character)

    def on_new_turn(self, current_character : Character, characters):
        self.controller.update_hud()
        self.controller.update_arena()
        self.controller.set_selected_character(current_character)
        self.event_receiver.on_new_turn(current_character, characters)

    def on_move(self, character : Character):
        self.controller.update_arena()
        self.event_receiver.on_move(character)