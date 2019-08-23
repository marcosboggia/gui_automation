# Made by Marcos Boggia
from abc import ABC, abstractmethod


class Handler(ABC):
    @abstractmethod
    def screenshot(self, *args):
        pass

    def move(self, *args):
        pass

    def click(self, *args):
        pass

    def hold_click(self, *args):
        pass

    def drag_click(self, *args):
        pass
