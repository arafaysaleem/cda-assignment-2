from .predictor import Predictor


class BimodalPredictor(Predictor):
    def __init__(self, pc_bits):
        self.pc_bits = pc_bits
        self.counter = [4] * (2**pc_bits)
        self.mispredictions = 0
        self.accesses = 0

    def predict(self, address, outcome):
        self.accesses += 1

        address = int(address, 16)
        index = (address >> 2) & ((1 << self.pc_bits) - 1)

        prediction = self.counter[index] >= 4

        actual_outcome = outcome == "t"

        if prediction != actual_outcome:
            self.mispredictions += 1

        if actual_outcome:  # Taken
            self.counter[index] = min(self.counter[index] + 1, 7)
        else:
            self.counter[index] = max(self.counter[index] - 1, 0)

    def __str__(self) -> str:
        stats = f"number of predictions:		{self.accesses}\n"
        stats += f"number of mispredictions:	{self.mispredictions}\n"
        stats += f"misprediction rate:		{format(self.mispredictions / self.accesses * 100, '.2f')}%\n"
        stats += f"FINAL BIMODAL CONTENTS\n"
        for i in range(len(self.counter)):
            stats += f"{i}	{self.counter[i]}\n"
        return stats
