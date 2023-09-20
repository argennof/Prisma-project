# SAPP4VU: Sviluppo di Algoritmi prototipali Prisma per la Stima del Danno Ambientale e della Vulnerabilità alla Land Degradation
---- 

# ** "Implementazione di algoritmi numerico-statistici per la caratterizzazione e rimozione del rumore e per la cloud detection in immagini iperspettrali.” **
### Additive noise removal example:
![image](https://github.com/argennof/Prisma-proyect/assets/11649711/c0e57428-ca05-4da7-9b31-5a8507016270)

### Additive noise removal - zoom example:
![image](https://github.com/argennof/Prisma-proyect/assets/11649711/539ae08e-63de-491f-acdd-081db3c61bf2)

### Poisson noise removal example:
![image](https://github.com/argennof/Prisma-proyect/assets/11649711/dfc7823c-4781-45ef-8f9b-d1ba111301dd)


## Description
This repository contains the Python sources of the Prisma basic processing, based denoising code of the VSNR algorithm originally coded in MATLAB - see the [Pierre Weiss website](https://www.math.univ-toulouse.fr/~weiss/PageCodes.html) & [pyvsnr](https://github.com/patquem/pyvsnr/tree/main) and HySime (hyperspectral signal subspace identiﬁcation by minimum error, algorithm originally coded in MATLAB) - see the [José Bioucas-Dias website](http://www.lx.it.pt/~bioucas/code.htm)


## **Requirements**
   - [x] matplotlib==3.7.1
   - [x] h5py==3.8.0
   - [x] scipy
   - [x] numpy
   - [x] scikit-image==0.20.0
   - [x] pyvsnr==1.0.0
 

----
# How to run? 
----
  1. Create an environment, for instance:
  ```
    $ pip install virtualenv
    $ python3.1  -m venv <virtual-environment-name>
  ```
  
  2. Activate your virtual environment:
  ```
      $ source env/bin/activate
  ```
  3.  Install the requirements in the Virtual Environment, you can easily just pip install the libraries. For example:
  ```
      $ pip install pyvsnr
  ```
  or  If you use the requirements.txt file:
  ```
      $ pip install -r requirements.txt
  ```

  4. Download the scripts available here ( _*main.py_ and _*functions_he5.py_ ) and save them into the same directory.
  5. Then, execute the next command in a terminal:
 ```
      $ python main.py
  ```
  
  ----
  ### How it works?
  
![image](https://github.com/argennof/Prisma-proyect/assets/11649711/05c072a4-b8d7-4be7-9000-21372e2bf280)

  ----
  ### Usage
For a single image processing :
 
  ``` python

from pyvsnr import VSNR
from skimage import io

# read the image to correct
img = io.imread('my_image.tif')

# vsnr object creation
vsnr = VSNR(img.shape)

# add filter (at least one !)
vsnr.add_filter(alpha=1e-2, name='gabor', sigma=(1, 30), theta=20)
vsnr.add_filter(alpha=5e-2, name='gabor', sigma=(3, 40), theta=20)

# vsnr initialization
vsnr.initialize()

# image processing
img_corr = vsnr.eval(img, maxit=100, cvg_threshold=1e-4)
...
  ```


  ----
#  Authors information
This is adapted to Python from the original Matlab codes developed by:
 - [x] Jérôme Fehrenbach and Pierre Weiss.
 - [x] José Bioucas-Dias and José Nascimento

All credit goes to the original author.

In case you use the results of this code with your article, please don't forget to cite:

- [x] Fehrenbach, Jérôme, Pierre Weiss, and Corinne Lorenzo. "Variational algorithms to remove stationary noise: applications to microscopy imaging." IEEE Transactions on Image Processing 21.10 (2012): 4420-4430.
- [x] Fehrenbach, Jérôme, and Pierre Weiss. "Processing stationary noise: model and parameter selection in variational methods." SIAM Journal on Imaging Sciences 7.2 (2014): 613-640.
- [x] Escande, Paul, Pierre Weiss, and Wenxing Zhang. "A variational model for multiplicative structured noise removal." Journal of Mathematical Imaging and Vision 57.1 (2017): 43-55.
- [x] Bioucas-Dias, J. and  Nascimento, J.  "Hyperspectral subspace identification", IEEE Transactions on Geoscience and Remote Sensing, vol. 46, no. 8, pp. 2435-2445, 2008
