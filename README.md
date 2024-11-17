# collinear-polyominoes

Categorising free polyominoes by collinearity of cells as well as size

## Free Polyominoes

A [free polyomino](https://en.wikipedia.org/wiki/Polyomino) is analogous to a simple connected planer graph where nodes are points on the lattice.

Free meaning we do not double count the dihedral symmetries (rotation / reflection)

The [exponential growth](https://polyominoes.org/count) of the number of polyominoes of size n is known up to n=45

## Polyomino Cell Shape

We are considering just the **Square** and **Hexagon** polyominoes

For hexagon polyominoes the analogy to connected planer graphs uses a triangular lattice

## Collinearity

We are considering cells/nodes/points that are collinear in 2 ways

### Anywhere on the plane

Using the centres of the cells as points then collinear points in the plane means the cells are considered collinear.

### Just on the lattice

- For a Square polyomino that means cells in the same row or column, or points on the grid lines of a square lattice.
- For a Hexagon polyomino that means cells on a line that runs perpendicular to the hexagon sides and through the centres
(or for nodes/points the triangular lattice).

### Maximum Points Collinear

We are interested in counting the number of polyominoes that have a maximum number of cells collinear (k) for the 4 cases of (Square or Hexagon) x (Lattice or Plane).

#### Triangular Sequences

See OEIS

- [A377941](https://oeis.org/A377941) | Square | Lattice
- [A377942](https://oeis.org/A377942) | Square | Plane
- [A378014](https://oeis.org/A378014) | Hexagon | Lattice
- [A378015](https://oeis.org/A378015) | Hexagon | Plane

### Largest Polyomino with no more than 3 cells collinear on the Plane

Square: n=15 , the only polyomino is

```text
  #
  #
 ###
 # ##
##  #
#  ##
#
```

Hexagon: n=23 , the 2 hexagon polyominoes are:

```text
            @ @                      @
           @                    @     @
    @       @                    @ @   @
     @ @     @          @           @ @
@   @       @            @ @           @
 @   @       @          @   @           @
  @ @         @              @ @       @
     @     @ @                  @   @ @
      @ @ @                      @ @
```

### Enumeration

The enumeration identifier is constructed by observing the pattern on a row/column grid using the usual coordinate system.
This gives us a binary representation of each row, so the whole pattern is represented as a tuple of integers.
