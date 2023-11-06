import h5py
import rasterio 
from rasterio.transform import from_gcps
from rasterio.control import GroundControlPoint as GCP

in_file = 'PRS_L1_STD_OFFL_20210922101425_20210922101429_0001.he5'
mask = '//HDFEOS/SWATHS/PRS_L1_HCO/Data Fields/LandCover_Mask'
latitude = '//HDFEOS/SWATHS/PRS_L1_HRC/Geolocation Fields/Latitude_SWIR'
longitude = '//HDFEOS/SWATHS/PRS_L1_HRC/Geolocation Fields/Longitude_SWIR'


with h5py.File(in_file,  mode='r') as hf:
    ds = hf[mask][:]      
    # Read attributes
    lat = hf[latitude][:]
    lon = hf[longitude][:]

gcps = []

for i in range(0, 1000, 10):
    for j in range(0, 1000, 10):
        gcps.append(GCP(i, j, lon[i,j], lat[i,j]))

transform = from_gcps(gcps)
height, width = ds.shape

meta = {'driver': 'GTiff', 'dtype': 'uint16', 'nodata': 255, 'width': width, 'height': height, 'count': 1, 'crs': 4326, 'transform': transform}


with rasterio.open('landcover3.tif', "w", **meta) as dest:
    dest.write(ds.reshape(1,1000,1000))
