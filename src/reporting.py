"""Functions for reporting"""

from collections import defaultdict
from classes import Ancestor, CollinearityType, PolyShape, get_row_count
from generation import load_ancestors_nk, load_polyomino_patterns_nk
from utils import reverse_dag


def get_summary(poly_class: PolyShape, collinearity: CollinearityType, max_m):
    """Return the summary counts as a dict keyed on (n,k)"""
    summary = defaultdict(int)
    for n in range(1, max_m + 1):
        for k in range(1, n + 1):
            file_path = poly_class.get_file_path(collinearity, Ancestor, n, k)
            row_count = None
            try:
                with open(file_path, "r") as file_obj:
                    meta = file_obj.readline()
                    row_count = get_row_count(meta)
            except:
                pass
            summary[(n, k)] = row_count
    return summary


def output_table(
    poly_class: PolyShape,
    collinearity: CollinearityType,
    max_n: int,
    k_limit=None,
    cell_width=10,
):
    """Output a collinearity table n,k to console
    and the values for OEIS Data"""
    summary = get_summary(poly_class, collinearity, max_n)
    oeis = []
    format_string = f"{cell_width}d"

    # titles
    print()
    print(
        f"{poly_class.title} of size (n) with no more than (k) cells collinear on the {collinearity.file_name.title()}"
    )
    print()

    # header
    print("   |  k")
    line = " n | "
    k_stop = max_n + 1
    if k_limit:
        k_stop = k_limit + 1
    for k in range(1, k_stop):
        line += f"{k:{format_string}}"
    line = line.ljust(cell_width * (k_stop - 1) + 10)
    line += "Total".rjust(cell_width)
    print(line)
    print("-" * len(line))

    # data
    for n in range(1, max_n + 1):
        row_sum = 0
        line = f"{n:2d} | "
        k_stop = n + 1
        if k_limit:
            k_stop = k_limit + 1
        for k in range(1, k_stop):
            cnt = summary.get((n, k), 0)
            oeis.append(cnt)
            if cnt is None:
                line += " " * cell_width
            else:
                row_sum += cnt
                line += f"{cnt:{format_string}}"

        line = line.ljust(cell_width * (k_stop - 1) + 10)
        if row_sum:
            line += f"{row_sum:{format_string}}"
        print(line)

    print()


def oeis_data(
    poly_class: PolyShape, collinearity: CollinearityType, max_n: int
) -> list:
    """Output OEIS Data"""
    summary = get_summary(poly_class, collinearity, max_n)
    oeis_data = []
    for n in range(1, max_n + 1):
        for k in range(1, n + 1):
            oeis_data.append(summary.get((n, k), 0))
    return oeis_data


def descendants(poly_class: PolyShape, collinearity: CollinearityType, n, k):
    patterns_nk = load_polyomino_patterns_nk(poly_class, collinearity, n, k)
    ancestors_n1k0 = load_ancestors_nk(poly_class, collinearity, n + 1, k)
    ancestors_n1k1 = load_ancestors_nk(poly_class, collinearity, n + 1, k + 1)

    descendants_to_n1k0 = reverse_dag(ancestors_n1k0)
    descendants_to_n1k1 = reverse_dag(ancestors_n1k1)

    descendants_to_n1k0 = {
        id: d_dict for id, d_dict in descendants_to_n1k0.items() if id in patterns_nk
    }
    descendants_to_n1k1 = {
        id: d_dict for id, d_dict in descendants_to_n1k1.items() if id in patterns_nk
    }

    set_n1k0 = set(descendants_to_n1k0)
    set_n1k1 = set(descendants_to_n1k1)
    assert (set_n1k0 | set_n1k1) == set(patterns_nk)

    k_always_remains_unchanged = set_n1k0 - set_n1k1
    k_always_increases = set_n1k1 - set_n1k0
    both = set_n1k1 & set_n1k0

    return k_always_remains_unchanged, both, k_always_increases

    # descendants = descendants_to_n1k0
    # descendants.update(descendants_to_n1k1)
