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
from reporting import descendant_groups, oeis_data_row_total_for_n, output_table

# default root folder for data
os.environ["POLYOMINO_DATA_FOLDER"] = "data"

#####################################################################
# Examples have been commented out, uncomment or cut/paste as desired
#####################################################################


# ensure folder structure in place within your chosen folder
# create_folder_structure()

# create data for n,k: note that file data must already exist for (n-1,k-1) and (n-1,k)
# For example:
# create_ancestors_nk(SquarePoly, Lattice, 1, 1)

# create a full T(n,k) set for a given limit on k
# create_data(SquarePoly, Plane, 1, 8)
# create_data(HexagonPoly, Plane, 1, 8)

# Output summary of results to console
# output_table(HexagonPoly, Plane, 8)
# output_table(SquarePoly, Plane, 8, k_limit=4)

# Visualise a polyomino in the console
# PolyShape.draw("327680-32768-65792-133632-65808-131616-262464-164352-21504", pixel="#")

# Get a feel for how generation splits between P(n+1,k) and P(n+1,k+1)
# As n increases more go to P(n+1,k+1) and less to P(n+1,k), eventually zero?
# d_dict = {}
# for n in range(3, 15):
#     d_dict[n] = descendant_groups(SquarePoly, Plane, n, 3)

# for n, (descendants_to_n1k0, descendants_to_n1k1) in d_dict.items():
#     print(n, len(descendants_to_n1k0), len(descendants_to_n1k1))
#     forced_to_k1 = set(descendants_to_n1k1) - set(descendants_to_n1k0)
#     for p in forced_to_k1:
#         PolyShape.draw(p)
#         print()

# Plot
# PolyShape.plot("327680-32768-65792-133632-65808-131616-262464-164352-21504")
# PolyShape.plot("262144-532480-1130496-655392-1048896-2097696-1053696-663552-81920")
# PolyShape.plot("10")
# PolyShape.plot("84-10-4")

create_data(SquarePoly, Plane, 1, 16, 3)
output_table(SquarePoly, Plane, 16, k_limit=3)
result = ", ".join(
    [str(x) for x in oeis_data_row_total_for_n(SquarePoly, Plane, 16, k_limit=3)]
)
print(result)

expected = "1, 1, 2, 4, 9, 18, 37, 62, 86, 78, 61, 34, 14, 4, 1, 0"
assert result == expected
