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


def example_data_for_nk():
    """To create data for entry (n=8, k=5) the square lattice sequence A377941"""
    create_ancestors_nk(SquarePoly, Lattice, 8, 5)


def example_all_sets_to_n(n):
    """Create T(n,k) for all types up n"""
    create_data(SquarePoly, Lattice, 1, n)
    create_data(HexagonPoly, Lattice, 1, n)
    create_data(SquarePoly, Plane, 1, n)
    create_data(HexagonPoly, Plane, 1, n)


def example_output_result_tables_to_n(n):
    """Output result tables to n"""
    output_table(SquarePoly, Lattice, n)
    output_table(HexagonPoly, Lattice, n)
    output_table(SquarePoly, Plane, n)
    output_table(HexagonPoly, Plane, n)


def example_output_result_a378169():
    """Output result tables with k limited"""
    output_table(SquarePoly, Plane, 16, k_limit=3)


def example_visual_on_console():
    """Visualise a polyomino in the console"""
    PolyShape.draw("112-28-7-44-56", pixel="#")


def example_visual_using_matplotlib():
    """Visualise a polyomino in the console"""
    # SquarePoly.plot("112-28-7-44-56", to_file=False)
    # SquarePoly.plot("14-12-7-2", to_file=False)
    # HexagonPoly.plot("1344-42-336", to_file=False)
    # HexagonPoly.plot("5376-2688-336-8", to_file=False)
    # SquarePoly.plot("28-24-14-6", to_file=False)

    # Isaac
    # HexagonPoly.plot(
    #     "327680-32768-65792-133632-65808-131616-262464-164352-21504", to_file=False
    # )

    # Elliott
    # HexagonPoly.plot(
    #     "262144-532480-1130496-655392-1048896-2097696-1053696-663552-81920",
    #     to_file=False,
    # )


example_visual_using_matplotlib()
