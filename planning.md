<h1 align="center">Planning and Analysis </h1>
<h3 align="center">Team Members: Ritesh Ojha, Rivan Deets, Tyler Biss, Krish Yendluri </h3>

## Problem Formulation
The objective of the Underwater Cables problem is to connect all `n` island data centers while minimizing the total cost of laying fiber-optic cables. We are given a weighted, undirected graph `G=(V,E)`, where each vertex represents an island, each edge represents a possible cable route between two islands, and the weight of an edge is the cost of installing that route. We need to choose a set of edges that connects every island, possibly through other islands, at the smallest possible total cost.

This is a Minimum Spanning Tree (MST) problem. A spanning tree connects every vertex without forming a cycle and contains exactly `n-1` edges. We assume the input graph is connected; otherwise, no solution can connect all islands using the available routes.

## Baseline Solution
Instead of testing complex combinations, Kruskal's algorithm uses a greedy strategy: it sorts all available cable routes (edges) in ascending order of their installation costs. It then iterates through the sorted list, adding the cheapest cable to the network one by one, provided that adding it does not create a closed loop (cycle) among the islands. The process stops once all $n$ islands are connected using exactly $n-1$ cables.
## Algorithmic Strategy 
To efficently find the smallest possible total cost of a weighted, undirected graph, we want to use a greedy approach that will go for the cheapest most efficent route possible. Specifically, we want to use what is called `Kruskal's Algorithm` which repeatedly chooses the cheapest available edge that does not create a cycle. The algorithm ensures there is no cycle since a cycle would make the graph no longer a `Minimum Spanning Tree`. 

For the algorithm to work, we use the data structure of Disjoint Set Union. DSU allows us to make a set of the weighted graph (MAKE-SET) and then use the functions FIND, UNION to figure out if islands are connected already or not and connect them if they need to be. 

To find the MST of the graph, we implement `Kruskal's Algorithm` in our Underwater Cables problem. The algorithm first starts with an empty MST that we attempting to create. The algorithm uses DSU to make sure each island has its own component in the set. The algorithm then sorts all the edges in ascending order with the cheapest first. The for loop then finds through the cheapest available edge and checks if it would create a cycle or not. If not, add it to MST and if so, move on. This for loop will continue until there are edges of less than one of the total vertices. This ensures that the MST will contain the cheapest possible tree between the islands. 
```text
Algorithm underWaterCablesGreedy(G):
    Input: a weighted, undirected graph G=(V,E) 
        V = vertices representing islands 
        E = edges of the graph that connect the islands
    Output: 
        MST = minimum spanning tree
        total_cost = total cost of the MST (minimum through the algorithm)

    MST = empty set of edges
    total cost = 0 
    for every vertices (v) in V: 
        MAKE-SET(v)
    Sort edges by increasing costs (least expensive -> most expensive)
    for each edge (x, y, cost) in E:
        if FIND(x)!= FIND(y):
            MST.add(x, y, cost)
            UNION(x, y)
            total_cost += cost
        if size(MST) == V - 1:
            break
    return MST, total_cost
```

## Complexity Analysis 
Our baseline starts at one island and repeatedly scans every cable route to find the cheapest one that connects a visited island to a new one. A spanning tree needs |V| − 1 edges, so we repeat this scan about |V| times, and each scan may look at all |E| routes. That gives O(|V| × |E|). The main weakness is repeated work: each round re-checks routes we’ve already looked at. This is fine for small maps but gets slow as the number of islands and routes grows. Kruskal’s avoids this by sorting the routes once (O(|E| log |E|)) and then making a quick cycle check for each one with Union-Find, which is why it’s our improved solution.
