class Hypergraph:
    def __init__(self):
        self.vertices = set()
        self.edges = set()  # edges of size 2
        self.faces = set()  # hyperedges of size > 2

    def __str__(self) -> str:
        return f"V: {self.vertices} | E: {self.edges} | F: {self.faces}"

    def add_vertex(self, vertex):
        self.vertices.add(vertex)

    def add_edge(self, vertex_set: set):
        if len(vertex_set) != 2:
            raise ValueError("Edge must connect exactly two vertices.")
        if not all(vertex in self.vertices for vertex in vertex_set):
            raise ValueError("All vertices in an edge must exist in the hypergraph.")
        self.edges.add(frozenset(vertex_set))

    def add_face(self, face):
        if not all(vertex in self.vertices for vertex in face):
            raise ValueError("All vertices in a face must exist in the hypergraph.")
        self.faces.add(frozenset(face))

    def remove_vertex(self, vertex):
        if vertex not in self.vertices:
            return

        self.vertices.remove(vertex)
        # Remove all edges and faces that contain vertex
        self.edges = {edge for edge in self.edges if vertex not in edge}
        self.faces = {face for face in self.faces if vertex not in face}

    def remove_edge(self, edge: set):
        if edge in self.edges:
            self.edges.discard(frozenset(edge))

    def remove_hyperedge(self, h_set: set):
        self.faces = {face for face in self.faces if not h_set.issubset(face)}
        if len(h_set) == 2:
            self.edges.discard(frozenset(h_set))

    def remove_face(self, face: set):
        if face in self.faces:
            self.faces.discard(frozenset(face))

    def is_empty(self):
        return len(self.vertices) == 0
        # another way to check emptiness
        # return not self.vertices and not self.edges and not self.faces

    def __repr__(self):
        return (
            f"Hypergraph(vertices={sorted(list(self.vertices))}, "
            f"edges={sorted([tuple(sorted(list(e))) for e in self.edges])}, "
            f"faces={sorted([tuple(sorted(list(f))) for f in self.faces])})"
        )

    # Override equality method for proper comparison;
    # we check for equality between two Hypergraph instances
    def __eq__(self, other):
        if not isinstance(other, Hypergraph):
            return NotImplemented
        return (
            self.vertices == other.vertices
            and self.edges == other.edges
            and self.faces == other.faces
        )

    # Two Hypergraph objects will have the same hash
    # # if their structure (vertices, edges, faces)
    # is identical, regardless of the internal order
    # of elements in the Python sets, making them suitable for
    # use as dictionary keys or set members
    def __hash__(self):
        # Create a canonical representation for hashing
        # qwe sort vertices for consistent order
        canonical_vertices = frozenset(sorted(list(self.vertices)))
        # sort frozenset edges (each frozenset is already hashable)
        # The key ensures consistent ordering
        # of frozensets in the outer frozenset
        canonical_edges = frozenset(
            sorted(list(self.edges), key=lambda x: tuple(sorted(x)))
        )
        # and , sort frozenset faces
        canonical_faces = frozenset(
            sorted(list(self.faces), key=lambda x: tuple(sorted(x)))
        )

        return hash((canonical_vertices, canonical_edges, canonical_faces))

    def copy(self) -> "Hypergraph":
        """
        Creates a deep copy of the hypergraph.
        """
        new_hg = Hypergraph()
        # Add vertices explicitly
        for vertex in self.vertices:
            new_hg.add_vertex(vertex)
        # Add edges (they will be frozensets, so they can be copied directly)
        new_hg.edges = (
            self.edges.copy()
        )  # set.copy() creates a shallow copy of the set, but frozensets are immutable
        # Add faces
        new_hg.faces = self.faces.copy()
        return new_hg
