from datetime import datetime
import os


def create_experiment_folders(dir_exp):
    """Create directories for the experiment logs."""
    str_date = datetime.now().strftime('%Y%m%d')
    str_time = datetime.now().strftime('%H%M%S')
    dir_exp = os.path.join(dir_exp, str_date, str_time)
    os.makedirs(dir_exp, exist_ok=True)
    
    subdirs = ['model_architecture', 'train_val_test_details', 'results']
    for subdir in subdirs:
        os.makedirs(os.path.join(dir_exp, subdir), exist_ok=True)
    
    return dir_exp

def create_model_folders(dir_model):
    """Create directories for the models."""
    str_date = datetime.now().strftime('%Y%m%d')
    str_time = datetime.now().strftime('%H%M%S')
    dir_model = os.path.join(dir_model, str_date, str_time)
    os.makedirs(dir_model, exist_ok=True)

    subdirs = ['best_model', 'model_weights']
    for subdir in subdirs:
        os.makedirs(os.path.join(dir_model, subdir), exist_ok=True)

    return dir_model
    

