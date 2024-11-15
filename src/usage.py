"""Example code on how to use this"""

import os
from classes import Lattice, SquarePoly, create_folder_structure
from generation import create_ancestors_nk

# default root folder for data
os.environ["POLYOMINO_DATA_FOLDER"] = "data"

# ensure folder structure in place within your chosen folder
create_folder_structure()

# create an arbitrary ancestors file
# create_ancestors_nk(SquarePoly, Lattice, 4, 3)

# create a full T(n,k) set for a given n
for n in range(1, 11):
    for k in range(1, n + 1):
        create_ancestors_nk(SquarePoly, Lattice, n, k)
