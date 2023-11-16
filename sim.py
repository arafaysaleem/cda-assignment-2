import sys
from src.predictors.gshare_predictor import GsharePredictor
from src.predictors.bimodal_predictor import BimodalPredictor
from src.predictors.predictor import Predictor

from src.predictors.smith_predictor import SmithPredictor


def run_smith_predictor() -> None:
    if len(sys.argv) != 4:
        print("Invalid arguments for Smith Predictor")
        return
    counter_bits = int(sys.argv[2])
    tracefile = sys.argv[3]
    smith_predictor = SmithPredictor(counter_bits)

    run_trace(tracefile, smith_predictor)
    print(smith_predictor)


def run_bimodal_predictor():
    if len(sys.argv) != 4:
        print("Invalid arguments for Bimodal Predictor")
        return
    pc_bits = int(sys.argv[2])
    tracefile = sys.argv[3]
    bimodal_predictor = BimodalPredictor(pc_bits)

    run_trace(tracefile, bimodal_predictor)
    print(bimodal_predictor)


def run_gshare_predictor():
    if len(sys.argv) != 5:
        print("Invalid arguments for Gshare Predictor")
        return
    pc_bits = int(sys.argv[2])
    global_bhr_bits = int(sys.argv[3])
    tracefile = sys.argv[4]
    gshare_predictor = GsharePredictor(pc_bits, global_bhr_bits)

    run_trace(tracefile, gshare_predictor)
    print(gshare_predictor)


def run_hybrid_predictor():
    if len(sys.argv) != 7:
        print("Invalid arguments for Hybrid Predictor")
        return
    pc_bits_chooser = int(sys.argv[2])
    pc_bits_gshare = int(sys.argv[3])
    global_bhr_bits = int(sys.argv[4])
    pc_bits_bimodal = int(sys.argv[5])
    tracefile = sys.argv[6]
    # Implement Hybrid Predictor logic here
    pass


def run_trace(tracefile: str, predictor: Predictor):
    with open(tracefile, "r") as f:
        for line in f:
            (address, outcome) = line.strip().split(" ")
            predictor.predict(address, outcome)


def main():
    if len(sys.argv) < 3:
        print("Invalid arguments")
        return

    print("COMMAND")
    print("./" + " ".join(sys.argv))
    print("OUTPUT")

    sim_type = sys.argv[1]
    if sim_type == "smith":
        run_smith_predictor()
    elif sim_type == "bimodal":
        run_bimodal_predictor()
    elif sim_type == "gshare":
        run_gshare_predictor()
    elif sim_type == "hybrid":
        run_hybrid_predictor()
    else:
        print("Invalid simulator type")


if __name__ == "__main__":
    main()
