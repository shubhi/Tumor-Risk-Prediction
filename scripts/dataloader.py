import os
import torch
import pandas as pd
import nibabel as nib
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from scipy.ndimage import zoom

def resize_scan(scan, target_shape):
    factors = [float(t) / float(s) for s, t in zip(scan.shape, target_shape)]
    return zoom(scan, factors, order=1)

class TumorRiskDataset(Dataset):
    def __init__(self, metadata_file, transform=None, target_shape=(128, 128, 32)):
        self.metadata = pd.read_csv(metadata_file)
        self.transform = transform
        self.target_shape = target_shape

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        scan_path = self.metadata.iloc[idx]['dir_scan']
        label = self.metadata.iloc[idx]['label']
        days = self.metadata.iloc[idx]['days']

        print(f"Loading scan from path: {scan_path}")  # Debugging statement

        if not os.path.exists(scan_path):
            raise FileNotFoundError(f"File not found: {scan_path}")

        scan = nib.load(scan_path).get_fdata()

        # Resize the scan
        scan = resize_scan(scan, self.target_shape)

        if self.transform:
            scan = self.transform(scan)

        scan = torch.tensor(scan, dtype=torch.float32)

        sample = {'scan': scan, 'label': torch.tensor(label, dtype=torch.long), 'days': torch.tensor(days, dtype=torch.float32)}

        return sample
    
def mri_dataloader(pth_metadata_mri, batch_size=4, num_workers=4):
    
    transform = None  # Placeholder for any transformation functions

    # Initialize the dataset
    dataset = TumorRiskDataset(metadata_file=pth_metadata_mri, transform=transform)

    # Initialize the dataloader
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)

    for batch in dataloader:
        scans = batch['scan']
        labels = batch['label']
        days = batch['days']
        print(f'Scans shape: {scans.shape}, Labels: {labels}, Days: {days}')
        break  # to remove during training

