"""Code for generating the data files"""

import os
from collections import defaultdict
from operator import add
from classes import (
    ENCODING_SEPARATOR,
    Ancestor,
    CollinearityType,
    DataType,
    Identifier,
    PolyShape,
    get_row_count,
)
from utils import (
    progress_bar_freq,
    progress_bar_update,
)

# default root folder for data
os.environ["POLYOMINO_DATA_FOLDER"] = "data"


def load_data_file(
    poly_class: PolyShape,
    collinearity: CollinearityType,
    data_type: DataType,
    n: int,
    k: int,
) -> dict:
    """Load a file into a dict and return it"""
    data_dict = {}
    file_path = poly_class.get_file_path(collinearity, data_type, n, k)
    silent = os.environ.get("POLYOMINO_SILENT", False)

    try:
        with open(file_path, "r") as file_obj:
            meta = file_obj.readline()
            row_count = get_row_count(meta)
            if not silent:
                pbf = progress_bar_freq(row_count)
                poly_class.start_loading(collinearity, data_type, n, k, row_count)

            cnt = 0
            while line := file_obj.readline():
                line = line.strip()
                arr = line.split(" ")
                id = line.split(" ")[0]
                line_data = data_type.line_to_data(id, arr[1:])
                data_dict[id] = line_data
                cnt += 1
                if not silent and (cnt % pbf == 0 or cnt == row_count):
                    progress_bar_update(row_count, cnt)

    except FileNotFoundError:
        raise RuntimeError(
            f"{data_type.file_name} file for {poly_class.file_name} {collinearity.file_name} n={n} k={k} not found"
        )

    return data_dict


def load_polyomino_patterns_nk(
    poly_class: PolyShape, collinearity: CollinearityType, n: int, k: int
):
    """Return a dict of polyominoes loaded from file keyed on id.
    The value is a frozen sets of points"""
    return {
        id: poly_class.decoder(encoding)
        for id, encoding in load_data_file(
            poly_class, collinearity, Identifier, n, k
        ).items()
    }


def load_polyomino_patterns_n(
    poly_class: PolyShape, collinearity: CollinearityType, n: int
):
    """Load all polyomino patterns of a given size n"""
    polyominoes = {}
    for k in range(1, n + 1):
        k_dict = load_data_file(poly_class, collinearity, n, k)
        assert set(k_dict) & polyominoes == set()
        polyominoes.update(k_dict)
    return polyominoes


def load_ancestors_nk(
    poly_class: PolyShape, collinearity: CollinearityType, n: int, k: int
):
    """Return a dictionary keyed on id (str) where the value is a dict of ancestors value
    being additional point"""
    return {
        id: poly_class.decoder(encoding)
        for id, encoding in load_data_file(poly_class, collinearity, Ancestor, n, k)
    }


def create_ancestors_nk(
    poly_class: PolyShape, collinearity: CollinearityType, n: int, k: int
):
    """Return a dict of ancestors for a given n,k"""

    # Generate a dict of ancestors of a given type,n,k keyed on id

    # For k=n there is just the single row pattern (id=2^n-1) with
    # the only ancestor being id=2^(n-1)-1.

    # We need patterns from Patterns(n-1, k) and Patterns(n-1, k-1)

    # If adding an additional point to those patterns results in
    # k being the maximum number collinear going through that point,
    # then we include it as a newly generated pattern.

    # Symmetry is resolved during the process of obtaining the id
    # for the new pattern, in that symmetric patterns will have the
    # same id.

    # The working DAG of descendants is where we store the point
    # being added as the edge from the perspective of the descendent.

    # We then reverse that to form the ancestors DAG

    silent = os.environ.get("POLYOMINO_SILENT", False)

    # Seeded at the origin - single tile and has no ancestors
    # "1" is the encoding
    if n == 1:
        ancestors = {"1": {}}
        poly_class.save_to_file(collinearity, Ancestor, n, k, ancestors)
        return

    # load the previous sets
    same = {}
    if k < n:
        same = load_polyomino_patterns_nk(poly_class, collinearity, n - 1, k)
    prev = {}
    if k > 1:
        prev = load_polyomino_patterns_nk(poly_class, collinearity, n - 1, k - 1)
    assert set(prev) & set(same) == set()
    prev.update(same)
    if not prev:
        print(f"Previous set of {n-1} empty, so no more for k={k}")
        poly_class.save_to_file(collinearity, Ancestor, n, k, {})
        return

    # establish progress bar update frequency
    pbf = progress_bar_freq(len(prev))

    # DAG data structures for our working set and final result
    # edge data is the point added to the ancestor
    # from the ancestors perspective in the preferred orientation
    ancestors = defaultdict(dict)
    descendants = defaultdict(dict)
    cnt = 0

    if not silent:
        print(
            f"Generating {Ancestor.file_name} for {poly_class.file_name} {collinearity.file_name} n={n} k={k}"
        )

    for id, pattern in prev.items():

        cnt += 1
        if not silent and (cnt % pbf == 0 or cnt == len(prev)):
            progress_bar_update(len(prev), cnt)

        # for every node in that graph
        for p in pattern:

            # for ever possible neighbour of that node
            for v in poly_class.vectors:
                np = tuple(map(add, p, v))
                if np in pattern:
                    continue

                # a potential new pattern
                new_pattern = pattern | {np}
                d_id, removal_point, pref_pattern = poly_class.get_pattern_id(
                    new_pattern, np
                )

                # how does the new point (the removal point) affect collinearity
                max_collinear = collinearity.get_maximum_collinear(
                    pref_pattern, removal_point, poly_class.dimensions
                )

                if id in same:
                    if max_collinear > k:
                        continue
                else:
                    if max_collinear < k:
                        continue

                # add to the DAG of descendants
                descendants[id][d_id] = removal_point

    # ancestors is reversed DAG of descendants
    for id, d_dict in descendants.items():
        for d_id, removal_point in d_dict.items():
            ancestors[d_id][id] = removal_point

    poly_class.save_to_file(collinearity, Ancestor, n, k, ancestors)
