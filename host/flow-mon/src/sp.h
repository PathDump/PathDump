// Program to print BFS traversal from a given source vertex. BFS(int s) 
// traverses vertices reachable from s.
#include<iostream>
#include <list>
#include <string.h>
using namespace std;

// This class represents a directed graph using adjacency list representation
class Graph
{
	int V; // No. of vertices
	list<int> *adj; // Pointer to an array containing adjacency lists
        int *prev;
	bool *visited;
public:
	Graph();
	~Graph();
	void init(int V); 
	void addEdge(int v, int w); // function to add an edge to graph
	void BFS(int s,int d, int *prev); // prints BFS traversal from a given source s
        list<int> getPath(int s,int d);
};
