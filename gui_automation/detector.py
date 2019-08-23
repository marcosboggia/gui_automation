# Made by Marcos Boggia
from abc import ABC, abstractmethod


class Detector(ABC):
    @abstractmethod
    def detect(self, *args):
        pass
