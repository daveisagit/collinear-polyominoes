"""Code for exhaustively finding all the free hexagon polyominoes where there are no more
than 3 cell centres collinear anywhere on the plane.

From here on polyominoes to mean free hexagon polyominoes and "collinearity" to mean the maximum
number of cells that are collinear for a given polyomino.

Let P(n) define the set of all polyominoes with n cells.
Let P(n,k) define the set of polyominoes of n cells with and a collinearity of k.
See A378015 for the triangle sequence of these set sizes.

The code in the link of A378015 https://github.com/daveisagit/oeis/blob/main/hex_grid/connected_nodes.py
is not optimized to find higher values of n,k but is useful for observing the basic mechanics and method 
of the proof which is essentially a breadth first search to find all of P(n) given P(n-1) and disregarding
those breaking the collinearity limit.

v2
--

In order to discover higher values I have chosen to create a process which creates P(n,k) given
P(n-1,k-1) and P(n-1,k) since adding a cell can only increase the collinearity by 1 if at all.

For various reasons I have chosen to enumerate the polyominoes and save them to disk, so for each set
of P(n,k) there is related file called ancestor_n_k.txt with the set enumerated. Recording the ancestors
and the cell which was added to it enables a an optimisation in finding the collinearity, in that we only
need to check for lines going through the added cell.

Running the tests.py module asserts the expected results for A377941, A377942, A378014 and A378015.

The enumeration identifier is constructed by observing the pattern on a row/column grid using the 
doubled points coordinate system. This gives us a binary representation of each row, so the whole pattern
is represented as a tuple of integers.

Running the code
----------------

Requires 15Mb disk space (hopefully should not be an issue)

In your virtual environment 
pip install requirements.txt
and from within the repository root run
python ./src/A377756.py

Results are output to the console and the file content in ../data/A377756/hexagon/plane
can be used to verify any particular set of P(n,k) for n<=24 and k<=3.

Running this module on an Intel i7 laptop took just under 2 hours
(most of the time being spent around the peak 12 <= n <= 19).

If you need to terminate before completion then subsequent runs will pick up from the last saved file
and so once the whole process is complete running this will just output results.
"""

import os

from classes import HexagonPoly, Plane, create_folder_structure
from generation import create_data, load_polyomino_patterns_nk
from reporting import oeis_data_row_total_for_n, output_table

# set the location for the data files
os.environ["POLYOMINO_DATA_FOLDER"] = "data/A377756"

# ensure the folder structure is in place within your chosen folder
create_folder_structure()

# create a full P(n,k) set for n=24, k=3
# showing P(24,3) to be empty
# and proving the sequence A377756 is finite and the data full
create_data(HexagonPoly, Plane, 1, 24, 3)

# output the n/k table, A377756 is the row sums
output_table(HexagonPoly, Plane, 24, k_limit=3)

# assert the result matches submission
result = ", ".join(
    [str(x) for x in oeis_data_row_total_for_n(HexagonPoly, Plane, 24, k_limit=3)]
)
data_str = "1, 1, 3, 6, 18, 55, 169, 477, 1245, 2750, 5380, 8989, 12674, 14741, 13928, 10297, 6185, 2910, 1012, 289, 69, 12, 2, 0"
assert result == data_str
print(result)

# output the 2 examples of n=23
print()
print("2 examples of n=23")
examples = load_polyomino_patterns_nk(HexagonPoly, Plane, 23, 3)
for id in examples:
    print()
    print(id)
    HexagonPoly.draw(id)
