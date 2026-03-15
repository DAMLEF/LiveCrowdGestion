import time
import pygame

from tools.text_style import BaseStyle
from tools.colors import RED

class Error_Message():

    base_error_style = BaseStyle(15, RED)

    def __init__(self):
        self.messages = []

    def actualise(self):
        to_remove = []
        for em in self.messages:
            if time.time() - em.start > em.duration:
                to_remove.append(em)

        for em in to_remove:
            self.messages.remove(em)

    def display(self, window: pygame.Surface, start_x: int, start_y: int):

        y_offset = 0
        for error in self.messages:
            error_render = Error_Message.base_error_style.render(error.text)

            window.blit(error_render, (start_x, start_y + y_offset))

            y_offset += error_render.get_height() + 3


    def add_message(self, text: str, duration: float):
        self.messages.append(_Message(text, duration))


class _Message:
    def __init__(self, text: str, duration: float):
        self.text = text
        self.duration = duration
        self.start = time.time()

