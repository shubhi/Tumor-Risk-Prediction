from data import read_data


def main():

    base_directory = '/data/qte4288/BrainMRI-YOLO-LSTM' 

    mri_data = read_data(base_directory)


if __name__ == "__main__":
    main()