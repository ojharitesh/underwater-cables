<h1 align="center">Planning and Analysis </h1>

## Problem Formulation
The objective of the Underwater Cables problem is to connect all `n` island data centers while minimizing the total cost of laying fiber-optic cables. We are given a weighted, undirected graph `G=(V,E)`, where each vertex represents an island, each edge represents a possible cable route between two islands, and the weight of an edge is the cost of installing that route. We need to choose a set of edges that connects every island, possibly through other islands, at the smallest possible total cost.

This is a Minimum Spanning Tree (MST) problem. A spanning tree connects every vertex without forming a cycle and contains exactly `n-1` edges. We assume the input graph is connected; otherwise, no solution can connect all islands using the available routes.

## Baseline Solution
Instead of testing complex combinations, Prim’s algorithm uses a greedy strategy: it begins with one island and repeatedly selects the least expensive cable route that connects an island already in the network to an island outside the network. By always expanding from the existing network, the algorithm avoids creating cycles. The process stops once all (n) islands are connected using exactly (n-1) cables.## Algorithmic Strategy 

## Complexity Analysis 
Our baseline starts at one island and repeatedly scans every cable route to find the cheapest one that connects a visited island to a new one. A spanning tree needs |V| − 1 edges, so we repeat this scan about |V| times, and each scan may look at all |E| routes. That gives O(|V| × |E|). The main weakness is repeated work: each round re-checks routes we’ve already looked at. This is fine for small maps but gets slow as the number of islands and routes grows. Kruskal’s avoids this by sorting the routes once (O(|E| log |E|)) and then making a quick cycle check for each one with Union-Find, which is why it’s our improved solution.