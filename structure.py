import numpy as np

class Vertex:
    """
    Point where multiple edges meet/connect
    """

    def __init__(self, pos):
        # Position of this vertex in 3D space
        self.pos = np.array(pos)

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

    def add_vertex(self, pos):
        """
        Add a new vertex to the structure
        """

        v = Vertex(pos)
        self.verts.append(v)

        # Return the new vertex
        return v

    def add_edge(self):
        """
        Add a new edge to the structure
        """


        # TODO:
        # Return the new edge
        pass

cube = Structure()

# Bottom face
cube.add_vertex([0, 0, 0])
cube.add_vertex([1, 0, 0])
cube.add_vertex([1, 0, 1])
cube.add_vertex([0, 0, 1])

# Top face
cube.add_vertex([0, 1, 0])
cube.add_vertex([1, 1, 0])
cube.add_vertex([1, 1, 1])
cube.add_vertex([0, 1, 1])
