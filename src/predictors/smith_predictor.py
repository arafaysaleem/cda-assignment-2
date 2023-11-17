from .predictor import Predictor

class SmithPredictor(Predictor):
    def __init__(self, counter_bits):
        self.counter_bits = counter_bits
        self.counter = 1 << (self.counter_bits - 1)
        self.mispredictions = 0
        self.accesses = 0

    def run(self, address: str, outcome: str) -> None:
        self.accesses += 1

        prediction = self.counter >= (1 << (self.counter_bits - 1))

        actual_outcome = outcome == 't'

        if prediction != actual_outcome:
            self.mispredictions += 1

        if actual_outcome:  # Taken
            self.counter = min(self.counter + 1, (1 << self.counter_bits) - 1)
        else:
            self.counter = max(self.counter - 1, 0)

    def __str__(self) -> str:
        stats = f"number of predictions:		{self.accesses}\n"
        stats += f"number of mispredictions:	{self.mispredictions}\n"
        stats += f"misprediction rate:		{format(self.mispredictions / self.accesses * 100, '.2f')}%\n"
        stats += f"FINAL COUNTER CONTENT:		{self.counter}\n"
        return stats
