# Routine by Valera, edit paths and filenames
# Creates spaxels arrays using [nx x ny x nwave] intensity data from NETCDF files
# combines 16 x 16 pixels

import netCDF4 as nc
import numpy as np
import os

_WAV_AXIS = 0

class ReduceIntensityCubeSizes:

    def __init__(
        self,
        block_dim_x: int = 16,
        block_dim_y: int = 16
    ):
        """
        Initialize with block dimensions for averaging.
        
        Parameters:
        - block_dim_x (int): Block size along the x-dimension.
        - block_dim_y (int): Block size along the y-dimension.
        """
        self.nx = block_dim_x
        self.ny = block_dim_y

    def read_nc_file_and_return_averaged(self, filepath: str):
        with nc.Dataset(filepath) as dataset:
            # Read intensity and wavelength data
            spec = dataset["Intensity"][:].data
            wavevac = dataset["wave"][:].data

            # Compute the averaged intensity
            Nz, Nx, Ny = spec.shape
            averaged_int = spec.reshape(Nz, Nx // self.nx, self.nx, Ny // self.ny, self.ny).mean(axis=(2, 4))
        return averaged_int, wavevac

base_path = "/path/to/directory/with/cube_folders"
wav_start = 380
wav_end = 800
wav_step =10


reducer = ReduceIntensityCubeSizes(block_dim_x=16, block_dim_y=16)

cubes = [
 '383231',
 '384295', '384966', '385552', '386247', '386945', '387525', '388082', '388649',
 '389127', '389698', '390348', '391028', '391623', '392352', '392960', '393512',
 '394065', '394656', '395121', '395714', '396178', '396694', '397121', '397569',
 '398063', '398534', '399008', '399578', '400071', '400542', '401082', '401676',
 '402330', '402809', '403250', '403895', '404564', '405149', '405642', '406113',
 '406531', '406981', '407449', '407887'
]

for cube_id in cubes: #loop over cube id
    for index_mu in range(10): #loop over mu
        for index_wav, wav in enumerate(range(wav_start, wav_end, wav_step)): #loop over wavelengths

            folder_with_int_cubes = f"{base_path}{wav}{wav+10}nm_vald_sun_ssd_mu10/full_nc_cubes/SSD_set2_{cube_id}/"
            cube_files = []
            for d in os.listdir(folder_with_int_cubes):
                if d.startswith(f"result_Int.{cube_id}_{index_mu}"):
                    cube_files.append(os.path.join(folder_with_int_cubes, d))
            cube_files = np.sort(cube_files)


            for index_cube, cube in enumerate(cube_files):
                averaged_int, wavevac = reducer.read_nc_file_and_return_averaged(filepath=cube)
                if (index_cube==0) & (index_wav==0):
                    intensity_combined_cube = np.copy(averaged_int)
                    wave_combined_cube = np.copy(wavevac)
                else:
                    intensity_combined_cube = np.concatenate((intensity_combined_cube, averaged_int), axis=_WAV_AXIS)
                    wave_combined_cube = np.concatenate((wave_combined_cube, wavevac), axis=_WAV_AXIS)

        data_to_save = {"wave":wave_combined_cube, "intensity":intensity_combined_cube}
        np.save(f"/path/to/desired/save_folder/int_cube_32x32_{cube_id}_{index_mu}.npy", data_to_save)
