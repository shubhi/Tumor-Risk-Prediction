import os
import nibabel as nib
import pandas as pd

def read_metadata(pth_metadata):
    df_metadata = pd.read_csv(pth_metadata)


def read_mri_scans(base_dir):
    data = {}
    
    # Iterate through each patient directory
    for patient_id in os.listdir(base_dir):
        patient_dir = os.path.join(base_dir, patient_id)
        if os.path.isdir(patient_dir):
            data[patient_id] = {}
            
            # Iterate through each appointment directory
            for appointment in os.listdir(patient_dir):
                appointment_dir = os.path.join(patient_dir, appointment)
                if os.path.isdir(appointment_dir):
                    data[patient_id][appointment] = {}
                    
                    # Iterate through each MRI scan type file
                    for mri_type in os.listdir(appointment_dir):
                        mri_file = os.path.join(appointment_dir, mri_type)
                        if os.path.isfile(mri_file) and mri_file.endswith('.nii'):
                            scan = nib.load(mri_file)
                            data[patient_id][appointment][mri_type] = scan.get_fdata()
    
    return data

def read_data(base_directory):

    base_directory = "/data/qte4288/BrainMRI-YOLO-LSTM"
    mri_data = read_mri_scans(base_directory)

    print(mri_)

    # Sample output
    for patient_id, appointments in mri_data.items():
        print(f"Patient ID: {patient_id}")
        for appointment, scans in appointments.items():
            print(f"  Appointment: {appointment}")
            for scan_type, scan_data in scans.items():
                print(f"    Scan Type: {scan_type} - Shape: {scan_data.shape}")

    return mri_data
