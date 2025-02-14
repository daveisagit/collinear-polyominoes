"""Classes and supporting functions"""

import os
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
from numpy.linalg import matrix_rank
from matplotlib.patches import RegularPolygon
from math import radians, sin, sqrt
from operator import add, sub
from utils import draw_pattern, get_pattern_limits, scalar_multiply

ENCODING_SEPARATOR = "-"
R3O2 = sin(radians(60))
ROOT2 = sqrt(2)


def encoding_str_to_tuple(s: str):
    return [int(x) for x in s.split(ENCODING_SEPARATOR)]


def row_encode(cols: list) -> int:
    """Given a list of column indexes create an integer representation
    using reverse binary format
    For example
    @ @ : [0,2] = 101 = 5
     @@ : [1,2] = 011 = 6
    This gives a means to encode i.e. give the pattern an id
    """
    v = 0
    for i in cols:
        mask = 1 << i
        v |= mask
    return v


def row_decode(v: int) -> list:
    """Given an integer return the places where there are 1's
    the reverse binary format.
    For example
    @ @ : 5 = 101 = [0,2]
     @@ : 6 = 011 = [1,2]
    This gives the column indexes of the points"""
    cols = []
    idx = 0
    while v:
        if v & 1:
            cols.append(idx)
        idx += 1
        v = v >> 1
    return cols


def translate_points(points, vector):
    """Translate all point by the given vector"""
    return tuple(tuple(map(add, p, vector)) for p in points)


def are_parallel(*point_list):
    """Return True if points are collinear"""
    r = matrix_rank(point_list)
    return r <= 1


def get_row_count(line):
    """The header row contains Shape, CollinearityType, n, k and row count"""
    meta = line.split(",")
    row_count = meta[-1]
    row_count = int(row_count)
    return row_count


def create_folder_structure():
    data_folder = os.environ.get("POLYOMINO_DATA_FOLDER", "data")
    src_path = os.path.dirname(__file__)

    file_path = os.path.join(
        src_path,
        f"../{data_folder}",
        SquarePoly.file_name,
        Lattice.file_name,
    )
    os.makedirs(file_path, exist_ok=True)

    file_path = os.path.join(
        src_path,
        f"../{data_folder}",
        SquarePoly.file_name,
        Plane.file_name,
    )
    os.makedirs(file_path, exist_ok=True)

    file_path = os.path.join(
        src_path,
        f"../{data_folder}",
        HexagonPoly.file_name,
        Lattice.file_name,
    )
    os.makedirs(file_path, exist_ok=True)

    file_path = os.path.join(
        src_path,
        f"../{data_folder}",
        HexagonPoly.file_name,
        Plane.file_name,
    )
    os.makedirs(file_path, exist_ok=True)


class CollinearityType:
    file_name = "no_collinearity_type"

    @staticmethod
    def get_maximum_collinear(points, new_point, dimensions: int) -> int:
        """Returns the most number of collinear points going through the new point"""
        return 0


class Lattice(CollinearityType):
    file_name = "lattice"

    @staticmethod
    def get_maximum_collinear(pattern, new_point, dimensions: int) -> int:
        """Returns the most number of collinear points going through the new point"""
        max_collinear = 0
        for d in range(dimensions):
            collinear_count = len([p for p in pattern if p[d] == new_point[d]])
            max_collinear = max(collinear_count, max_collinear)
        return max_collinear


class Plane(CollinearityType):
    file_name = "plane"

    @staticmethod
    def get_maximum_collinear(pattern, new_point, dimensions: int) -> int:
        """Returns the most number of collinear points going through the new point"""

        # for a given pattern create a list of vectors from the new point
        # to every other point in the pattern
        vectors = [tuple(map(sub, p, new_point)) for p in pattern if p != new_point]

        # build a dict of sets, each set is a set of parallel vectors
        orthogonal = {}
        for v in vectors:
            new_value = True
            for o in orthogonal:
                if are_parallel(v, o):
                    orthogonal[o].add(v)
                    new_value = False
                    break
            if new_value:
                orthogonal[v] = {v}

        # the largest set gives the longest collinearity through the new point
        # we add 1 to include the new point
        return max([len(line) for line in orthogonal.values()]) + 1


class DataType:
    file_name = "no_file_type"

    @staticmethod
    def line_to_data(id: str, line_data: str):
        return None

    @staticmethod
    def data_to_line(id: str, line_data: str) -> str:
        pass


class Identifier(DataType):
    file_name = "ancestor"

    @staticmethod
    def line_to_data(line: str):
        """Return the integer tuple identifier"""
        arr = line.split(" ")
        id = arr[0]
        return id, encoding_str_to_tuple(id)


class Ancestor(DataType):
    file_name = "ancestor"

    @staticmethod
    def line_to_data(line: str):
        """Return the ancestors of a polyomino effectively directed edges
        where the edge data is the point being added from the perspective
        the larger descendent"""
        ancestors = {}
        tokens = line.split(" ")
        id = tokens[0]
        for ancestor in tokens[1:]:
            arr = ancestor.split(":")
            a_id = arr[0]
            arr = arr[1].split(",")
            p = tuple(int(x) for x in arr)
            ancestors[a_id] = p
        return id, ancestors

    @staticmethod
    def data_to_line(id: str, line_data: str) -> str:
        """Format our ancestors to a string
        <id> list-of-ancestors [id:rp]
        For example 7-6 7-2:1,2 7-4:1,1 6-3:0,2 3-3:0,0"""
        return f"{id} " + " ".join(
            [
                a_id + ":" + ",".join([str(x) for x in rp])
                for a_id, rp in line_data.items()
            ]
        )


def get_class(poly_type: str):
    """Return the class used for the type"""
    # origin
    if poly_type[0].upper() == "S":
        return SquarePoly

    if poly_type[0].upper() == "H":
        return HexagonPoly


class PolyShape:

    file_name = "no_shape"
    origin = (0, 0)
    vectors = []
    dimensions = 2
    symmetry = 1

    plot_orientation = 0
    plot_radius = 1
    plot_facecolor = "lightyellow"

    @classmethod
    def plot(cls, pattern, alt_cell=None, to_file=True, show_graph=True):

        marker_size = 10
        id = None
        if isinstance(pattern, str):
            id = pattern
        console_points = cls.pattern_to_points(pattern)

        edges = None
        if show_graph and id:
            gph = cls.get_graph(id)
            edges = cls.graph_to_plot(gph)
            marker_size = 30

        # adjustment from console row/col points
        # to matplotlib x,y
        plot_points = cls.console_to_plot(console_points)

        # we need to scale the marker based on the
        # physical space the polyomino takes up
        min_r, min_c, max_r, max_c = get_pattern_limits(plot_points)
        marker_scale = max((max_r - min_r), ((max_c - min_c)))
        marker_scale = (marker_size / marker_scale) ** 2

        fig, ax = plt.subplots(1)
        ax.set_aspect("equal")
        ax.axis("off")

        # Add some coloured cells
        for x, y in plot_points:
            cell = RegularPolygon(
                (x, y),
                numVertices=cls.symmetry,
                radius=cls.plot_radius,
                orientation=cls.plot_orientation,
                facecolor=cls.plot_facecolor,
                alpha=0.5,
                edgecolor="k",
                zorder=0,
            )
            ax.add_patch(cell)

        # Also add scatter points in cell centres
        X = [p[0] for p in plot_points]
        Y = [p[1] for p in plot_points]
        ax.scatter(X, Y, c="k", s=marker_scale * 2, zorder=20)

        # optional graph
        if edges:
            lc = LineCollection(edges, linewidth=3, zorder=10)
            ax.add_collection(lc)

        if to_file and id:
            fig.tight_layout()
            plt.savefig(f"{cls.file_name} {id}.png")
            return

        plt.show()

    @classmethod
    def point_to_doubled(cls, p):
        return p

    @classmethod
    def doubled_to_point(cls, p):
        return p

    @classmethod
    def points_to_doubled(cls, ps):
        return [cls.point_to_doubled(p) for p in ps]

    @classmethod
    def doubled_to_points(cls, ps):
        return [cls.doubled_to_point(p) for p in ps]

    @classmethod
    def encoder(cls, points) -> tuple:
        """Return a binary tuple encoding of the pattern"""
        min_r, _, max_r, _ = get_pattern_limits(points)
        encoded = ()
        for r in range(min_r, max_r + 1):
            cols = [p[1] for p in points if p[0] == r]
            v = row_encode(cols)
            encoded += (v,)
        return encoded

    @classmethod
    def decoder(cls, encoding: list) -> frozenset:
        """Return a pattern given a binary tuple encoding"""
        points = ()
        for ri, v in enumerate(encoding):
            cols = row_decode(v)
            for c in cols:
                p = ri, c
                points += (p,)
        return frozenset(points)

    @classmethod
    def flip_points(cls, points):
        """Reflect the pattern over vertical centre line through origin"""
        return tuple(cls.flip_point(p) for p in points)

    @classmethod
    def rotate_points(cls, points):
        """Returns points rotated"""
        points = tuple(cls.rotate_point(p) for p in points)
        return points

    @classmethod
    def generate_dihedral_symmetries(cls, points, ref):
        """Generator for the dihedral symmetries
        Yields the new set of points and the change to a reference point"""

        def generate_rotations(points, ref):
            for _ in range(cls.symmetry):
                points, ref = cls.normalise_position(points, ref)
                yield points, ref
                points = cls.rotate_points(points)
                ref = cls.rotate_point(ref)

        yield from generate_rotations(points, ref)
        points = cls.flip_points(points)
        ref = cls.flip_point(ref)
        yield from generate_rotations(points, ref)

    @classmethod
    def get_pattern_id(cls, new_pattern: frozenset, ref):
        """Given a pattern return its id.
        This is done by finding a preferred orientation and encoding the layout
        The preferred choice is arbitrary as long as its consistent and
        I have chosen the maximum encoding value since its guaranteed to be unique.

        The reference point is the new point being added to the existing pattern.
        We want to know where it ends with respect to the preferred orientation
        and return that as the "removal point". We call it the removal point
        because it is from the perspective of the new pattern.
        """
        pref_encoding = (0,)
        removal_point = None
        for new_pattern_sym, ref_sym in cls.generate_dihedral_symmetries(
            new_pattern, ref
        ):
            encoding = cls.encoder(new_pattern_sym)
            if encoding > pref_encoding:
                pref_encoding = encoding
                removal_point = ref_sym
                pref_pattern = new_pattern_sym

        return (
            ENCODING_SEPARATOR.join(str(v) for v in pref_encoding),
            removal_point,
            pref_pattern,
        )

    @classmethod
    def pattern_to_points(cls, pattern):
        """Return the row,col points as seen on a console image"""
        if isinstance(pattern, str):
            pattern = encoding_str_to_tuple(pattern)
        if isinstance(pattern, (list, tuple)):
            pattern = SquarePoly.decoder(pattern)
        return pattern

    @classmethod
    def plot_coordinates(cls, points):
        """Return the list of X and Y coordinates for matplotlib"""
        # Horizontal cartesian coords
        Y = [-p[0] for p in points]
        X = [2 * p[1] * R3O2 / 3 for p in points]  # good

    @classmethod
    def draw(cls, pattern, pixel="@"):
        """Draw the pattern given id, tuple or point set to console"""
        points = cls.pattern_to_points(pattern)
        draw_pattern(points, pixel=pixel)

    @classmethod
    def get_file_path(
        cls,
        collinearity: CollinearityType,
        file_type: DataType,
        n: int,
        k: int,
    ) -> str:
        """Returns a file path matching the inputs"""
        data_folder = os.environ.get("POLYOMINO_DATA_FOLDER", "data")
        file_name = f"{file_type.file_name}_{n:02d}_{k:02d}.txt"
        src_path = os.path.dirname(__file__)
        file_path = os.path.join(
            src_path,
            f"../{data_folder}",
            cls.file_name,
            collinearity.file_name,
            file_name,
        )
        return file_path

    @classmethod
    def save_to_file(
        cls,
        collinearity: CollinearityType,
        file_type: DataType,
        n: int,
        k: int,
        rows,
    ):
        """Save rows to a file. The rows argument is assumed to be some sequence of strings.
        The header row contains Shape, CollinearityType, n, k and row count"""
        file_path = cls.get_file_path(collinearity, file_type, n, k)
        with open(file_path, "w") as file_obj:
            meta = [
                cls.file_name,
                collinearity.file_name,
                str(n),
                str(k),
                str(len(rows)),
            ]
            file_obj.write(",".join(meta) + "\n")
            for id, line_data in rows.items():
                line = file_type.data_to_line(id, line_data)
                file_obj.write(line + "\n")

    @classmethod
    def start_loading(
        cls,
        collinearity_type: CollinearityType,
        data_file_type: DataType,
        n: int,
        k: int,
        total,
    ):
        """Output start loading message to console"""
        silent = os.environ.get("POLYOMINO_SILENT", False)
        if not silent:
            print(
                f"Loading {cls.file_name} {collinearity_type.file_name} {data_file_type.file_name} n={n} k={k} rows={total}"
            )

    @classmethod
    def get_graph(cls, pattern) -> dict:
        """Return a graph dict of set"""
        if isinstance(pattern, str):
            pattern = encoding_str_to_tuple(pattern)
        points = cls.decoder(pattern)
        gph = {p: set() for p in points}
        for p in points:
            for v in cls.vectors:
                np = tuple(map(add, p, v))
                if np in points:
                    gph[p].add(np)
        return gph

    @classmethod
    def graph_to_plot(cls, gph) -> list:
        edges = []
        for u, es in gph.items():
            u = cls.doubled_to_plot(cls.point_to_doubled(u))
            for v in es:
                v = cls.doubled_to_plot(cls.point_to_doubled(v))
                edges.append((u, v))
        return edges


####################################################################
# Implementations
####################################################################

#
# Square
#


class SquarePoly(PolyShape):

    title = "Square Polyonimoes"
    file_name = "square"
    origin = (0, 0)
    vectors = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    dimensions = 2
    symmetry = 4

    plot_orientation = radians(45)
    plot_radius = 1 / ROOT2
    plot_facecolor = "peru"

    @classmethod
    def doubled_to_plot(cls, d):
        """Convert to real values for plotting"""
        return d[1], -d[0]

    @classmethod
    def console_to_plot(cls, doubled_points):
        """Convert to real values for plotting"""
        return [cls.doubled_to_plot(p) for p in doubled_points]

    @classmethod
    def normalise_position(cls, points, ref):
        """Translate the pattern to the top left in a consistent fashion
        This will allow us to identify a unique pattern by its coordinate set.
        Included is the vector used to translate the points"""
        min_r = min(p[0] for p in points)
        min_c = min(p[1] for p in points)
        v = (-min_r, -min_c)
        points = translate_points(points, v)
        ref = tuple(map(add, ref, v))
        return points, ref

    @classmethod
    def flip_point(cls, p):
        """Reflect a point over vertical centre line through origin"""
        return -p[0], p[1]

    @classmethod
    def rotate_point(cls, p):
        """Rotate 90 ACW"""
        return -p[1], p[0]


#
# Hexagon
#


class HexagonPoly(PolyShape):

    title = "Hexagon Polyonimoes"
    origin = (0, 0, 0)
    file_name = "hexagon"
    vectors = [
        (1, 0, -1),
        (1, -1, 0),
        (0, -1, 1),
        (-1, 0, 1),
        (-1, 1, 0),
        (0, 1, -1),
    ]
    dimensions = 3
    symmetry = 6

    plot_radius = 2.0 / 3.0
    plot_facecolor = "lightgreen"

    @classmethod
    def doubled_to_plot(cls, d):
        """Convert to real values for plotting"""
        return (2 * d[1] * R3O2 / 3), -d[0]

    @classmethod
    def console_to_plot(cls, doubled_points):
        """Convert to real values for plotting"""
        return [cls.doubled_to_plot(p) for p in doubled_points]

    @classmethod
    def point_to_doubled(cls, p):
        return p[1], p[0] - p[2]

    @classmethod
    def doubled_to_point(cls, d):
        if d == (0, 1):
            pass
        return (d[1] - d[0]) // 2, d[0], (-d[1] - d[0]) // 2

    @classmethod
    def encoder(cls, points) -> tuple:
        """Return a binary tuple encoding of the pattern"""
        points = cls.points_to_doubled(points)
        return super().encoder(points)

    @classmethod
    def decoder(cls, encoding: list):
        """Return a pattern given a binary tuple encoding"""
        points = super().decoder(encoding)
        points = cls.doubled_to_points(points)
        return frozenset(points)

    @classmethod
    def normalise_position(cls, points, ref):
        """Translate the pattern to the top left in a consistent fashion
        This will allow us to identify a unique pattern by its coordinate set"""
        min_r = min(p[1] for p in points)
        v1 = scalar_multiply(cls.vectors[1], min_r)
        points = translate_points(points, v1)

        min_c = min(p[0] for p in points)
        v2 = scalar_multiply(cls.vectors[3], min_c)
        points = translate_points(points, v2)

        v = tuple(map(add, v1, v2))
        ref = tuple(map(add, ref, v))
        return points, ref

    @classmethod
    def flip_point(cls, p):
        """Reflect a point over vertical centre line through origin"""
        return p[2], p[1], p[0]

    @classmethod
    def rotate_point(cls, p):
        """Shift coordinates right and x-1"""
        return tuple(-p[(i - 1) % 3] for i in range(3))
