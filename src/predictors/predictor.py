from abc import ABC, abstractmethod

class Predictor(ABC):

    @abstractmethod
    def run(self, address, outcome):
        pass