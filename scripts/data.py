import os
import nibabel as nib
import pandas as pd

def read_metadata(pth_metadata, base_dir):
    df_metadata = pd.read_csv(pth_metadata, dtype={'scan_folder': str})
    
    # Convert label to numerical
    df_metadata['label'] = df_metadata['label'].apply(lambda x: 1 if x == 'TRUE' else 0)
    
    # Convert time to datetime
    df_metadata['time'] = pd.to_datetime(df_metadata['time'], format='%d-%m-%y')
    
    # Calculate days since first scan
    df_metadata['days'] = df_metadata.groupby('patient_id')['time'].transform(lambda x: (x - x.min()).dt.days)
    
    # Create dir_scan column
    df_metadata['dir_scan'] = df_metadata.apply(
        lambda row: os.path.join(base_dir, row['patient_id'], row['scan_folder']), axis=1
    )
    
    return df_metadata

def load_scan(scan_path):
    """Load an individual MRI scan using nibabel."""
    return nib.load(scan_path).get_fdata()

def load_patient_data(dir_scan):
    """Load all MRI scans for a given scan directory."""
    scans = {}
    for scan in os.listdir(dir_scan):
        scan_type = os.path.splitext(scan)[0]
        scan_path = os.path.join(dir_scan, scan)
        scans[scan_type] = load_scan(scan_path)
    return scans

def load_all_data(metadata):
    """Load data for all patients based on the metadata CSV."""
    data = {}
    for _, row in metadata.iterrows():
        patient_id = row['patient_id']
        if patient_id not in data:
            data[patient_id] = []
        data[patient_id].append(load_patient_data(row['dir_scan']))
    return data


def create_metadata_mri_df(metadata):
    """Create a new DataFrame with MRI scan types included."""
    new_rows = []
    
    for _, row in metadata.iterrows():
        scan_dir = row['dir_scan']
        if os.path.exists(scan_dir):
            for scan_file in os.listdir(scan_dir):
                scan_type = os.path.splitext(scan_file)[0]
                scan_type = scan_type.split('_')[0]  # Extract the base scan type (e.g., 'FLAIR' from 'FLAIR_1.nii')
                new_row = row.copy()
                new_row['mri'] = scan_type
                new_rows.append(new_row)
    
    new_df = pd.DataFrame(new_rows)
    
    # Reorder columns
    cols = list(new_df.columns)
    cols.remove('dir_scan')
    cols.remove('label')
    cols.append('label')
    cols.append('dir_scan')
    new_df = new_df[cols]
    
    return new_df

def save_metadata_mri_df(df, save_path):
    """Save the new metadata DataFrame with MRI scan types to a CSV file."""
    df.to_csv(save_path, index=False)