import pygame
from gui.input.input_event import *
from gui.input.input_controller_interface import *

class GlobalInputController:
    def __init__(self):
        self.controllers = set()

    def __define_event(event : pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                return InputEvent(InputEvent.UP_PRESSED)
            if keys[pygame.K_DOWN] :
                return InputEvent(InputEvent.DOWN_PRESSED)
            if keys[pygame.K_LEFT]:
                return InputEvent(InputEvent.LEFT_PRESSED)
            if keys[pygame.K_RIGHT] :
                return InputEvent(InputEvent.RIGHT_PRESSED)
            if keys[pygame.K_RETURN] :
                return InputEvent(InputEvent.SELECT_PRESSED)
            if keys[pygame.K_a]:
                return InputEvent(InputEvent.A_PRESSED)
            if keys[pygame.K_b] :
                return InputEvent(InputEvent.B_PRESSED)
            if keys[pygame.K_c] :
                return InputEvent(InputEvent.C_PRESSED)
            if keys[pygame.K_d] :
                return InputEvent(InputEvent.D_PRESSED)
            if keys[pygame.K_e] :
                return InputEvent(InputEvent.E_PRESSED)
            if keys[pygame.K_f] :
                return InputEvent(InputEvent.F_PRESSED)
            if keys[pygame.K_g] :
                return InputEvent(InputEvent.G_PRESSED)
            if keys[pygame.K_h] :
                return InputEvent(InputEvent.H_PRESSED)
            if keys[pygame.K_i] :
                return InputEvent(InputEvent.I_PRESSED)
            if keys[pygame.K_j] :
                return InputEvent(InputEvent.J_PRESSED)
            if keys[pygame.K_k] :
                return InputEvent(InputEvent.K_PRESSED)
            if keys[pygame.K_l] :
                return InputEvent(InputEvent.L_PRESSED)
            if keys[pygame.K_m] :
                return InputEvent(InputEvent.M_PRESSED)
            if keys[pygame.K_n] :
                return InputEvent(InputEvent.N_PRESSED)
            if keys[pygame.K_o] :
                return InputEvent(InputEvent.O_PRESSED)
            if keys[pygame.K_p] :
                return InputEvent(InputEvent.P_PRESSED)
            if keys[pygame.K_q] :
                return InputEvent(InputEvent.Q_PRESSED)
            if keys[pygame.K_r] :
                return InputEvent(InputEvent.R_PRESSED)
            if keys[pygame.K_s] :
                return InputEvent(InputEvent.S_PRESSED)
            if keys[pygame.K_t] :
                return InputEvent(InputEvent.T_PRESSED)
            if keys[pygame.K_u] :
                return InputEvent(InputEvent.U_PRESSED)
            if keys[pygame.K_v] :
                return InputEvent(InputEvent.V_PRESSED)
            if keys[pygame.K_w] :
                return InputEvent(InputEvent.W_PRESSED)
            if keys[pygame.K_x] :
                return InputEvent(InputEvent.X_PRESSED)
            if keys[pygame.K_y] :
                return InputEvent(InputEvent.Y_PRESSED)
            if keys[pygame.K_z] :
                return InputEvent(InputEvent.Z_PRESSED)
            if keys[pygame.K_BACKSPACE] :
                return InputEvent(InputEvent.BACKSPACE_PRESSED)
        return InputEvent(InputEvent.NONE)

    def register_controller(self, controller : InputControllerInterface):
        self.controllers.add(controller)

    def unregister_controller(self, controller : InputControllerInterface):
        self.controllers.discard(controller)

    def process_pygame_event(self, pygame_event : pygame.event.Event):
        event = GlobalInputController.__define_event(pygame_event)
        if event.event != InputEvent.NONE:
            for controller in self.controllers:
                controller.on_event(event)