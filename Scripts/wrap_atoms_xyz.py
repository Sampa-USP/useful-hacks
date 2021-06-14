"""
Receives a xyz file and box length to apply PBC 
and wrap coordinates in a single direction.

Author: Henrique Musseli Cezar
Date: JUN/2021
"""

import os
import argparse
import sys

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

def wrap_coords(xyzfile, boxL, wrapidx):
  outxyz = ""

  with open(xyzfile, "r") as f:
    # read number of atoms and commentary
    line = f.readline()
    natoms = int(line.strip())
    outxyz += line
    outxyz += f.readline()

    # wrap coordinates
    for i in range(natoms):
      line = f.readline()
      sp, x, y, z = line.split()
      coords = [float(x), float(y), float(z)]
      if coords[wrapidx] < 0.:
        coords[wrapidx] += boxL
      outxyz += "{}\t{}\t{}\t{}\n".format(sp, coords[0], coords[1], coords[2])

    return outxyz

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Receives a xyz and length to wrap coordinates, applying PBC in a single direction.")
  parser.add_argument("xyzfile", type=extant_file, help="file in xyz format")
  parser.add_argument("boxL", type=float, help="box length of side to be wrapped")
  parser.add_argument("--axis", help="x, y or z (default = z)", default="z")

  args = parser.parse_args()

  lindex = {"x": 0, "y": 1, "z": 2}
  try:
    wrapidx = lindex[args.axis.lower()]
  except:
    sys.exit("Error: invalid axis")

  print(wrap_coords(args.xyzfile, args.boxL, wrapidx))
