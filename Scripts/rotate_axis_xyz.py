"""
Receives a xyz file and rotate one axis into another.

Author: Henrique Musseli Cezar
Date: AUG/2020
"""

import os
import argparse
import sys
import numpy as np

# from https://stackoverflow.com/a/11541495
def extant_file(x):
  """
  'Type' for argparse - checks that file exists but does not open.
  """
  if not os.path.exists(x):
      # Argparse uses the ArgumentTypeError to give a rejection message like:
      # error: argument input: x does not exist
      raise argparse.ArgumentTypeError("{0} does not exist".format(x))
  return x


def readxyz(file):
  species = []
  atoms = []
  with open(file,"r") as f:
    try:
      natoms = int(f.readline())
    except:
      print("The first line of the xyz file should be the number of atoms")
      sys.exit(0)

    # skip comment and read atomic positions and species
    f.readline()
    for i, line in enumerate(f):
      species.append(line.split()[0])
      atoms.append(np.array([float(x) for x in line.split()[1:]]))

    # check consistency
    if i+1 < natoms:
      print("Error: Could not read %d atoms. Maybe you forgot the comment after the number of atoms?" % natoms)
      sys.exit(0)
    elif i+1 > natoms:
      print("Error: Read more than %d atoms. Check your .xyz file." % natoms)
      sys.exit(0)

  return species, np.array(atoms)


def writexyz(species, atoms):
  print("%d\n" % (len(species)))
  for sp, acoord in zip(species, atoms):
    print("%s\t%.6f\t%.6f\t%.6f" % (sp, acoord[0], acoord[1], acoord[2]))


# rotate v1 to v2 - expression from https://math.stackexchange.com/a/476311
def rotationmatrix(v1, v2):
  # make sure vectors are unit vectors
  uv1 = v1 / np.linalg.norm(v1)
  uv2 = v2 / np.linalg.norm(v2)

  # create rotation matrix
  v = np.cross(uv1,uv2)
  c = np.dot(uv1, uv2) # cosine of angle between vecs

  # if parallel or anti parallel just returns
  if (c == 1.) or (c == -1.):
    return np.identity(3) 

  # skew-symmetric cross product matrix
  vmx = np.array([[0.,-v[2],v[1]],[v[2],0.,-v[0]],[-v[1],v[0],0.]])

  # rotation matrix
  return np.identity(3) + vmx + (1./(1.+c))*np.dot(vmx,vmx)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Receives a xyz and rotate one axis into another")
  parser.add_argument("xyzfile", type=extant_file, help="file in xyz format")
  parser.add_argument("oaxis", help="original axis")
  parser.add_argument("taxis", help="target axis")

  args = parser.parse_args()

  axis = {"x": [1.,0.,0.], "y": [0.,1.,0.], "z": [0.,0.,1.]}
  
  orig_axis = args.oaxis.lower()
  target_axis = args.taxis.lower()

  if orig_axis not in ["x", "y", "z"]:
    print("The passed original axis is neither x, y or z")
    sys.exit(0)

  if target_axis not in ["x", "y", "z"]:
    print("The passed target axis is neither x, y or z")
    sys.exit(0)

  species, atoms = readxyz(args.xyzfile)

  # rotate
  R = rotationmatrix(axis[orig_axis], axis[target_axis])
  rotated = np.dot(atoms, R)

  writexyz(species, rotated)
