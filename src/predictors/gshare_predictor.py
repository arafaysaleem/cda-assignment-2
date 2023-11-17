from .predictor import Predictor


class GsharePredictor(Predictor):
    def __init__(self, pc_bits, global_bhr_bits):
        self.pc_bits = pc_bits
        self.global_bhr_bits = global_bhr_bits
        self.counter = [4] * (2**pc_bits)
        self.history = 0
        self.mispredictions = 0
        self.accesses = 0

    def run(self, address, outcome):
        self.accesses += 1
        address = int(address, 16) & ~0b11

        prediction = self.predict(address)
        
        actual_outcome = outcome == 't'
        if prediction != actual_outcome:
            self.mispredictions += 1

        self.update_predictor(address, actual_outcome)
        self.update_history(actual_outcome)

        return prediction
    
    def predict(self, address):
        index = (address >> 2) & ((1 << self.pc_bits) - 1)
        if self.global_bhr_bits > 0:
            index ^= (self.history & ((1 << self.global_bhr_bits) - 1))

        return self.counter[index] >= 4

    def update_predictor(self, address, actual_outcome):
        index = (address >> 2) & ((1 << self.pc_bits) - 1)
        if self.global_bhr_bits > 0:
            index ^= (self.history & ((1 << self.global_bhr_bits) - 1))

        if actual_outcome:
            self.counter[index] = min(7, self.counter[index] + 1)
        else:
            self.counter[index] = max(0, self.counter[index] - 1)

    def update_history(self, actual_outcome):
        self.history = ((self.history >> 1) | (actual_outcome << (self.global_bhr_bits - 1))) & ((1 << self.global_bhr_bits) - 1)

    def __str__(self) -> str:
        stats = f"number of predictions:		{self.accesses}\n"
        stats += f"number of mispredictions:	{self.mispredictions}\n"
        stats += f"misprediction rate:		{format(self.mispredictions / self.accesses * 100, '.2f')}%\n"
        stats += self.get_content()
        return stats

    def get_content(self) -> str:
        stats = f"FINAL GSHARE CONTENTS\n"
        for i in range(len(self.counter)):
            stats += f"{i}	{self.counter[i]}\n"
        return stats