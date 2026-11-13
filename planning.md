<h1 align="center">Planning and Analysis </h1>
<h3 align="center">Team Members: Ritesh Ojha, Rivan Deets, Tyler Biss, Krish Yendluri </h3>

## Problem Formulation
The objective of the Underwater Cables problem is to connect all `n` island data centers while minimizing the total cost of laying fiber-optic cables. We are given a weighted, undirected graph `G=(V,E)`, where each vertex represents an island, each edge represents a possible cable route between two islands, and the weight of an edge is the cost of installing that route. We need to choose a set of edges that connects every island, possibly through other islands, at the smallest possible total cost.

This is a Minimum Spanning Tree (MST) problem. A spanning tree connects every vertex without forming a cycle and contains exactly `n-1` edges. We assume the input graph is connected; otherwise, no solution can connect all islands using the available routes.

## Baseline Solution
Instead of testing complex combinations, Prim’s algorithm uses a greedy strategy: it begins with one island and repeatedly selects the least expensive cable route that connects an island already in the network to an island outside the network. By always expanding from the existing network, the algorithm avoids creating cycles. The process stops once all (n) islands are connected using exactly (n-1) cables.## Algorithmic Strategy 

## Algorithmic Strategy 
To efficently find the smallest possible total cost of a weighted, undirected graph, we want to use a greedy approach that will go for the cheapest most efficent route possible. Specifically, we want to use what is called `Kruskal's Algorithm` which repeatedly chooses the cheapest available edge that does not create a cycle. The algorithm ensures there is no cycle since a cycle would make the graph no longer a `Minimum Spanning Tree`. 

For the algorithm to work, we use the data structure of Disjoint Set Union. DSU allows us to make a set of the weighted graph and then use the functions FIND, UNION to figure out if islands are connected already or not and connect them if they need to be. A DSU class will have to be made that will check these things. This class includes:
```text
class DSU:
    def __init__(self, vertices):
        parent = array of size of number of vertices
        size = array of size of number of vertices initialized to 0

        for each vertex in vertices from 0 to vertices - 1:
            parent[vertex] = vertex
    find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return x
    union(x, y):
        found_x = find(x)
        found_y = find(y)
        if rank[found_x] < rank[found_y]:
            parent[found_x] = found_y
        else if rank[found_x] > rank[found_y]:
            parent[found_y] = found_x
        else:
            parent[found_y] = found_x
            rank[found_x] = rank[found_x] + 1
```
To find the MST of the graph, we implement `Kruskal's Algorithm` in our Underwater Cables problem. The algorithm first starts with an empty MST that we attempting to create. The algorithm uses DSU to make sure each island has its own component in the set. The algorithm then sorts all the edges in ascending order with the cheapest first. The for loop then finds through the cheapest available edge and checks if it would create a cycle or not. If not, add it to MST and if so, move on. This for loop will continue until there are edges of less than one of the total vertices. This ensures that the MST will contain the cheapest possible tree between the islands. 
```text
Algorithm underWaterCablesGreedy(G):
    Input: a weighted, undirected graph G=(V,E) 
        V = vertices representing islands 
        E = edges of the graph that connect the islands
    Output: 
        MST = minimum spanning tree
        total_cost = total cost of the MST (minimum through the algorithm)

    initialize DSU
    MST = empty set of edges
    total cost = 0 
    for every vertices (v) in V: 
        make_set(v)
    Sort edges by increasing costs (least expensive -> most expensive)
    for each edge (x, y, cost) in E:
        if dsu.find(x)!= dsu.find(y):
            MST.add(x, y, cost)
            dsu.union(x, y)
            total_cost += cost
        if size(MST) == V - 1:
            break
    return MST, total_cost
```

## Complexity Analysis 
The baseline algorithm adds one new island per iteration, requiring `|V| - 1` iterations for a connected graph. During each iteration, it scans all `|E|` cable routes. Assuming expected constant-time membership checks using a hash set, the overall running time is **O(|V| × |E|)**. Its main weakness is repeatedly examining the same routes.

Our improved solution initializes DSU in O(|V|) time and sorts the routes in O(|E| log |E|) time. With path compression and union by rank, the Union-Find operations take O(|E| α(|V|)) time in total, where α is the inverse Ackermann function and grows extremely slowly. For a connected graph with at least two vertices, sorting dominates, giving an overall running time of **O(|E| log |E|)**.

Both algorithms produce a minimum-cost cable network. Kruskal’s improves efficiency by sorting the routes once and using Union-Find to check connections instead of repeatedly scanning every route to choose each new cable.
