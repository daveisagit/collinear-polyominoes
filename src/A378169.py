"""Code for exhaustively finding all the free polyominoes where there are no more
than 3 cell centres collinear anywhere on the plane.

From here on polyominoes to mean free polyominoes and "collinearity" to mean the maximum
number of cells that are collinear for a given polyomino.

Let P(n) define the set of all polyominoes with n cells.
Let P(n,k) define the set of polyominoes of n cells with and a collinearity of k.
See A377942 for the triangle sequence of these set sizes.

Running the tests.py module asserts the expected results for A377941, A377942, A378014 and A378015.

Running this Module
-------------------

Requires less than 50Kb of disk space (hopefully should not be an issue)

In your virtual environment 
pip install requirements.txt
and from within the repository root run
python ./src/A378169.py

Results are output to the console and the file content in ../data/A378169/square/plane
can be used to verify any particular set of P(n,k) for n<=16 and k<=3.

"""

import os

from classes import Plane, SquarePoly, create_folder_structure
from generation import create_data, load_polyomino_patterns_nk
from reporting import oeis_data_row_total_for_n, output_table

# set the location for the data files
os.environ["POLYOMINO_DATA_FOLDER"] = "data/A378169"

# ensure the folder structure is in place within your chosen folder
create_folder_structure()

# create a full P(n,k) set for n=16, k=3
# showing P(16,3) to be empty
# and proving the sequence A378169 is finite and the data full
create_data(SquarePoly, Plane, 1, 16, 3)

# output the n/k table, A378169 is the row sums
output_table(SquarePoly, Plane, 16, k_limit=3)

# assert the result matches submission
result = ", ".join(
    [str(x) for x in oeis_data_row_total_for_n(SquarePoly, Plane, 16, k_limit=3)]
)
data_str = "1, 1, 2, 4, 9, 18, 37, 62, 86, 78, 61, 34, 14, 4, 1, 0"
assert result == data_str
print(result)

# output the example of n=15
print()
print("example of n=15")
examples = load_polyomino_patterns_nk(SquarePoly, Plane, 15, 3)
for id in examples:
    print()
    print(id)
    SquarePoly.draw(id, pixel="#")
