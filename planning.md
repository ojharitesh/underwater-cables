<h1 align="center">Planning and Analysis </h1>
<h3 align="center">Team Members: Ritesh Ojha, Rivan Deets, Tyler Biss, Krish Yendluri </h3>

## Problem Formulation
The objective of the Underwater Cables problem is to connect all `n` island data centers while minimizing the total cost of laying fiber-optic cables. We are given a weighted, undirected graph `G=(V,E)`, where each vertex represents an island, each edge represents a possible cable route between two islands, and the weight of an edge is the cost of installing that route. We need to choose a set of edges that connects every island, possibly through other islands, at the smallest possible total cost.

This is a Minimum Spanning Tree (MST) problem. A spanning tree connects every vertex without forming a cycle and contains exactly `n-1` edges. We assume the input graph is connected; otherwise, no solution can connect all islands using the available routes.

## Baseline Solution
Instead of testing complex combinations, Prim’s algorithm uses a greedy strategy: it begins with one island and repeatedly selects the least expensive cable route that connects an island already in the network to an island outside the network. By always expanding from the existing network, the algorithm avoids creating cycles. The process stops once all (n) islands are connected using exactly (n-1) cables.## Algorithmic Strategy 

## Complexity Analysis 
The baseline algorithm adds one new island per iteration, requiring `|V| - 1` iterations for a connected graph. During each iteration, it scans all `|E|` cable routes. Assuming expected constant-time membership checks using a hash set, the overall running time is **O(|V| × |E|)**. Its main weakness is repeatedly examining the same routes.

Our improved solution initializes DSU in O(|V|) time and sorts the routes in O(|E| log |E|) time. With path compression and union by rank, the Union-Find operations take O(|E| α(|V|)) time in total, where α is the inverse Ackermann function and grows extremely slowly. For a connected graph with at least two vertices, sorting dominates, giving an overall running time of **O(|E| log |E|)**.

Both algorithms produce a minimum-cost cable network. Kruskal’s improves efficiency by sorting the routes once and using Union-Find to check connections instead of repeatedly scanning every route to choose each new cable.
