from .gshare_predictor import GsharePredictor
from .bimodal_predictor import BimodalPredictor
from .predictor import Predictor
from enum import Enum


class PredictorType(Enum):
    GSHARE = 1
    BIMODAL = 2


class HybridPredictor(Predictor):
    def __init__(
        self, pc_bits_chooser, pc_bits_gshare, global_bhr_bits, pc_bits_bimodal
    ):
        self.pc_bits_chooser = pc_bits_chooser
        self.mispredictions = 0
        self.accesses = 0
        self.chooser = [1] * (2**pc_bits_chooser)
        self.bimodal = BimodalPredictor(pc_bits_bimodal)
        self.gshare = GsharePredictor(pc_bits_gshare, global_bhr_bits)

    def run(self, address, outcome):
        self.accesses += 1
        address = int(address, 16) & ~0b11
        actual_outcome = outcome == "t"

        prediction_gshare = self.gshare.predict(address)
        prediction_bimodal = self.bimodal.predict(address)

        index = (address >> 2) & ((1 << self.pc_bits_chooser) - 1)

        if self.chooser[index] >= 2:
            prediction = prediction_gshare
            selected_predictor = PredictorType.GSHARE
        else:
            prediction = prediction_bimodal
            selected_predictor = PredictorType.BIMODAL

        if prediction != actual_outcome:
            self.mispredictions += 1

        if selected_predictor == PredictorType.GSHARE:
            self.gshare.update_predictor(address, actual_outcome)
        else:
            self.bimodal.update_predictor(address, actual_outcome)

        self.gshare.update_history(actual_outcome)

        if prediction_gshare == prediction_bimodal:
            pass  # case 1: no change
        elif prediction_gshare == actual_outcome:
            self.chooser[index] = min(3, self.chooser[index] + 1)  # case 2: increment
        else:
            self.chooser[index] = max(0, self.chooser[index] - 1)  # case 3: decrement

    def __str__(self) -> str:
        stats = f"number of predictions:		{self.accesses}\n"
        stats += f"number of mispredictions:	{self.mispredictions}\n"
        stats += f"misprediction rate:		{format(self.mispredictions / self.accesses * 100, '.2f')}%\n"
        stats += f"FINAL CHOOSER CONTENTS\n"
        for i in range(len(self.chooser)):
            stats += f"{i}	{self.chooser[i]}\n"
        stats += self.gshare.get_content()
        stats += self.bimodal.get_content()
        return stats
