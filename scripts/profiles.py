import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import h5py
import os
import shutil
import numpy as np
import sys 

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
        
    with h5py.File(filename,  mode='r') as hf:
        if spectral_region.lower().endswith('_cube'):
            spectral_region = spectral_region[:-5] 
        # Paths:
        if len(spectral_region) == 4:
            
            sds = f'HDFEOS/SWATHS/PRS_L1_{sensor}/Data Fields/{spectral_region.upper()}_Cube'
        
        elif len(spectral_region) > 4:
            sr = spectral_region.split('_') 
            sds = f'HDFEOS/SWATHS/PRS_L1_{sensor}/Data Fields/{sr[0].upper()}_{"_".join(sr[1:])}_Cube'        
        else:
            print('Select a Data Cube')
            
        prod_msk_lc = f'//HDFEOS/SWATHS/PRS_L1_HCO/Data Fields/LandCover_Mask'
        prod_msk_cm = f'//HDFEOS/SWATHS/PRS_L1_HCO/Data Fields/Cloud_Mask'
        prod_err_vnir = f'//HDFEOS/SWATHS/PRS_L1_HCO/Data Fields/VNIR_PIXEL_SAT_ERR_MATRIX'
        prod_err_swir = f'//HDFEOS/SWATHS/PRS_L1_HCO/Data Fields/SWIR_PIXEL_SAT_ERR_MATRIX'
        
        attrs = list(hf.attrs['List_Cw_Swir'])
        wl_swir = hf.attrs['List_Cw_Swir']
        wl_vnir = hf.attrs['List_Cw_Vnir']
        
        # Loading matrix
        ds_m_lc = hf[prod_msk_lc][:]
        ds_m_cm = hf[prod_msk_cm][:]
        err_vnir = hf[prod_err_vnir][:]
        err_swir = hf[prod_err_swir][:]
        #print('print sds',sds)
        
        ds = hf[sds][:].astype(np.single) 
     
        # Read attributes
        scale_factor = hf.attrs[f'ScaleFactor_{spectral_region[:4].capitalize()}'] 
     
        offset = hf.attrs[f'Offset_{spectral_region[:4].capitalize()}']
     
    if scale:
        # Scaling data 
        ds = ds/scale_factor - offset
    
    return ds, wl_swir, wl_vnir, ds_m_lc, ds_m_cm, err_vnir, err_swir









# =============================================================================
# Test
# =============================================================================

path = '/media/carito/Carito2/PRISMA/img/'
in_file = path +'PRS_L1_STD_OFFL_20191113101109_20191113101113_0001.he5'
# ~ spectral_region_swirm = 'SWIR_poisson'
spectral_region_swir = 'SWIR'
spectral_region_vnir = 'VNIR'
sensor='HCO'

# ~ ds, wl_swir, wl_vnir, ds_m_lc, ds_m_cm, err_vnir, err_swir = read_data_profile(in_file,'vnir','HRC')
ds, wl_swir, wl_vnir, ds_m_lc, ds_m_cm, err_vnir, err_swir = read_data_profile(in_file,spectral_region_swir,sensor)
# ~ ds, wl_swir, wl_vnir, ds_m_lc, ds_m_cm, err_vnir, err_swir  = read_data_profile(in_file,spectral_region_swirm,sensor)



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


# =============================================================================
#  Extracting samples and Dataframe
# =============================================================================

# ~ # Land cover
# ~ # class_landcover = [i for i in np.unique(ds_m_lc)]

# ~ class_landcover = [i for i in np.unique(ds_m_lc)  if i != 255 and i !=10]
# ~ rows = [] 
# ~ cols = []

# ~ for i in class_landcover:
    # ~ #print(f'Class_landcover: {i}')
    # ~ px = np.where(ds_m_lc==i)
    # ~ # print(px)
    
    # ~ # Extracting samples
    # ~ row = px[0][0]  # first list, first position of the list
    # ~ col = px[1][0]  # second list, first position of the list
    # ~ rows.append(row)
    # ~ cols.append(col)
    # ~ #print(f'Value: {ds_m_lc[row,col]}')  # other form to get the same value


# ~ df = pd.DataFrame(columns=['Class_landcover', 'r', 'c'])
# ~ for i in class_landcover:
    # ~ print(f'Class_landcover: {i}')
    # ~ px = np.where(ds_m_lc==i)
    # ~ df = pd.concat([df, pd.DataFrame({'Class_landcover': i, 'r': px[0][:], 'c': px[1][:]})], ignore_index=True)




# Land cover
# class_landcover = [i for i in np.unique(ds_m_lc)]

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


sys.exit()


# =============================================================================
# Ploting Cubes: Modified and Normal
# =============================================================================

path = '//media/carito/Carito2/PRISMA/img/'
in_file = path +'PRS_L1_STD_OFFL_20210922101425_20210922101429_0001_denoised.he5'


ds_sr_swirm, wl_swir, wl_vnir, ds_m_lc, ds_m_cm = read_data_profile(in_file,'SWIR_additive_Cube',sensor, False) #  False when it is a result
ds_sr_swir, _, _, _, _ = read_data_profile(in_file,'SWIR_Cube',sensor)
ds_sr_vnir, _, _, _, _ = read_data_profile(in_file,'VNIR_Cube',sensor)


# Masking zero values in the vector
mask_wl_swir = wl_swir != 0
mask_wl_vnir = wl_vnir != 0


fig,ax = plt.subplots(1,2)
ax[0].set_title('SWIR_additive_Cube')
ax[1].set_title('SWIR_Cube')

ax[0].set_xlabel('Wavelength [\u03BB]' )
ax[0].set_ylabel('Radiance')

ax[1].set_xlabel(f'Wavelength [$\lambda$]')
ax[1].set_ylabel('Radiance')

y_min = np.inf
y_max = -np.inf

for i, land_cover in enumerate(class_landcover):
     
    val_swirm_a = ds_sr_swirm[rows[i], :, cols[i]]
    # ~ val_swirm_a = val_swirm_a[mask_wl_swir[:5]]
    val_swirm_a = val_swirm_a[mask_wl_swir[:]]
     
    # ~ val_swir    = ds_sr_swir[rows[i], :5, cols[i]]   
    # ~ val_swir    = val_swir[mask_wl_swir[:5]]  
    val_swir    = ds_sr_swir[rows[i], :, cols[i]]   
    val_swir    = val_swir[mask_wl_swir[:]]  
     
    y_min = y_min if y_min < np.min([val_swirm_a, val_swir]) else np.min([val_swirm_a, val_swir]) 
    y_max = y_max if y_max > np.max([val_swirm_a, val_swir]) else np.max([val_swirm_a, val_swir]) 
    
    # ~ ax[0].plot(wl_swir[mask_wl_swir][:5], val_swirm_a, label=landcover_dict[land_cover])
    # ~ ax[1].plot(wl_swir[mask_wl_swir][:5], val_swir, label=landcover_dict[land_cover])
    ax[0].plot(wl_swir[mask_wl_swir][:], val_swirm_a, label=landcover_dict[land_cover])
    ax[1].plot(wl_swir[mask_wl_swir][:], val_swir, label=landcover_dict[land_cover])


# ~ ax[0].set_ylim(y_min, y_max)
# ~ ax[1].set_ylim(y_min, y_max)
ax[0].legend()
ax[1].legend()

ax[0].grid(alpha=0.3)
ax[1].grid(alpha=0.3)

plt.show()


# =============================================================================
# Ploting Cube without correction
# =============================================================================


fig,ax = plt.subplots()
ax.set_title('ds_sr_swir - without correction')

ax.set_xlabel(f'Wavelength [$\lambda$]')
ax.set_ylabel('Radiance')

for i, land_cover in enumerate(class_landcover):
     
    val_swir = ds_sr_swir[rows[i], :, cols[i]]
    val_swir = val_swir[mask_wl_swir]  
     
    ax.plot(wl_swir[mask_wl_swir], val_swir, label=landcover_dict[land_cover])

ax.legend()
ax.grid(alpha=0.3)
plt.show()


# =============================================================================
# Animation: profile and Mask
# =============================================================================
prod_sr_swir = f'//HDFEOS/SWATHS/PRS_L1_{sensor}/Data Fields/SWIR_Cube'
prod_msk_lc = f'//HDFEOS/SWATHS/PRS_L1_HCO/Data Fields/LandCover_Mask'


def onclick(event):
    if event.button == 1:
         x = round(event.xdata)
         y = round(event.ydata)
          
    land_cover = ds_m_lc[y,x] 
    ax[1].clear()  # clear frame
    ax[1].set_title(f'Profile: {prod_sr_swir}: row {y}, sample {x}') 
    ax[1].plot(wl_swir[mask_wl_swir],ds_sr_swir[y,:,x][mask_wl_swir],label=landcover_dict[land_cover])  # inform matplotlib of the new data
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

