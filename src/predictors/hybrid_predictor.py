from predictors.predictor import Predictor


class HybridPredictor(Predictor):
    def __init__(self, pc_bits_chooser, pc_bits_gshare, global_bhr_bits, pc_bits_bimodal):
        self.pc_bits_chooser = pc_bits_chooser
        self.pc_bits_gshare = pc_bits_gshare
        self.global_bhr_bits = global_bhr_bits
        self.pc_bits_bimodal = pc_bits_bimodal
        self.counter_bits = 2
        self.counter = 0
        self.history = []
        self.history_index = 0

    def predict(self, address, outcome):
        # Implement Hybrid Predictor logic here
        pass