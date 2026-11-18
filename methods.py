class DSU: # Disjoint Set Union
    def __init__(self, vertices): # Constructor
        self.parent = {}
        self.rank = {}

        for v in vertices:
            self.parent[v] = v
            self.rank[v] = 0
    def find(self, x): # Find the vertex to use in union
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y): # Check if the vertices are connected
        found_x = self.find(x)
        found_y = self.find(y)

        if found_x == found_y:
            return

        if self.rank[found_x] < self.rank[found_y]:
            self.parent[found_x] = found_y
        elif self.rank[found_x] > self.rank[found_y]:
            self.parent[found_y] = found_x
        else:
            self.parent[found_y] = found_x
            self.rank[found_x] = self.rank[found_x] + 1

def underwaterCablesGreedy(G):
    V, E = G # Split the Graph into Vertices and Edges
    MST = [] # Establish the MST
    total_cost = 0

    if len(V) <= 1: # Base case
        return MST, total_cost

    dsu = DSU(V)
    sorted_edges = sorted(E, key=lambda edge: edge[2]) # Sort edges in ascending cost order

    for u, v, cost in sorted_edges: # For every edge starting with the cheapest, check if the vertices are connected already. If not connected, connect.
        if dsu.find(u) != dsu.find(v):
            MST.append((u, v, cost))
            total_cost = total_cost + cost
            dsu.union(u, v)

            if len(MST) == len(V) - 1: # Once there are V - 1 edges, then the MST is completed
                return MST, total_cost

    return "No spanning tree exists" # If edges cannot get to V - 1, then it cannot become a MST