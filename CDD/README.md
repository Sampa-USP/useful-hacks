# Charge density difference (CDD) with VASP

This is a brief tutorial on how to obtain charge density difference (CDD) plots using VASP. The principles are roughly the same for all DFT packages. Visualization will be done with VESTA. 


## Step 1: geometry optimization (ionic relaxation)

I am assuming you already have obtained an optimized geometry before starting this tutorial. If the optimized geometry was obtained using other DFT package, pseudopotentials, or parameters other than the desired ones, run a geometry optimization with the following INCAR file:

```
PREC = Accurate
ENCUT = 600      # 2x the largest CUTOFF in your POTCAR file should be good
NSW = 400        # in case you want to limit the number of allowed ionic steps
EDIFF = 10-6     # electronic break condition  
EDIFFG = -0.01   # ionic relaxation break condition
ISIF = 2         # 2 degrees of freedom (ions & cell vol; cell shape will NOT change);
IBRION = 2       # conjugate gradient algo
```

Include **NCORE = 4** if you are running calculations on a cluster with 2^N clusters

## Step 2: self consistent calculations (SCF)

With the optimized geometry in hand, perform a single electronic SCF. If you are analyzing a single molecule, you will need to perform at least 2 calculations(i.e. reference and final state). If you are working with a surface, catalyst, or any other complex system, the charge of isolated and combined molecules should be assessed. For all of these calculations, remember to always use the same atomic positions (e.g. from the combined system after relaxation). 
 
```
PREC = Accurate
ENCUT = 600      # 2x the largest CUTOFF in your POTCAR file should be good
NSW = 0          # no ionic steps, i.e. no ionic relaxation
EDIFF = 1E-6     # electronic break condition  
IBRION = -1      # ions are not moved
LCHARG = .TRUE.  # CHGCAR will be recorded
LAECHG = .TRUE.  # all-electron charge densities will be recorded (AECCAR0, 1, 2)
```

Obs: It is important to use a fine K-POINTS mesh in these calculations to get a good resolution in the CDD plots. Try to use equivalent K-POINTS among the structures, rounded up. LAECHG might be useful if you need to calculate BADER charge afterwards.

Rename the CHGCAR files to simplify the job. I will be reffering to them as CHGCAR_ref and CHGCAR_final to reference and final states, respectively.

## Step 3: charge density difference analysis (CDD)

In VESTA, first open the CHGCAR_final to load the final state charges. Then, go to **Edit > Edit Data > Volumetric data > Import** and select CHGCAR_ref. In the "Choose operations" box, choose **Subtract from current data** and select the appropriate unit conversion if you need (stardard data is in e/Bohr3). If you are working with many molecules, repeat *step 3* until all reference structures have been subtracted.

In the left-hand panel, click on **Style > Properties** to modify isosurface settings such as min and max values, opacity, colors, etc. Save a *.vesta* file as a backup and export the final image as TIFF or PNG. 

## Common mistakes

Always concatenate the pseudopotentials (in the POTCAR file) in the same order the atoms are called in the POSCAR file. To check if the order is correct use **grep**, ex:
 
```bash
grep 'PAW_PBE' POTCAR
$  PAW_PBE Ti_pv 07Sep2000
$    TITEL  = PAW_PBE Ti_pv 07Sep2000
$  PAW_PBE Nb_pv 08Apr2002
$    TITEL  = PAW_PBE Nb_pv 08Apr2002
```
 In this example the order should be: Ti, Nb. 

## Additional info

Reference KPOINTS file

```
k-points
0
M
9 9 9
0 0 0
```