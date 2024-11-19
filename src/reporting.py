"""Functions for reporting"""

from collections import defaultdict
from classes import Ancestor, CollinearityType, Identifier, PolyShape, get_row_count
from generation import load_ancestors_nk, load_data_file, load_polyomino_patterns_nk
from utils import reverse_dag


def get_summary(
    poly_class: PolyShape, collinearity: CollinearityType, max_m, default=None
):
    """Return the summary counts as a dict keyed on (n,k)"""
    summary = defaultdict(int)
    for n in range(1, max_m + 1):
        for k in range(1, n + 1):
            file_path = poly_class.get_file_path(collinearity, Ancestor, n, k)
            row_count = default
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
        k_stop = max_n + 1
        if k_limit:
            k_stop = k_limit + 1
        for k in range(1, k_stop):
            cnt = summary.get((n, k))
            oeis.append(cnt)
            if cnt is None:
                line += " " * cell_width
            else:
                row_sum += cnt
                line += f"{cnt:{format_string}}"
        line = line.ljust(cell_width * (k_stop - 1) + 10)
        line += f"{row_sum:{format_string}}"
        print(line)

    print()


def oeis_data_triangle(
    poly_class: PolyShape, collinearity: CollinearityType, max_n: int
) -> list:
    """Output OEIS Data for a triangle sequence"""
    summary = get_summary(poly_class, collinearity, max_n)
    oeis_data = []
    for n in range(1, max_n + 1):
        for k in range(1, n + 1):
            oeis_data.append(summary.get((n, k), 0))
    return oeis_data


def oeis_data_row_total_for_n(
    poly_class: PolyShape, collinearity: CollinearityType, max_n: int, k_limit=None
) -> list:
    """Output row totals"""
    summary = get_summary(poly_class, collinearity, max_n, default=0)
    oeis_data = []
    for n in range(1, max_n + 1):
        row_sum = 0
        k_stop = n + 1
        if k_limit:
            k_stop = k_limit + 1
        for k in range(1, k_stop):
            row_sum += summary.get((n, k), 0)
        oeis_data.append(row_sum)
    return oeis_data


def descendant_groups(poly_class: PolyShape, collinearity: CollinearityType, n, k):
    """Return the descendant groups of n,k as 2 dicts.
    Patterns from n,k that give rise to ones in n+1,k
    Patterns from n,k that give rise to ones in n+1,k+1
    """
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

    return descendants_to_n1k0, descendants_to_n1k1


def load_polyomino_patterns_n_le_k(
    poly_class: PolyShape, collinearity: CollinearityType, n: int, k: int
):
    """Load all polyomino patterns of a given size n"""
    polyominoes = {}
    for k in range(1, k + 1):
        k_dict = load_data_file(poly_class, collinearity, Identifier, n, k)
        polyominoes.update(k_dict)
    return polyominoes
