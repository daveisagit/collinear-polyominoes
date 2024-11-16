"""Example code on how to use this"""

import os
from classes import (
    Lattice,
    Plane,
    PolyShape,
    SquarePoly,
    HexagonPoly,
    create_folder_structure,
)
from generation import create_ancestors_nk, create_data
from reporting import output_table

# default root folder for data
os.environ["POLYOMINO_DATA_FOLDER"] = "data"

# ensure folder structure in place within your chosen folder
create_folder_structure()

# create data for n,k: note that file data must already exist for (n-1,k-1) and (n-1,k)
# For example:
# create_ancestors_nk(SquarePoly, Lattice, 1, 1)

# create a full T(n,k) set for a given limit on k
# create_data(SquarePoly, Plane, 1, 16, 3)

# Output summary of results to console
output_table(HexagonPoly, Plane, 8)
output_table(SquarePoly, Plane, 20, k_limit=4)

# Visualise a polyomino in the console
PolyShape.draw("327680-32768-65792-133632-65808-131616-262464-164352-21504", pixel="#")
