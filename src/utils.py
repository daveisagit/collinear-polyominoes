"""Various utility functions"""

from collections import defaultdict


PROGRESS_BAR_FREQ = 2  # as %


def progress_bar(
    iteration,
    total,
    prefix="",
    suffix="",
    decimals=1,
    length=100,
    fill="█",
    printEnd="\r",
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def progress_bar_freq(total: int):
    """How many rows before we update the progress bar"""
    prog_m = PROGRESS_BAR_FREQ * total // 100
    if prog_m == 0:
        prog_m = 1
    return prog_m


def progress_bar_update(total, cnt):
    """Update the progress bar"""
    progress_bar(cnt, total, prefix="Progress:", suffix="Complete", length=50)


def scalar_multiply(v, s):
    return tuple(x * s for x in v)


def get_pattern_limits(pattern):
    """Return the rol,col limits of the cartesian grid points"""
    min_r = min(p[0] for p in pattern)
    min_c = min(p[1] for p in pattern)
    max_r = max(p[0] for p in pattern)
    max_c = max(p[1] for p in pattern)
    return min_r, min_c, max_r, max_c


def draw_pattern(points, pixel="@"):
    """Visualise a pattern of nodes on the console"""
    min_r, min_c, max_r, max_c = get_pattern_limits(points)
    for r in range(min_r, max_r + 1):
        row = ""
        for c in range(min_c, max_c + 1):
            p = r, c
            c = " "
            if p in points:
                c = pixel
            row += c
        print(row)


def reverse_dag(g):
    """Return the reverse of the directed graph"""
    rg = defaultdict(dict)
    for u, edges in g.items():
        for v, p in edges.items():
            rg[v][u] = p
    return rg
