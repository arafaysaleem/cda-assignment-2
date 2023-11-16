from predictors.predictor import Predictor


class GsharePredictor(Predictor):
    def __init__(self, pc_bits, global_bhr_bits):
        self.pc_bits = pc_bits
        self.global_bhr_bits = global_bhr_bits
        self.counter_bits = 2
        self.counter = 0
        self.history = []
        self.history_index = 0

    def predict(self, address, outcome):
        # Implement Gshare Predictor logic here
        pass