class Hypergraph:
    def __init__(self):
        self.vertices = set()
        self.edges = []  # edges of size 2
        self.faces = []  # hyperedges of size > 2

    def __repr__(self) -> str:
        return (
            f"Hypergraph(\n"
            f"  Vertices: {sorted(self.vertices)}\n"
            f"  Edges: {sorted([sorted(e) for e in self.edges])}\n"
            f"  Faces: {sorted([sorted(f) for f in self.faces])}\n"
            f")"
        )

    def __str__(self) -> str:
        return f"V: {self.vertices} | E: {self.edges} | F: {self.faces}"

    def add_vertex(self, v):
        self.vertices.add(v)

    def add_edge(self, vertices: set):
        if len(vertices) != 2:
            raise ValueError("Edge must connect exactly two vertices.")
        self.edges.append(set(vertices))

    def add_face(self, face):
        self.faces.append(set(face))

    def remove_vertex(self, v):
        self.vertices.discard(v)
        self.edges = [e for e in self.edges if v not in e]
        self.faces = [f for f in self.faces if v not in f]

    def remove_edge(self, edge: set):
        if edge in self.edges:
            self.edges.remove(edge)

    def remove_hyperedge(self, h):
        self.faces = [f for f in self.faces if not h.issubset(f)]
        if len(h) == 2:
            self.edges = [e for e in self.edges if e != h]

    def remove_face(self, face: set):
        if face in self.faces:
            self.faces.remove(face)

    def is_empty(self):
        return len(self.vertices) == 0
