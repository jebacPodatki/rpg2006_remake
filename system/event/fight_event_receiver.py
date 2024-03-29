from system.core.character import Character

class FightEventReceiverInterface:
    def on_start(self):
        pass
    def on_end(self, winner_faction : int):
        pass
    def on_attack(self, attacker : Character, targets):
        pass
    def on_damage(self, character : Character, damage : int, armor_reduction : int, critical : bool):
        pass
    def on_block(self, character : Character):
        pass
    def on_cast_spell(self, attacker : Character, targets, spell_name : str):
        pass
    def on_spell_effect(self, targets, effect : str):
        pass
    def on_magic_block(self, character : Character):
        pass
    def on_wait(self, character : Character):
        pass
    def on_death(self, character : Character):
        pass
    def on_new_turn(self, current_character : Character, characters):
        pass
    def on_move(self, character : Character):
        pass