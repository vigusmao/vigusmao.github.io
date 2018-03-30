# readability constants
N = 0
M = 1
ADJACENCY_LISTS = 2

'''
    G: a (multi-)graph in the form of a list
       [n, m, dictionary {vertex: list of (repeated) neighbors}],
       where n and m are the vertex count and edge count, respectively
'''
def findDoubleTracing(G):

    '''
        currentPath: a list of vertices in the order they were visited
        visitedEdges: a set of ordered pairs indicating which edges were visited
    '''
    def backtrack(currentPath, visitedEdges):
        if len(currentPath) == 2 * G[M] + 1:
            return True  # found a double tracing!

        currentVertex = currentPath[-1]
        neighbors = G[ADJACENCY_LISTS].get(currentVertex)

        if neighbors != None:
            for nextVertex in neighbors:
                if (currentVertex, nextVertex) in visitedEdges:
                    continue  # edge already visited
                if len(currentPath) > 1 and currentPath[-2] == nextVertex:
                    continue  # avoiding U-turns

                # changes the current state
                currentPath.append(nextVertex)
                visitedEdges.add((currentVertex, nextVertex))

                if backtrack(currentPath, visitedEdges) == True:
                    return True

                # restores the previous state so we can move along to the next candidate state
                currentPath.pop()
                visitedEdges.remove((currentVertex, nextVertex))

        return False
    
    ###

    if G[N] == 0:
        return []
    
    currentPath = [1]
    visitedEdges = set()
    return currentPath if backtrack(currentPath, visitedEdges) else None
    

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
                neighbors = []
                graph[ADJACENCY_LISTS][v] = neighbors
            neighbors.append(w)
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
    path: a list of vertices
'''
def printPath(path):
    if len(path) > 0:
        for i in range(len(path) - 1):
            print(path[i], ",", sep="", end="")
        print(path[0])


##### Main

while True:
    G = createGraph()
    if G is None:
        break
    
    doubleTracing = findDoubleTracing(G)
    if doubleTracing is not None:
        printPath(doubleTracing)
    else:
        print("The graph is NOT double-traceable.")
    print("\n---------\n")

print("Bye!")

    








            

    
