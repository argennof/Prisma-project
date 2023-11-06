import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import h5py
import os
import shutil
import numpy as np
import sys 
import geopandas as gpd
import argparse

# =============================================================================
# 1. Read data
# =============================================================================

def read_data_profile(filename,spectral_region,sensor,scale=True):
    """
    Goals: open-read and scale the data cube
    Parameters
    ----------
        filename: path and name of the dataset
        spectral_region: VNIR - SWIR - PAN
        sensor: choose between 'HCO','HRC'
    Returns-> np array with the scaled data cube,
    in original order (samples,bands, lines), and
    some extra information
    """
    sensor = sensor.upper()   
    if not os.path.exists(filename): 
        print(f'File {filename}, not found...\n')
        print(f'Check your path or file')
        sys.exit(1)
     
    prs_name = f'//HDFEOS/SWATHS/PRS_L1_{sensor}'
       
      
    with h5py.File(filename,  mode='r') as hf:
        if spectral_region.lower().endswith('_cube'):
            spectral_region = spectral_region[:-5] 
        # Paths:
        if len(spectral_region) == 4:
            
            sds = f'{prs_name}/Data Fields/{spectral_region.upper()}_Cube'
        
        elif len(spectral_region) > 4:
            sr = spectral_region.split('_') 
            sds = f'{prs_name}/Data Fields/{sr[0].upper()}_{"_".join(sr[1:])}_Cube'        
        else:
            print('Select a Data Cube')
         
        prs_hco = f'//HDFEOS/SWATHS/PRS_L1_HCO'  
            
        prod_msk_lc = f'{prs_hco}/Data Fields/LandCover_Mask'
        prod_msk_cm = f'{prs_hco}/Data Fields/Cloud_Mask'
        prod_err = f'{prs_hco}/Data Fields/{spectral_region[:4].upper()}_PIXEL_SAT_ERR_MATRIX'
         
         
        prod_lat = f'{prs_hco}/Geolocation Fields/Latitude_{spectral_region[:4].upper()}'
        prod_lon = f'{prs_hco}/Geolocation Fields/Longitude_{spectral_region[:4].upper()}'
         
        attrs = list(hf.attrs[f'List_Cw_{spectral_region[:4].capitalize()}'])
        wavelength = hf.attrs[f'List_Cw_{spectral_region[:4].capitalize()}']
                
        # Loading matrix
        landmask = hf[prod_msk_lc][:]
        cloudmask = hf[prod_msk_cm][:]
        err_mtx = hf[prod_err][:]
         
        lat = hf[prod_lat][:]
        lon = hf[prod_lon][:]
        #print('print sds',sds)
         
        ds = hf[sds][:].astype(np.single) 
          
        # Read attributes
        scale_factor = hf.attrs[f'ScaleFactor_{spectral_region[:4].capitalize()}']    
        offset = hf.attrs[f'Offset_{spectral_region[:4].capitalize()}']
            
    if scale:
        # Scaling data 
        cube = ds/scale_factor - offset
           
    return cube, wavelength, landmask, cloudmask, err_mtx, lat, lon

# =============================================================================
# Test
# =============================================================================

path = '/media/carito/Carito2/PRISMA/img/'
in_file = path +'PRS_L1_STD_OFFL_20191113101109_20191113101113_0001.he5'
# ~ sp_region_swirm = 'SWIR_poisson'
sp_region_swir = 'SWIR'
sp_region_vnir = 'VNIR'
sensor='HCO'

# ~ ds, wl_swir, ds_m_lc, ds_m_cm, err_swir, lat, lon = read_data_profile(in_file,'vnir','HRC')
ds, wl_swir, ds_m_lc, ds_m_cm, err_swir, lat, lon = read_data_profile(in_file,sp_region_swir,sensor) #
# ~ ds, wl_vnir, ds_m_lc, ds_m_cm, err_vnir,  lat, lon  = read_data_profile(in_file,sp_region_swirm,sensor)

ds_swir = ds[:,:-2,:]
err_swir = err_swir[:,:-2,:]

# ~ x = ds_swir.copy()
# ~ y = err_swir.copy()

ds_swir[err_swir != 0] = np.nan

lati = np.expand_dims(lat, axis=1)
longi = np.expand_dims(lon, axis=1)
landm = np.expand_dims(ds_m_lc, axis=1)
cloudm = np.expand_dims(ds_m_cm, axis=1)

# ~ stack_cube = np.hstack((lati,longi,landm,cloudm,x))
stack_cube = np.hstack((lati,longi,landm,cloudm,ds_swir))
stack_cube = np.transpose(stack_cube, axes=[2,0,1])
# ~ np.isnan(stack_cube).sum()
lines,samples,bands = stack_cube.shape

n_b = list(wl_swir[:-2])
name_bds = [str(i) for i in n_b]
name_bands = ['lat','lon','msk_land','msk_cloud'] + name_bds 

df = pd.DataFrame(stack_cube.reshape(-1,bands),columns=name_bands)
# ~ gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['lon'], df['lat'], crs = 'EPSG:4326'))
# ~ gdf.to_file(f'{sp_region_swir}_filtered.gpkg')
df.to_csv(f'./Results/{sp_region_swir}_filtered.csv', index=False, sep=',',)




values_m_lc = np.unique(ds_m_lc)
values_m_cm = np.unique(ds_m_cm)

sunglint_dict = {0: 'Notsunglint',
                  1: 'Sunglint_px',
                  10: 'For not of all previous classification',
                  255: 'error'}
                  
cloudmask_dict = {0: 'NotCloudy_px',
                  1: 'Cloud_px',
                  10: 'For not of all previous classification',
                  255: 'error'}
                  
landcover_dict = {0: 'Water',
                  1: 'Snow/ice',
                  2: 'Bare_soil',
                  3: 'Crop/rangeland',
                  4: 'Forst',
                  5: 'Wetland',
                  6: 'Urban_Component',
                  10: 'For not of all previous classification',
                  255: 'error'}

# =============================================================================
# Mask
# =============================================================================
fig, ax = plt.subplots(1,2, figsize=(12,6), sharex=True, sharey=True)
ax[0].set_xticks([])
ax[0].set_yticks([])
ax[1].set_xticks([])
ax[1].set_yticks([])
ax[0].grid(alpha=0.3), ax[1].grid(alpha=0.3)

cmap1 = mpl.colors.ListedColormap(['navy','cyan','tan','darkgreen','lightgreen', 'cornflowerblue', 'gray','white','black'])
bounds1 = [0, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 11, 255]
norm1 = mpl.colors.BoundaryNorm(bounds1, cmap1.N)
label_lm = [j for i, j in enumerate(landcover_dict.items())] # Labels

cmap2 = mpl.colors.ListedColormap(['gray','cyan','white','black'])
bounds2 = [0, 0.5, 1.5, 11, 255]
norm2 = mpl.colors.BoundaryNorm(bounds2, cmap2.N)
label_cm = [j for i, j in enumerate(cloudmask_dict.items())] # Labels

# land mask
msk_lc = ax[0].imshow(ds_m_lc, norm=norm1, cmap=cmap1, interpolation = 'nearest') 
# ~ msk_lc = ax[0].imshow(ds_m_lc, norm=norm1, cmap=cmap1) 
cbar_l = fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=cmap1), ax=ax[0], shrink=0.5, ticks=[0.25, 1, 2, 3, 4, 5, 6, 9.25, 122])
cbar_l.ax.set_yticklabels(label_lm)

# cloud mask
msk_c = ax[1].imshow(ds_m_cm, norm=norm2, cmap=cmap2, interpolation = 'nearest')
cbar_c = fig.colorbar(mpl.cm.ScalarMappable(norm=norm2, cmap=cmap2), ax=ax[1], shrink=0.5, ticks=[0.25, 1, 6.25, 122])
cbar_c.ax.set_yticklabels(label_cm)

ax[0].set_title('Land_Cover_Mask')
ax[1].set_title('Cloud_Mask')

fig.tight_layout()
plt.show()




class_cloudcover = [i for i in np.unique(ds_m_cm)  if i != 255 and i !=10]
rws = [] 
cls = []

for i in class_cloudcover:
    #print(f'Class_landcover: {i}')
    px_c = np.where(ds_m_cm==i)
    # print(px)
    
    # Extracting samples
    rw = px_c[0][0]  # first list, first position of the list
    cl = px_c[1][0]  # second list, first position of the list
    rws.append(rw)
    cls.append(cl)
    #print(f'Value: {ds_m_lc[row,col]}')  # other form to get the same value


df_c = pd.DataFrame(columns=['class_cloudcover', 'row', 'col'])
for i in class_cloudcover:
    print(f'Class_cloudcover: {i}')
    pxs = np.where(ds_m_cm==i)
    if i == 0:
        df_c = pd.concat([df_c, pd.DataFrame({'class_cloudcover': i, 'row': pxs[0][:], 'col': pxs[1][:]})], ignore_index=True)

prod_msk_lc = f'//HDFEOS/SWATHS/PRS_L1_HCO/Data Fields/LandCover_Mask'


mask_wl_swir = wl_swir != 0
# ~ mask_wl_vnir = wl_vnir != 0

def onclick(event):
    if event.button == 1:
         x = round(event.xdata)
         y = round(event.ydata)
          
    land_cover = ds_m_lc[y,x] 
    ax[1].clear()  # clear frame
    #ax[1].set_title(f'Profile: {prod_sr_swir}: row {y}, sample {x}') 
    ax[1].plot(wl_swir[mask_wl_swir],err_swir[y,:,x][mask_wl_swir],label=landcover_dict[land_cover])  # inform matplotlib of the new data
    ax[1].set_xlabel(f'Wavelength [$\lambda$]')
    ax[1].set_ylabel('Radiance')
     
    #ax[1].set_ylim(np.nanmin(ds_sr_swir), np.nanmax(ds_sr_swir)) 
    ax[1].legend()
    ax[1].grid(alpha=0.3)
    
    plt.draw()  # redraw


fig, ax = plt.subplots(1, 2, figsize=(12,6))

ax[0].set_xticks([])
ax[0].set_yticks([])
ax[0].grid(alpha=0.3), ax[1].grid(alpha=0.3)

cmap1 = mpl.colors.ListedColormap(['navy','cyan','tan','darkgreen','lightgreen', 'cornflowerblue', 'gray','white','black'])
bounds1 = [0, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 11, 255]
norm1 = mpl.colors.BoundaryNorm(bounds1, cmap1.N)
label_lm = [j for i, j in enumerate(landcover_dict.items())] # Labels
ax[0].set_title(f'Landcover: {prod_msk_lc}')
msk_lc = ax[0].imshow(ds_m_lc, norm=norm1, cmap=cmap1, interpolation = 'nearest') 
cbar_l = fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=cmap1), ax=ax[0],shrink=0.5, ticks=[0.25, 1, 2, 3, 4, 5, 6, 9.25, 122])
cbar_l.ax.set_yticklabels(label_lm)

# ~ ax[0].imshow(ds_m_lc, vmin=np.nanmin(values_m_lc), vmax=np.nanmax(values_m_lc[values_m_lc!=255]))

fig.canvas.mpl_connect('button_press_event', onclick)
plt.draw()
fig.tight_layout(pad=3.5)
plt.show()


aa = err_swir[:,mask_wl_swir,:]
plt.imshow(aa[:,-1,:])


pp = np.sum(aa[:,:-1,:], axis=1)

np.unique(pp)


plt.imshow(pp,vmax=5)
plt.colorbar()
plt.show()
