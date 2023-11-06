import matplotlib.pyplot as plt
import h5py
import os
import shutil
import numpy as np
import sys 


path = '/media/carito/Carito2/PRISMA/Results/'
in_file = path +'PRS_L1_STD_OFFL_20210922101425_20210922101429_0001_denoised.he5'


sr_swir = 'SWIR'
sr_vnir = 'VNIR'

ds_lat_swir = f'//HDFEOS/SWATHS/PRS_L1_HCO/Geolocation Fields/Latitude_{sr_swir}'
ds_lon_swir = f'//HDFEOS/SWATHS/PRS_L1_HCO/Geolocation Fields/Longitude_{sr_swir}'

ds_lat_vnir = f'//HDFEOS/SWATHS/PRS_L1_HCO/Geolocation Fields/Latitude_{sr_vnir}'
ds_lon_vnir = f'//HDFEOS/SWATHS/PRS_L1_HCO/Geolocation Fields/Longitude_{sr_vnir}'

f = h5py.File(in_file, 'r')

lat_swir = f[ds_lat_swir][:]
lon_swir = f[ds_lon_swir][:]
lat_vnir = f[ds_lat_swir][:]
lon_vnir = f[ds_lon_swir][:]

'''
SUBDATASET_11_NAME=HDF5:"PRS_L1_STD_OFFL_20210922101425_20210922101429_0001_denoised.he5"://HDFEOS/SWATHS/PRS_L1_HCO/Geolocation Fields/Latitude_SWIR
SUBDATASET_11_DESC=[1000x1000] //HDFEOS/SWATHS/PRS_L1_HCO/Geolocation_Fields/Latitude_SWIR (32-bit floating-point)
SUBDATASET_12_NAME=HDF5:"PRS_L1_STD_OFFL_20210922101425_20210922101429_0001_denoised.he5"://HDFEOS/SWATHS/PRS_L1_HCO/Geolocation_Fields/Latitude_VNIR
SUBDATASET_12_DESC=[1000x1000] //HDFEOS/SWATHS/PRS_L1_HCO/Geolocation_Fields/Latitude_VNIR (32-bit floating-point)
SUBDATASET_13_NAME=HDF5:"PRS_L1_STD_OFFL_20210922101425_20210922101429_0001_denoised.he5"://HDFEOS/SWATHS/PRS_L1_HCO/Geolocation_Fields/Longitude_SWIR
SUBDATASET_13_DESC=[1000x1000] //HDFEOS/SWATHS/PRS_L1_HCO/Geolocation_Fields/Longitude_SWIR (32-bit floating-point)
SUBDATASET_14_NAME=HDF5:"PRS_L1_STD_OFFL_20210922101425_20210922101429_0001_denoised.he5"://HDFEOS/SWATHS/PRS_L1_HCO/Geolocation_Fields/Longitude_VNIR
'''

fig, ax = plt.subplots(1,2)
vmin,vmax = np.percentile(array1, (1,99))
ax[0].imshow(array, vmin=vmin, vmax=vmax)
ax[1].imshow(ds_m_cm, vmin=np.nanmin(values_m_cm), vmax=np.nanmax(values_m_cm[values_m_cm!=255])) # land mask
ax[0].set_title('Land_Cover_Mask')
ax[1].set_title('Cloud_Mask')
