from setup import *
from data import *

import os


def main():

    # setup project directory
    dir_base = '/data/qte4288/Tumor-Risk-Prediction/'

    dir_exp = os.path.join(dir_base, 'experiments')
    dir_exp = create_experiment_folders(dir_exp)
    dir_model = os.path.join(dir_base, 'model')
    dir_model = create_model_folders(dir_model)

    dir_data = os.path.join(dir_base, 'data/sample')
    pth_metadata = os.path.join(dir_data, 'metadata.csv')

    # process data
    df_metadata = read_metadata(pth_metadata)


if __name__ == "__main__":
    main()