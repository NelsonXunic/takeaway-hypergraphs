class Hypergraph:
    def __init__(self):
        self.vertices = set()
        self.edges = []  # edges of size 2
        self.faces = []  # hyperedges of size > 2

    def add_vertex(self, v):
        self.vertices.add(v)

    def add_edge(self, u, v):
        self.edges.append({u, v})

    def add_face(self, face):
        self.faces.append(set(face))

    def remove_vertex(self, v):
        self.vertices.discard(v)
        self.edges = [e for e in self.edges if v not in e]
        self.faces = [f for f in self.faces if v not in f]

    def remove_hyperedge(self, h):
        self.faces = [f for f in self.faces if not h.issubset(f)]
        if len(h) == 2:
            self.edges = [e for e in self.edges if e != h]

    def is_empty(self):
        return len(self.vertices) == 0
