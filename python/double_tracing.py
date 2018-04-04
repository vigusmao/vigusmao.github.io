#
#    All (multi-)graphs in this program will be given in the form of a list
#       [n, m, dictionary {vertex: hash set {neighbor: multiplicity} of neighbors}],
#       where `n` and `m` are the vertex count and edge count, respectively,
#       and `multiplicity` indicates the number of edges from `vertex` to `neighbor`.
#


# readability constants
N = 0
M = 1
ADJACENCY_LISTS = 2


'''
    G: a graph
'''
def findDoubleTracing(G):

    '''
        currentPath: a list of triples (v, w, label) in the order the edges were visited
        visitedEdges: a set of triples (v, w, label) indicating the edges that were already visited
    '''
    def backtrack(currentPath, visitedEdges, initialVertex):
        if len(currentPath) == 2 * G[M]:
            return True  # found a double tracing!

        latestEdge = currentPath[-1] if len(currentPath) > 0 else None
        currentVertex = latestEdge[1] if latestEdge is not None else initialVertex
        
        neighbors = G[ADJACENCY_LISTS].get(currentVertex)

        if neighbors != None:
            for nextVertex, multiplicity in neighbors.items():
                for label in range(1, multiplicity + 1):
                    edge = (currentVertex, nextVertex, label)
                    if edge in visitedEdges:
                        continue  # edge already visited
                    if len(currentPath) > 0 and currentPath[-1] == (nextVertex, currentVertex, label):
                        continue  # avoiding U-turns

                    # changes the current state
                    currentPath.append(edge)
                    visitedEdges.add(edge)

                    if backtrack(currentPath, visitedEdges, initialVertex) == True:
                        return True

                    # restores the previous state so we can move along to the next candidate state
                    currentPath.pop()
                    visitedEdges.remove(edge)

        return False
    
    ###

    for initialVertex in range(1, G[N] + 1):
        currentPath = []
        visitedEdges = set()
        if backtrack(currentPath, visitedEdges, initialVertex):
            return currentPath

    return None    


'''
    Reads graph from keyboard
'''
def createGraph():

    ''' Adds a non-oriented edge (v,w) to the graph '''
    def addEdge(graph, edge):

        ''' Adds w as an out-neigbor of v '''
        def addNeighbor(v, w):
            neighbors = graph[ADJACENCY_LISTS].get(v)
            if neighbors == None:
                neighbors = {}
                graph[ADJACENCY_LISTS][v] = neighbors

            neighbors[w] = neighbors.get(w, 0) + 1
        ###
    
        addNeighbor(edge[0], edge[1])
        addNeighbor(edge[1], edge[0])
        graph[M] += 1
    ###    
        
    n = input("Number of vertices (empty to end): ")
    if len(n) == 0:
        return None
    
    G = [int(n), 0, {}]

    while True:
        nextEdgeAsString = input("Next edge (comma separated, empty to end): ")
        if len(nextEdgeAsString) == 0:
            break
        nextEdgeAsList = nextEdgeAsString.split(',')
        nextEdge = (int(nextEdgeAsList[0]), int(nextEdgeAsList[1]))
        addEdge(G, nextEdge)
        
    return G


'''
    G: a graph
    path: a list of vertices representing a path in G
'''
def printPath(G, path):
    if len(path) > 0:
        print(path[0][0], end="")
        for edge in path:
            origin = edge[0]
            destination = edge[1]
            isMultiple = G[ADJACENCY_LISTS].get(origin).get(destination) > 1
            print("--", end="") 
            if isMultiple:
                edgeLabel = chr(ord('a') + edge[2] - 1) 
                print("(" + edgeLabel + ")--", end="")
            print(destination, end="")
    print()
                

##### Main

while True:
    G = createGraph()
    if G is None:
        break

    print()
    
    doubleTracing = findDoubleTracing(G)
    if doubleTracing is not None:
        printPath(G, doubleTracing)
    else:
        print("The graph is NOT double-traceable.")
    print("\n========\n")

print("Bye!")

    








            

    
