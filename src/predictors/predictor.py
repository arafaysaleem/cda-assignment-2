from abc import ABC, abstractmethod

class Predictor(ABC):

    @abstractmethod
    def predict(self, address, outcome):
        pass