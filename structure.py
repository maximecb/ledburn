import math
import numpy as np
from util import rot_matrix

class Vertex:
    """
    Point where multiple edges meet/connect
    """

    def __init__(self, pos):
        # Position of this vertex in 3D space
        self.pos = np.array(pos, dtype=np.float32)

        # Edges associated with this vertex
        self.edges = []

class Edge:
    def __init__(self, start, end, edge_idx, num_leds=60):
        # Start and end vertices
        self.start = start
        self.end = end

        # Number of LEDs among this edge
        self.num_leds = num_leds

        # TODO:
        # Start and end indices in a global LED matrix?
        # Or do we just want to assign each edge an index

        # Index of this edge (assigned by the structure)
        self.edge_idx = edge_idx

class Structure:
    """
    Define the topology and spatial positioning of a 3D shape/structure
    made of edges and vertices.
    """

    def __init__(self, leds_per_edge=60):
        # Each edge is assumed to have the same number of LEDs
        self.leds_per_edge = 60

        # List of vertices
        self.verts = []

        # List of edges
        self.edges = []

        # Total number of LEDs in the structure
        self.num_leds = 0

        # NumPy array, RGB color of each pixel (num_edges, leds_per_edge, 3)
        self.pixels = None

        # NumPy array, XYZ position of every LED (num_edges, leds_per_edge, 3)
        self.poss = None

    @property
    def num_edges(self):
        return len(self.edges)

    def add_vertex(self, pos):
        """
        Add a new vertex to the structure
        """

        v = Vertex(pos)
        self.verts.append(v)

        # Return the new vertex
        return v

    def add_edge(self, idx0, idx1):
        """
        Add a new edge to the structure
        """

        assert idx0 < len(self.verts)
        assert idx1 < len(self.verts)

        edge = Edge(
            start=self.verts[idx0],
            end=self.verts[idx1],
            edge_idx=len(self.edges),
            num_leds=self.leds_per_edge
        )

        self.edges.append(edge)
        self.num_leds += edge.num_leds

        # Return the new edge
        return edge

    def scale(self, s):
        """
        Re-scale the vertex position according to some scale factor
        """

        for vert in self.verts:
            vert.pos *= s

    # Method to rotate the structure around the origin
    # This will rotate the positions of all vertices
    def rotate(self, axis, angle):
        m = rot_matrix(axis, angle)

        for vert in self.verts:
            vert.pos = np.matmul(vert.pos, m)

    def extents(self):
        x_sorted = sorted(self.verts, key = lambda v: v.pos[0])
        y_sorted = sorted(self.verts, key = lambda v: v.pos[1])
        z_sorted = sorted(self.verts, key = lambda v: v.pos[2])
        return x_sorted[0].pos[0], x_sorted[-1].pos[0], y_sorted[0].pos[1], y_sorted[-1].pos[1], z_sorted[0].pos[2], z_sorted[-1].pos[2]

    def finalize(self):
        """
        Called once all vertices and edges are added
        """

        # Allocate an array for the LED RGB pixels
        self.pixels = np.zeros(
            shape=(len(self.edges), self.leds_per_edge, 3),
            dtype=np.float32
        )

        # Allocate an array for the LED positions in 3D space
        self.poss = np.zeros(
            shape=(self.num_edges, self.leds_per_edge, 3),
            dtype=np.float32
        )

        # Compute the position of each LED
        for edge_idx, edge in enumerate(self.edges):
            p0 = edge.start.pos
            p1 = edge.end.pos
            for led_idx in range(edge.num_leds):
                f = (led_idx + 0.5) / edge.num_leds
                p = (1 - f) * p0 + f * p1
                self.poss[edge_idx, led_idx, :] = p

cube = Structure()

# Bottom face (y=-1)
cube.add_vertex([-1,-1,-1]) # 0
cube.add_vertex([ 1,-1,-1]) # 1
cube.add_vertex([ 1,-1, 1]) # 2
cube.add_vertex([-1,-1, 1]) # 3

# Top face (y=1)
cube.add_vertex([-1, 1,-1]) # 4
cube.add_vertex([ 1, 1,-1]) # 5
cube.add_vertex([ 1, 1, 1]) # 6
cube.add_vertex([-1, 1, 1]) # 7

# Bottom face edges
cube.add_edge(0, 1)
cube.add_edge(1, 2)
cube.add_edge(2, 3)
cube.add_edge(3, 0)

# Top face edges
cube.add_edge(4, 5)
cube.add_edge(5, 6)
cube.add_edge(6, 7)
cube.add_edge(7, 4)

# Connect bottom to top
cube.add_edge(4, 0)
cube.add_edge(1, 5)
cube.add_edge(6, 2)
cube.add_edge(3, 7)

cube.scale(0.5)
#cube.rotate([1, 0, 0], math.pi / 4)
#cube.rotate([0, 1, 0], math.pi / 4)
cube.finalize()
