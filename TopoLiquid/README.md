# Generating a LAMMPS topology of a box of liquid water with pdb2lmp

In this tutorial we use [packmol](http://leandro.iqm.unicamp.br/m3g/packmol/home.shtml) and [pdb2lmp](https://github.com/Sampa-USP/pdb2lmp) to generate a topology of a box of liquid water to be read in LAMMPS with the `read_data` command.

The files necessary to complete this tutorial (as well as the output files) are present in this directory.

## Creating a box of liquid water with packmol
We start creating a with a 1000 molecules of water in the liquid phase. To find out the volume occupied by a single molecule of water, we calculate the molar volume V<sub>m</sub> = molar weight / density of water and divide by the Avogadro number. Considering a cubic volume, we can get the side of a box of that volume:

<img src="https://render.githubusercontent.com/render/math?math=L=%5Cleft(%5Cfrac%7B29915.81%7D%7B%5Crho%7D%5Cright)%5E%7B1%2F3%7D">Å

with <img src="https://render.githubusercontent.com/render/math?math=%5Crho"> being the water density (in kg/m<sup>3</sup>). If we consider 1000 kg/m<sup>3</sup>, we get L = 3.10432 Å, and if we consider that we want 1000 molecules in the box, we must multiply L by 1000<sup>1/3</sup>, obtaining that our box must have a 31.0432 Å side.

This information is provided in the `packmol.inp` file, in the `inside box` command. Read the commentaries in the `packmol.inp` file to understand how the box is created. Basically, packmol will use the configuration in the file `water.pdb` to create a box placing 1000 of these configurations randomly.
You can run packmol with:

```bash
packmol < packmol.inp > packmol.out
```

A `box.pdb` file will be created. You can visualize the box with your preferred software (VMD, Jmol, etc).

## Generating the topology from the PDB
With the `box.pdb` file you can generate the topology with `pdb2lmp`. To have a topology containing the correct atomic charges for the SPC/E water model, there is a `spce_charges.txt` file containing the atomic charges for the oxygen and hydrogen atoms within this model.

Run the command below and analyze the output file (`topo.lmp`):
```bash
python /path/to/pdb2lmp.py box.pdb --ignore-dihedrals --box-size 31.0432 31.0432 31.0432 --charges spce_charges.txt > topo.lmp
```

The `--ignore-dihedrals` option is used so the topology does not contain any information about dihedrals at all (as this water model has just 3 sites).

By running `pdb2lmp` as above, the script will use the provided box size box size. If you'd rather provide the box dimensions in your .pdb file, you can add the `CRYST1` line to the PDB file.
This is shown in the `mod_box.pdb` file. 
Using the `CRYST1` is necessary if your box is not orthogonal.
