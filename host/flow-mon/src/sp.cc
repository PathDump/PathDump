#include "sp.h"

Graph::Graph(void){
}

void Graph::init(int V)
{
	this->V = V;
	adj = new list<int>[V];
	prev = new int[V];
	visited = new bool[V];
}

Graph::~Graph(void)
{
	delete [] prev;
	delete [] visited;
	delete [] adj;
}


void Graph::addEdge(int v, int w)
{
	adj[v].push_back(w); // Add w to v’s list.
	adj[w].push_back(v); // Add v to w’s list.
}

list<int> Graph::getPath(int s, int d)
{
        list<int> path;
        memset(prev,0,sizeof(*prev));
        BFS(s,d,prev);
        while(true){
            path.push_front(d);
            if(d==s)
                break;
            d=prev[d];
        }
        return path;
}

void print( list <int> & v )
{
    std::list<int>::iterator n;  
    for (n = v.begin(); n != v.end(); n++)
              cout << "\"" << *n << "\"\n";
        cout << endl;
}

void Graph::BFS(int s,int d,int *prev)
{
	for(int i = 0; i < V; i++)
		visited[i] = false;
	list<int> queue;
	// Mark the current node as visited and enqueue it
	visited[s] = true;
	queue.push_back(s);

	// 'i' will be used to get all adjacent vertices of a vertex
	list<int>::iterator i;

	while(!queue.empty())
	{
		// Dequeue a vertex from queue and print it
		s=queue.front();
                queue.pop_front();
                if (s==d){
                    break; 
                }
		// Get all adjacent vertices of the dequeued vertex s
		// If a adjacent has not been visited, then mark it visited
		// and enqueue it
		for(i = adj[s].begin(); i != adj[s].end(); ++i)
		{
			if(!visited[*i])
			{
				visited[*i] = true;
                                queue.push_back(*i);
                                prev[*i]=s;
			}
		}
	}
}
