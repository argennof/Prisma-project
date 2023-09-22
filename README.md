# SAPP4VU: Sviluppo di Algoritmi prototipali Prisma per la Stima del Danno Ambientale e della Vulnerabilità alla Land Degradation
---- 

# 🚀 "Implementazione di algoritmi numerico-statistici per la caratterizzazione e rimozione del rumore e per la cloud detection in immagini iperspettrali.” **
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
   - [x] argparse
 

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

```diff - h ```


    Usage: 
      underscore <command> [--in <filename>|--data <JSON>|--nodata] [--infmt <format>] [--out <filename>] [--outfmt <format>] [--quiet] [--strict] [--color] [--text] [--trace] [--coffee] [--js]
  
    
  
    Commands:
  
      help [command]      Print more detailed help and examples for a specific command
      type                Print the type of the input data: {object, array, number, string, boolean, null, undefined}
      run <exp>           Runs arbitrary JS code. Use for CLI Javascripting.
      process <exp>       Run arbitrary JS against the input data.  Expression Args: (data)
      extract <field>     Extract a field from the input data.  Also supports field1.field2.field3
      map <exp>           Map each value from a list/object through a transformation expression whose arguments are (value, key, list).'
      reduce <exp>        Boil a list down to a single value by successively combining each element with a running total.  Expression args: (total, value, key, list)
      reduceRight <exp>   Right-associative version of reduce. ie, 1 + (2 + (3 + 4)). Expression args: (total, value, key, list)
      select <jselexp>    Run a 'JSON Selector' query against the input data. See jsonselect.org.
      find <exp>          Return the first value for which the expression Return a truish value.  Expression args: (value, key, list)
      filter <exp>        Return an array of all values that make the expression true.  Expression args: (value, key, list)
      reject <exp>        Return an array of all values that make the expression false.  Expression args: (value, key, list)
      flatten             Flattens a nested array (the nesting can be to any depth). If you pass '--shallow', the array will only be flattened a single level.
      pluck <key>         Extract a single property from a list of objects
      keys                Retrieve all the names of an object's properties.
      values              Retrieve all the values of an object's properties.
      extend <object>     Override properties in the input data.
      defaults <object>   Fill in missing properties in the input data.
      any <exp>           Return 'true' if any of the values in the input make the expression true.  Expression args: (value, key, list)
      all <exp>           Return 'true' if all values in the input make the expression true.  Expression args: (value, key, list)
      isObject            Return 'true' if the input data is an object with named properties
      isArray             Return 'true' if the input data is an array
      isString            Return 'true' if the input data is a string
      isNumber            Return 'true' if the input data is a number
      isBoolean           Return 'true' if the input data is a boolean, ie {true, false}
      isNull              Return 'true' if the input data is the 'null' value
      isUndefined         Return 'true' if the input data is undefined
      template <filename> Process an underscore template and print the results. See 'help template'
  
  
    Options:
  
      -h, --help            output usage information
      -V, --version         output the version number
      -i, --in <filename>   The data file to load.  If not specified, defaults to stdin.
      --infmt <format>      The format of the input data. See 'help formats'
      -o, --out <filename>  The output file.  If not specified, defaults to stdout.
      --outfmt <format>     The format of the output data. See 'help formats'
      -d, --data <JSON>     Input data provided in lieu of a filename
      -n, --nodata          Input data is 'undefined'
      -q, --quiet           Suppress normal output.  'console.log' will still trigger output.
      --strict              Use strict JSON parsing instead of more lax 'eval' syntax.  To avoid security concerns, use this with ANY data from an external source.
      --color               Colorize output
      --text                Parse data as text instead of JSON. Sets input and output formats to 'text'
      --trace               Print stack traces when things go wrong
      --coffee              Interpret expression as CoffeeScript. See http://coffeescript.org/
      --js                  Interpret expression as JavaScript. (default is "auto")
  

| Command | Description |
| --- | --- |
| `git status` | List all *new or modified* files |
| `git diff` | Show file differences that **haven't been** staged |

> :warning: **This is a Warning**: Description text here

> :memo: **This is a Note**: Description text here

> :bulb: **This is a Hint**: Description text here

> :heavy_check_mark: **Check**: Description text here

> :information_source: **Additional Information**: Description text here

>   <img alt="Info" src="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/dark-theme/info.svg">

  ----
# 📝 Authors information
This is adapted to Python from the original Matlab codes developed by:
 - [x] Jérôme Fehrenbach and Pierre Weiss.
 - [x] José Bioucas-Dias and José Nascimento

All credit goes to the original author.

In case you use the results of this code with your article, please don't forget to cite:

- [x] Fehrenbach, Jérôme, Pierre Weiss, and Corinne Lorenzo. "Variational algorithms to remove stationary noise: applications to microscopy imaging." IEEE Transactions on Image Processing 21.10 (2012): 4420-4430.
- [x] Fehrenbach, Jérôme, and Pierre Weiss. "Processing stationary noise: model and parameter selection in variational methods." SIAM Journal on Imaging Sciences 7.2 (2014): 613-640.
- [x] Escande, Paul, Pierre Weiss, and Wenxing Zhang. "A variational model for multiplicative structured noise removal." Journal of Mathematical Imaging and Vision 57.1 (2017): 43-55.
- [x] Bioucas-Dias, J. and  Nascimento, J.  "Hyperspectral subspace identification", IEEE Transactions on Geoscience and Remote Sensing, vol. 46, no. 8, pp. 2435-2445, 2008
