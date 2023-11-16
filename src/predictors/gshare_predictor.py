from .predictor import Predictor


class GsharePredictor(Predictor):
    def __init__(self, pc_bits, global_bhr_bits):
        self.pc_bits = pc_bits
        self.global_bhr_bits = global_bhr_bits
        self.counter = [4] * (2**pc_bits)
        self.history = 0
        self.mispredictions = 0
        self.accesses = 0

    def predict(self, address, outcome):
        self.accesses += 1
        address = int(address, 16) & ~0b11

        index = (address >> 2) & ((1 << self.pc_bits) - 1)
        if self.global_bhr_bits > 0:
            index ^= (self.history & ((1 << self.global_bhr_bits) - 1))

        prediction = self.counter[index] >= 4
        
        actual_outcome = outcome == 't'
        if prediction != actual_outcome:
            self.mispredictions += 1

        if actual_outcome:
            self.counter[index] = min(7, self.counter[index] + 1)
        else:
            self.counter[index] = max(0, self.counter[index] - 1)

        self.history = ((self.history >> 1) | (actual_outcome << (self.global_bhr_bits - 1))) & ((1 << self.global_bhr_bits) - 1)

    def __str__(self) -> str:
        stats = f"number of predictions:		{self.accesses}\n"
        stats += f"number of mispredictions:	{self.mispredictions}\n"
        stats += f"misprediction rate:		{format(self.mispredictions / self.accesses * 100, '.2f')}%\n"
        stats += f"FINAL GSHARE CONTENTS\n"
        for i in range(len(self.counter)):
            stats += f"{i}	{self.counter[i]}\n"
        return stats
