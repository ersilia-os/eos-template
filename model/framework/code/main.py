# imports
import os
import sys
import numpy as np
from rdkit import Chem
from rdkit.Chem.Descriptors import MolWt
from ersilia_pack_utils.core import read_smiles, write_out

# current file directory
root = os.path.dirname(os.path.abspath(__file__))
checkpoints = os.path.join(root, "..", "..", "checkpoints")


# load the model once: imports, checkpoints and anything else that is slow to set up.
# When served, Ersilia calls this once and keeps the result in memory between batches.
def load_tool():
    return MolWt


# run the model on one batch: read the input file, predict, write the output file.
def run_tool(model, input_file, output_file):
    # read SMILES from .csv file, assuming one column with header
    _, smiles_list = read_smiles(input_file)

    # run model
    outputs = np.array([[model(Chem.MolFromSmiles(smi))] for smi in smiles_list])

    # check input and output have the same length
    assert len(smiles_list) == len(outputs)

    num_dims = outputs.shape[1]
    header = [f"feat_{str(i).zfill(3)}" for i in range(num_dims)]

    # write output in a .csv file
    write_out(outputs, header, output_file, np.float32)


if __name__ == "__main__":
    # parse arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    run_tool(load_tool(), input_file, output_file)
