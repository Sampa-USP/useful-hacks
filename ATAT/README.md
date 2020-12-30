# Using the ATAT package to generate SQS structures

# Aim of this tutorial

Special quasi-random structures (SQS) are employed to estimate the physical and electronic properties of disordered materials, such as solid solutions (e.g., Si-Ge, HEAs, and metallic materials in general). This tutorial provides a step-by-step guide to generate an SQS (and evaluate it) via the ATAT package.

In summary, we use two scripts - **corrdump** and **mcsqs** - to generate the SQS. The job can be executed offline, in a regular PC, and does not require integration with VASP, QE or similar (at this stage).

# Compiling ATAT

ATAT current version (3.36) requires g++ 2.72 or later, and GNU make to compile. Before compiling, it is recommended to update/install the following packages: **xsltproc**, **perl**, **python-pip** and **csh**.

To download the last (stable) version of ATAT, please check the ATAT [official page](https://www.brown.edu/Departments/Engineering/Labs/avdw/atat/).

Please refer to the [ATAT manual](https://www.brown.edu/Departments/Engineering/Labs/avdw/atat/manual/manual.html) in case of any problems compiling the code.


## Preparing the structure input file

We need a structure input file named *rndstr.in* to run *corrdump*. An example of such a file is presented below.

```
1 1 1.633 90 90 60
2 0 0
0 2 0
0 0 1
0.000000 0.000000 0.0 Cr
0.000000 1.000000 0.0 Ni=.333333,Fe=.333333,Co=.333334
1.000000 0.000000 0.0 Ni=.333333,Fe=.333333,Co=.333334
1.000000 1.000000 0.0 Ni=.333333,Fe=.333333,Co=.333334
0.666667 0.666667 0.5 Cr
1.666667 0.666667 0.5 Ni=.333333,Fe=.333333,Co=.333334
0.666667 1.666667 0.5 Ni=.333333,Fe=.333333,Co=.333334
1.666667 1.666667 0.5 Ni=.333333,Fe=.333333,Co=.333334
```

Reading the file from the top to the bottom: the first line defines a coordinate system (Cartesian, as three vectors and three angles); the following lines define the periodic (or primitive) cell expressed in the given coordinate system; finally, float variables (0.000000) define each lattice site (the atomic positions). Concentrations of atomic sites are limited to 6 significant digits. The sum of concentration must always be 1.

As for the lattice in the example above, Cr atoms occupy specific positions, generating a partially-ordered structure, common in intermetallic compounds. In the case of (true) random cells (i.e., atoms can fill any position), the input file can be simplified as follows:

```
1 1 1 90 90 90
0 0.5 0.5
0.5 0 0.5
0.5 0.5 0
0 0 0 Cu,Au
```

Which is an FCC random solid-solution of Cu and Au (50 at%). Either Cu or Au can occupy any of the lattice sites. We notice that all input files use 1 as lattice parameter, which makes it easier to set the parameters to run *corrdump*. We will be able to change it to the real lattice parameter afterward.

## Running *corrdump*

*Corrdump* uses the structure file to check all symmetry operations and permutations of the original cell, which is later written in *clusters.out*. The most relevant parameter of *corrdump* is the -2 attribute, which defines the cut-off distance to the calculation of the pair-correlation functions. I recommend you to set -2 = 1.1 to include first and second nearest neighbors in BCC, FCC and HCP based structures. The -3 attribute does the same for triplets interactions. I recommend something between 1.2 and 1.8, depending on the structure and how many neighbors are to be included in the optimization. To run *corrdump* with this setup:

```bash
corrdump -l=rndstr.in -ro -noe -nop -clus -2=1.1 -3=1.5
```

## Running *mcsqs*

The *mcsqs* command generates random structures using a Monte-Carlo based algorithm, with a defined supercell size, and sort these structures based on a pair correlation function. The *mcsqs* code can run indefinitely, depending on the complexity of the system. Since it is a Monte-Carlo based algorithm, one can run multiple seeds to accelerate the process of generation of SQSs.

There are two ways of running this script.

## Searching for an SQS based on the number of atoms

In this case, the number of atoms must be passed on to "-n" - e.g., 16 atoms:

```bash
mcsqs -n 16
```

This command enables us to adjust composition precisely the way we want, however, might lead to a non-symmetrical SQS, with long lattice vectors and sharp angles, which are not ideal for DFT calculations.

## Searching for a preset supercell

With this resource, it is possible to control the shape of the SQS setting specific lattice vectors in the sqscell.out file and then running the *mcsqs* as -rc (which is used to restart a job).

```bash
mcsqs -rc
```
For example, to build a 2-2-2 fcc supercell (32 atoms), **sqscell.out** should be:

```
1
2 0 0
0 2 0
0 0 2
```
The *mcsqs* code saves the best SQS structure it could find as **bestsqs.out**. It also saves an interesting log file, with all of the tested SQS and their pair-correlation function.

## Converting the final SQS

You can use the script provided by Prof. Liu to convert the SQS to POSCAR (Direct): https://github.com/changning/sqs2poscar - once you have a POSCAR file, it is easy to visualize it with p4v, VESTA, or any other similar software. It is recommended to always visualize your structure before running DFT calculations of any sort. Don't forget to alter the lattice parameter before visualizing or performing further calculations with the structure you generated.

# Advanced
[Dr. Changning Liu](https://cniu.me/) performed a few modifications in the original code to improve overall functionality. These modifications are listed below:

1. If you want to save all the SQS structures and not only the (last) best one, before compiling ATAT add the following lines to

```bash
gedit atat/src/mcsqs.c++
```

```c++
int tic=0;
Real obj=best.obj;
best.obj=MAXFLOAT;
int count_cniu=1;                                       // added by cniu
while (1) {
  if (obj<best.obj) {
    // cerr << "Best" << endl;
    best=mc(cc);
    ofstream strfile;
    stringstream out_cniu;                              // added by cniu
    out_cniu << count_cniu++;                           // added by cniu
    std::string str1_cniu = "bestsqs-";                 // added by cniu
    str1_cniu += out_cniu.str();                        // added by cniu
    std::string str2_cniu = "bestcorr-";                // added by cniu
    str2_cniu += out_cniu.str();                        // added by cniu
    char *cstr1_cniu = new char[str1_cniu.length()+1];  // added by cniu
    char *cstr2_cniu = new char[str2_cniu.length()+1];  // added by cniu
    strcpy(cstr1_cniu,str1_cniu.c_str());               // added by cniu
    strcpy(cstr2_cniu,str2_cniu.c_str());               // added by cniu
    open_numbered_file(strfile,cstr1_cniu,ip,".out");   // changed by cniu
    delete [] cstr1_cniu;                               // added by cniu
    strfile.setf(ios::fixed);
    strfile.precision(sigdig);
    write_structure(best.str,ulat,site_type_list,atom_label,axes,strfile);
    ofstream corrfile;
    open_numbered_file(corrfile,cstr2_cniu,ip,".out");  // changed by cniu
    delete [] cstr2_cniu;                               // added by cniu
    corrfile.setf(ios::fixed);
    corrfile.precision(sigdig);
    }
```

Then, save it and compile it with your preferred c++ compiler. Keep in mind that after this modification, the code will save many **bestsqs-i.out** files.

2. It is possible to use *mcsqs -n NN* to generate SQS of varied shape, stop it, then use the python script **trim.py** (by Prof. Liu) to search for symmetric cells in **sqscell.out**, trim the others out of it, and finally restart the code with *mcsqs -rc*.

```python
#! /usr/bin/env python
#
# trim.py
# This script is written for Python 2.7.13.
#
# It copies sqscell.out (generated by mcsqs) to old-sqscell.out.
# Then trim the sqscell.out to three or fewer cells. All cells have
# equal-length lattice vectors. If more than three cells like this
# exist in the original sqscell.out, it keeps three cells with the
# smallest vector lengths.
import numpy as np

# Read the original file
with open('sqscell.out') as f1:
    lines = f1.readlines()

# Save the original file
with open('old-sqscell.out', 'w') as f2:
    for x in lines: f2.write(x)

# Replace it with a new file with 3 cells.
# The 3 cells have the smallest and equal vector lengths
with open('sqscell.out', 'w') as f3:
    tot = int(lines[0].split()[0])  # total number of cells
    count = 0
    arr1 = np.zeros((tot, 2))
    for i in range(tot):
        arr1[i][0] = i
        a1, a2, a3 = [ float(x) for x in lines[4*i+2].split() ]
        b1, b2, b3 = [ float(x) for x in lines[4*i+3].split() ]
        c1, c2, c3 = [ float(x) for x in lines[4*i+4].split() ]
        l1 = (a1**2 + a2**2 + a3**2)**.5
        l2 = (b1**2 + b2**2 + b3**2)**.5
        l3 = (c1**2 + c2**2 + c3**2)**.5
        if l1 == l2 and l2 == l3:
            arr1[i][1] = l1
            count += 1
    arr1 = arr1[arr1[:,1].argsort()]
    if count >= 3:
        j = 0
        f3.write('3\n\n')
        for i in range(tot):
            if arr1[i][1] > 0 and j < 3:
                f3.write(lines[4*int(arr1[i][0])+2])
                f3.write(lines[4*int(arr1[i][0])+3])
                f3.write(lines[4*int(arr1[i][0])+4] + '\n')
                j += 1
    else:
        f3.write(str(count) + '\n\n')
        for i in range(tot):
            if arr1[i][1] > 0:
                f3.write(lines[4*int(arr1[i][0])+2])
                f3.write(lines[4*int(arr1[i][0])+3])
                f3.write(lines[4*int(arr1[i][0])+4] + '\n')
```

# References
This tutorial is a simplified version of this [base tutorial](http://cniu.me/2017/08/05/SQS.html), by Dr. Changning Niu, from [QuesTek Innovations LLC](https://www.questek.com/). 

Other useful references are:

- Niu et al 2018, [arXiv:1811.04092](https://arxiv.org/abs/1811.04092)
- [The ATAT manual](https://www.brown.edu/Departments/Engineering/Labs/avdw/atat/manual/manual.html)
- [The ATAT users forum](https://www.brown.edu/Departments/Engineering/Labs/avdw/forum/)
- Ed. M. C. Gao, J. W. Yeh, P. K. Liaw, Y. Zhang, "High-Entropy Alloys", Chapter 10: Applications of Special Quasi-random Structures to High-Entropy Alloys, Springer, 2016

## If you have used the ATAT package to generate an SQS for a publication, please cite:
A. Van de Walle, P. Tiwary, M. de Jong, D.L. Olmsted, M. Asta, A. Dick, D. Shin, Y. Wang, L.-Q. Chen, Z.-K. Liu, Efficient stochastic generation of special quasi-random structures, Calphad Journal 42, pp. 13-18 (2013), [link](https://doi.org/10.1016/j.calphad.2013.06.006)

## Glossary and file structure
- ATAT - alloy automoted theorical toolkit (software)
- SQS - special quasi-random structures (term)
- HEA - high-entropy alloys (term)
- rndstr.in - the structure input (file)
- bestsqs.out - the best sqs obtained (file)

#### -- version 0.2, 2019 --
