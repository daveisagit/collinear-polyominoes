"""Functions for reporting"""

from collections import defaultdict
from classes import Ancestor, CollinearityType, PolyShape, get_row_count


def get_summary(poly_class: PolyShape, collinearity: CollinearityType, max_m):
    """Return the summary counts as a dict keyed on (n,k)"""
    summary = defaultdict(int)
    for n in range(1, max_m + 1):
        for k in range(1, n + 1):
            file_path = poly_class.get_file_path(collinearity, Ancestor, n, k)
            row_count = 0
            try:
                with open(file_path, "r") as file_obj:
                    meta = file_obj.readline()
                    row_count = get_row_count(meta)
            except:
                pass
            summary[(n, k)] = row_count
    return summary


# def output_table(poly_type, N, plane=True, cell_width=10):
#     """Output a collinearity table n,k to console
#     and the values for OEIS Data"""
#     ploy_class = get_class(poly_type)
#     results_dict = {}
#     all_as_line = []
#     format_string = f"{cell_width}d"

#     for n in range(1, N + 1):
#         collinearity = load_collinearity_file(ploy_class, n)
#         results_dict[n] = collinearity

#     # titles
#     print()
#     if plane:
#         print(f"{ploy_class.file_name}|  Collinearity limit for any line in the plane")
#     else:
#         print(
#             f"{ploy_class.file_name}|  Collinearity limit only considered along lattice lines"
#         )
#     print("   |")

#     # header
#     print("   |  k")
#     line = " n | "
#     for k in range(1, N + 1):
#         line += f"{k:{format_string}}"
#     line = line.ljust(cell_width * N + 10)
#     line += "Total".rjust(cell_width)
#     print(line)
#     print("-" * len(line))

#     # data
#     for n in range(1, N + 1):
#         row_sum = 0
#         attrs = results_dict.get(n, {})
#         line = f"{n:2d} | "
#         for k in range(1, n + 1):
#             data = [
#                 id
#                 for id, (l_max, p_max) in attrs.items()
#                 if plane and p_max == k or not plane and l_max == k
#             ]
#             cnt = len(data)

#             all_as_line.append(cnt)
#             row_sum += cnt

#             line += f"{cnt:{format_string}}"

#         line = line.ljust(cell_width * N + 10)
#         line += f"{row_sum:{format_string}}"
#         print(line)
#     print()

#     # OEIS data
#     print("OEIS Data")
#     print()
#     print(", ".join(str(x) for x in all_as_line))
#     print()


def oeis_data(
    poly_class: PolyShape, collinearity: CollinearityType, max_m: int
) -> list:
    """Output OEIS Data"""
    summary = get_summary(poly_class, collinearity, max_m)
    oeis_data = []
    for n in range(1, max_m + 1):
        for k in range(1, n + 1):
            oeis_data.append(summary.get((n, k)))
    return oeis_data
