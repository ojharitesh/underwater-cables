<h1 align="center">Planning and Analysis </h1>
<h3 align="center">Team Members: Ritesh Ojha, Rivan Deets, Tyler Biss, Krish Yendluri </h3>

## Problem Formulation
The objective of the Underwater Cables problem is to connect all `n` island data centers while minimizing the total cost of laying fiber-optic cables. We are given a weighted, undirected graph `G=(V,E)`, where each vertex represents an island, each edge represents a possible cable route between two islands, and the weight of an edge is the cost of installing that route. We need to choose a set of edges that connects every island, possibly through other islands, at the smallest possible total cost.

This is a Minimum Spanning Tree (MST) problem. A spanning tree connects every vertex without forming a cycle and contains exactly `n-1` edges. We assume the input graph is connected; otherwise, no solution can connect all islands using the available routes.

## Baseline Solution


## Algorithmic Strategy 

To efficiently find the smallest possible total cost of connecting all islands in a weighted, undirected graph, we will use a greedy approach. Specifically, we will use **Kruskal’s algorithm**, which sorts all available cable routes by increasing installation cost and repeatedly chooses the cheapest edge that does not create a cycle. A cycle would add an unnecessary cable because its endpoints already have a path connecting them.

For the algorithm to work efficiently, we use a **Disjoint Set Union (DSU)** data structure. DSU initially places each island in its own component. The `find` operation identifies the component an island belongs to, and `union` merges two components after we select a cable connecting them. If two islands already belong to the same component, adding a cable between them would create a cycle.

Our DSU uses path compression in `find` and union by rank in `union` to keep these operations efficient. The class includes:

```text
class DSU:
    initialize(vertices):
        parent = empty map
        rank = empty map

        for each vertex v in vertices:
            parent[v] = v
            rank[v] = 0

    find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    union(x, y):
        root_x = find(x)
        root_y = find(y)

        if root_x == root_y:
            return

        if rank[root_x] < rank[root_y]:
            parent[root_x] = root_y
        else if rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        else:
            parent[root_y] = root_x
            rank[root_x] = rank[root_x] + 1
```

To find the MST, the algorithm starts with an empty set of selected edges and initializes DSU so that each island belongs to its own component. It then sorts all edges in ascending order of cost. For each edge, the algorithm checks whether its endpoints belong to different components. If they do, it adds the edge to the MST, updates the total cost, and merges the components. Otherwise, it skips the edge. This continues until the MST contains exactly `|V| - 1` edges.

This greedy choice is justified by the **MST cut property**. Each selected edge is a cheapest edge leaving one of the current components, so it can safely be added while preserving the possibility of completing a minimum spanning tree. Repeating these safe choices produces a network connecting all islands at the minimum total installation cost.

```text
Algorithm underwaterCablesGreedy(G):
    input: Weighted, undirected graph G = (V, E)
    output: MST and its total cost, or failure if disconnected

    MST = empty set
    total_cost = 0

    if size(V) <= 1:
        return MST, total_cost

    dsu = DSU(V)
    sorted_edges = sort E by increasing cost

    for each edge (u, v, cost) in sorted_edges:
        if dsu.find(u) != dsu.find(v):
            Add (u, v, cost) to MST
            total_cost = total_cost + cost
            dsu.union(u, v)

            if size(MST) == size(V) - 1:
                return MST, total_cost

    return "No spanning tree exists"
```

## Complexity Analysis 
The baseline algorithm adds one new island per iteration, requiring `|V| - 1` iterations for a connected graph. During each iteration, it scans all `|E|` cable routes. Assuming expected constant-time membership checks using a hash set, the overall running time is **O(|V| × |E|)**. Its main weakness is repeatedly examining the same routes.

Our improved solution initializes DSU in O(|V|) time and sorts the routes in O(|E| log |E|) time. With path compression and union by rank, the Union-Find operations take O(|E| α(|V|)) time in total, where α is the inverse Ackermann function and grows extremely slowly. For a connected graph with at least two vertices, sorting dominates, giving an overall running time of **O(|E| log |E|)**.

Both algorithms produce a minimum-cost cable network. Kruskal’s improves efficiency by sorting the routes once and using Union-Find to check connections instead of repeatedly scanning every route to choose each new cable.
