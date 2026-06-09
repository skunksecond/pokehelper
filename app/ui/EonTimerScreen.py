import pygame
from ui.screen import Screen
from ui.set_screen import set_screen
from eontimer import request_exit
from ui.widgets import Button


class EonTimerScreen(Screen):
    def __init__(self):
        self.done = False
        self.exit_button = Button(
            pygame.Rect(620, 420, 140, 44),
            "Back",
            callback=self._exit,
        )
        self.exit_button.set_selected(True)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._exit()
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._exit()

        self.exit_button.handle_event(event)

    def update(self):
        if self.done:
            self._exit()

    def draw(self, surface):
        self.exit_button.draw(surface)

    def _return_to_menu(self):
        if self.done:
            return
        self.done = True
        from ui.menu import MainMenu
        set_screen(MainMenu())

    def _exit(self):
        if self.done:
            return
        self.done = True
        request_exit(self._return_to_menu)