# Routine by Valera, change paths, cube IDs and filenames
# It cleans spaxels array created by create_spaxels.py routine to remove negative intensities and duplicate wavelength entries
import sys
from typing import Tuple, List
import numpy as np
import os

"""
28.05.2025
Implemented outlier detection. 
They are replaced by linear interpolation.
"""
_WAV_AXIS = 0

_AXIS_SPAXEL_FLATTENED: int = 1

def correct_for_outliers(arr_3d, threshold_mad):
    # Assume `arr` is your original array of shape (Nwav, 32, 32) -> (Nwav, 32*32)
    arr_reshaped_2d = np.copy(arr_3d.reshape(arr_3d.shape[0], -1))
    n_total_outliers = 0
    for index_spaxel in range(arr_reshaped_2d.shape[_AXIS_SPAXEL_FLATTENED]):
        median =  np.median(arr_reshaped_2d[:, index_spaxel])
        mad = np.median(np.abs(arr_reshaped_2d[:, index_spaxel] - median))
        mask = np.logical_or(
            arr_reshaped_2d[:, index_spaxel] < 0,
            arr_reshaped_2d[:, index_spaxel] > median + threshold_mad * mad
        )
        indices_outliers = np.squeeze(np.argwhere(mask))

        if np.size(indices_outliers)>0:
            arr_reshaped_2d[indices_outliers, index_spaxel] = np.interp(
                wave[indices_outliers],
                wave[~mask],
                arr_reshaped_2d[~mask, index_spaxel]
            )
            n_total_outliers = n_total_outliers + np.size(indices_outliers)

    print("n_total_outliers:", n_total_outliers)
    return arr_reshaped_2d.reshape(-1, arr_3d.shape[1], arr_3d.shape[2])

base_path = "/path/to/int_cube_32_32*npy/files"
THRESHOLD_MAD = 10

cube_id = '286703' 

for index_mu in range(10):
    for d in os.listdir(f"{base_path}"):
        if d.startswith(f"int_cube_32x32_{cube_id}_{index_mu}.npy"):
           data = np.load(f"{base_path}{d}",allow_pickle=True).item()
           wave = data['wave']
           spaxel = data['intensity']

           # Sort wave for comparison
           sort_indices = np.argsort(wave)
           wave_sorted = wave[sort_indices]
           intensity_sorted = spaxel[sort_indices]

           # Create a mask where adjacent values are *not* close
           tolerance = 1e-8  # adjust this as needed
           diff = np.diff(wave_sorted)
           unique_mask = np.insert(diff > tolerance, 0, True)  # keep the first value

           # Apply mask
           wave_cleaned = wave_sorted[unique_mask]
           intensity_cleaned = intensity_sorted[unique_mask]

           duplicates_removed = len(wave) - len(wave_cleaned)
           print(f"Removed {duplicates_removed} duplicate entries from wave.")

           intensity_combined_cube=correct_for_outliers(arr_3d=spaxel, threshold_mad=THRESHOLD_MAD)
           print("min:", intensity_combined_cube.min(), "max:", intensity_combined_cube.max())
           data_to_save = {"wave":wave, "intensity":intensity_combined_cube}
           np.save(f"{base_path}/intensity_380800nm_{cube_id}_{index_mu}_16_16.npy", data_to_save)
           print("done for cube:"+cube_id)

