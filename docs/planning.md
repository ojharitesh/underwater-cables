<h1 align="center">Planning and Analysis </h1>
<h3 align="center">Team Members: Ritesh Ojha, Rivan Deets, Tyler Biss, Krish Yendluri </h3>

## Problem Formulation
The objective of the Underwater Cables problem is to connect all `n` island data centers while minimizing the total cost of laying fiber-optic cables. We are given a weighted, undirected graph `G=(V,E)`, where each vertex represents an island, each edge represents a possible cable route between two islands, and the weight of an edge is the cost of installing that route. We need to choose a set of edges that connects every island, possibly through other islands, at the smallest possible total cost.

This is a Minimum Spanning Tree (MST) problem. A spanning tree connects every vertex without forming a cycle and contains exactly `n-1` edges. We assume the input graph is connected; otherwise, no solution can connect all islands using the available routes.

## Baseline Solution
For our baseline solution, we will use a simple version of **Prim’s algorithm**. The algorithm starts at any island and repeatedly scans every cable route to find the cheapest edge connecting an already connected island to an unconnected island.

After selecting that edge, the algorithm adds the new island to the connected group. This continues until every island is connected. If no edge connects the current group to a remaining island, the algorithm reports that no spanning tree exists.

```text
Algorithm underwaterCablesBaseline(G):
    input: Weighted, undirected graph G = (V, E)
    output: MST and its total cost, or failure if disconnected

    MST = empty set
    total_cost = 0

    if V is empty:
        return MST, total_cost

    connected = hash set containing any vertex in V

    while size(connected) < size(V):
        cheapest = NONE

        for each edge (u, v, cost) in E:
            if exactly one of u and v is in connected:
                if cheapest is NONE or cost < cheapest.cost:
                    cheapest = (u, v, cost)

        if cheapest is NONE:
            return "No spanning tree exists"

        (u, v, cost) = cheapest
        Add cheapest to MST
        total_cost = total_cost + cost

        if u is in connected:
            Add v to connected
        else:
            Add u to connected

    return MST, total_cost
```

For example, suppose we have four islands with these possible cable routes:

| Cable Route | Installation Cost |
|-------------|-------------------|
| A–B         | 2                 |
| A–C         | 5                 |
| B–C         | 1                 |
| B–D         | 4                 |
| C–D         | 3                 |

Starting at island A, the baseline selects A–B with cost 2. It then selects B–C with cost 1, followed by C–D with cost 3. These three cables connect all four islands with a minimum total cost of **6**.

This approach guarantees an optimal solution because each selected edge is the cheapest edge connecting the current group to the remaining islands. However, repeatedly scanning all routes becomes inefficient as the number of islands and routes increases.

## Algorithmic Strategy 

To efficiently find the smallest possible total cost of connecting all islands, we will use a different greedy approach based on **Kruskal’s algorithm**. The algorithm sorts all available cable routes by increasing installation cost and repeatedly chooses the cheapest edge that does not create a cycle. A cycle would add an unnecessary cable because its endpoints already have a path connecting them.

For the algorithm to work efficiently, we use a **Disjoint Set Union (DSU)** data structure. DSU initially places each island in its own component. The `find` operation identifies the component an island belongs to, while `union` merges two components after we select a cable connecting them. If two islands already belong to the same component, adding a cable between them would create a cycle.

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
        found_x = find(x)
        found_y = find(y)

        if found_x == found_y:
            return

        if rank[found_x] < rank[found_y]:
            parent[found_x] = found_y
        else if rank[found_x] > rank[found_y]:
            parent[found_y] = found_x
        else:
            parent[found_y] = found_x
            rank[found_x] = rank[found_x] + 1
```

To find the MST, the algorithm starts with an empty set of selected edges and initializes DSU so that each island belongs to its own component. It then sorts all edges in ascending order of cost. For each edge, it checks whether the endpoints belong to different components. If they do, the algorithm adds the edge to the MST, updates the total cost, and merges the components. Otherwise, it skips the edge. The algorithm stops after selecting exactly `|V| - 1` edges. If all edges have been considered without reaching this count, no spanning tree exists.

This greedy choice is justified by the **MST cut property**. Each selected edge is a cheapest edge leaving one of the current components, so it can safely be added while preserving the possibility of completing a minimum spanning tree. Repeating these safe choices connects all islands at the minimum total installation cost.

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
