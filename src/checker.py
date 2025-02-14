from classes import HexagonPoly, Plane


pattern = """
......@.@.@.....
.....@.....@.@..
..@.@.........@.
.@.............@
........@.@...@.
.......@...@.@..
........@.@.....
"""
pattern = """
...@...........
@.@............
...@.@.@.......
........@.@.@..
.............@.
............@..
.@.@.........@.
....@.@.....@..
.......@.@.@...
..@.@.@........
"""

pt = set()
for r, line in enumerate(pattern.splitlines(keepends=False)[1:]):
    for c, ch in enumerate(line):
        p = r, c
        if ch == "@":
            pt.add(p)
pt = HexagonPoly.doubled_to_points(pt)

print("Cube coordinates")
print(pt)

print("Id and Preferred")
id, rp, pt = HexagonPoly.get_pattern_id(pt, (0, 0, 0))
print(id)
print(pt)

HexagonPoly.draw(id)

hmc = 0
for p in pt:
    mc = Plane.get_maximum_collinear(pt, p, 3)
    hmc = max(mc, hmc)
print(hmc, len(pt))
