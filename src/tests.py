"""Run some end to end tests making sure the first terms of output match OEIS"""

import os
from classes import HexagonPoly, Lattice, Plane, SquarePoly, create_folder_structure
from generation import create_ancestors_nk
from reporting import oeis_data

os.environ["POLYOMINO_DATA_FOLDER"] = "temp"
max_n = 7


def answer_for_n(s: str, n) -> list:
    terms = n * (n + 1) // 2
    return [int(x) for x in s.split(", ")][:terms]


# ensure folder structure in place within temp
create_folder_structure()

# strings currently up to n=10
squ_lattice = "1, 0, 1, 0, 1, 1, 0, 2, 2, 1, 0, 1, 8, 2, 1, 0, 1, 17, 13, 3, 1, 0, 1, 39, 45, 19, 3, 1, 0, 1, 79, 182, 77, 25, 4, 1, 0, 1, 162, 607, 363, 114, 33, 4, 1, 0, 1, 301, 2004, 1539, 593, 170, 41, 5, 1"
squ_plane = "1, 0, 1, 0, 1, 1, 0, 2, 2, 1, 0, 0, 9, 2, 1, 0, 0, 18, 13, 3, 1, 0, 0, 37, 48, 19, 3, 1, 0, 0, 62, 200, 77, 25, 4, 1, 0, 0, 86, 678, 369, 114, 33, 4, 1, 0, 0, 78, 2177, 1590, 593, 170, 41, 5, 1"
hex_lattice = "1, 0, 1, 0, 2, 1, 0, 4, 2, 1, 0, 3, 15, 3, 1, 0, 5, 50, 23, 3, 1, 0, 1, 171, 126, 30, 4, 1, 0, 1, 506, 710, 187, 39, 4, 1, 0, 1, 1459, 3520, 1268, 270, 48, 5, 1, 0, 1, 3792, 16617, 7703, 1948, 364, 59, 5, 1"
hex_plane = "1, 0, 1, 0, 2, 1, 0, 4, 2, 1, 0, 2, 16, 3, 1, 0, 3, 52, 23, 3, 1, 0, 0, 169, 129, 30, 4, 1, 0, 0, 477, 740, 187, 39, 4, 1, 0, 0, 1245, 3729, 1274, 270, 48, 5, 1, 0, 0, 2750, 17578, 7785, 1948, 364, 59, 5, 1"

if max_n > 10:
    max_n = 10

# create all the files
for n in range(1, max_n + 1):
    for k in range(1, n + 1):
        create_ancestors_nk(SquarePoly, Lattice, n, k, overwrite=True)
        create_ancestors_nk(SquarePoly, Plane, n, k, overwrite=True)
        create_ancestors_nk(HexagonPoly, Lattice, n, k, overwrite=True)
        create_ancestors_nk(HexagonPoly, Plane, n, k, overwrite=True)


# assertions
assert oeis_data(SquarePoly, Lattice, max_n) == answer_for_n(squ_lattice, max_n)
assert oeis_data(SquarePoly, Plane, max_n) == answer_for_n(squ_plane, max_n)
assert oeis_data(HexagonPoly, Lattice, max_n) == answer_for_n(hex_lattice, max_n)
assert oeis_data(HexagonPoly, Plane, max_n) == answer_for_n(hex_plane, max_n)
