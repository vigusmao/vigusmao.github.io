#
#    All (multi-)graphs in this program will be given in the form of a list
#       [n, m, dictionary {vertex: hash set {neighbor: multiplicity} of neighbors}],
#       where `n` and `m` are the vertex count and edge count, respectively,
#       and `multiplicity` indicates the number of edges from `vertex` to `neighbor`.
#


from random import randrange

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
    

''' Adds a non-oriented edge (v,w) to the given graph '''
def addEdge(graph, edge):

    ''' Adds w as an out-neigbor of v '''
    def addNeighbor(v, w):
        neighbors = graph[ADJACENCY_LISTS].get(v)
        if neighbors is None:
            neighbors = {}
            graph[ADJACENCY_LISTS][v] = neighbors

        neighbors[w] = neighbors.get(w, 0) + 1
    ###

    addNeighbor(edge[0], edge[1])
    addNeighbor(edge[1], edge[0])
    graph[M] += 1


''' Removes an edge from the given graph '''
def removeEdge(graph, edge):

    def removeNeighbor(v, w):
        neighbors = graph[ADJACENCY_LISTS].get(v)
        if neighbors is not None:
            neighborMultiplicity = neighbors.get(w, 0)
            if neighborMultiplicity == 1:
                del(neighbors[w])
            elif neighborMultiplicity > 1:
                neighbors.put(w, neighborMultiplicity - 1)
    ###

    removeNeighbor(edge[0], edge[1])
    removeNeighbor(edge[1], edge[0])
    graph[M] -= 1                   
        

'''
    Reads graph from keyboard
'''
def createGraph():

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
                

def getNeighborsList(G, v):
    return [w for w in G[ADJACENCY_LISTS].get(v, {}).keys()]

def printGraph(G):
    for v in range(1, G[N] + 1):
        neighbors = sorted(getNeighborsList(G, v))
        print(str(v) + " ---> " + str(neighbors))


def isConnected(G):

    def dfs(v, parent):
        neighbors = getNeighborsList(G, v)
        for w in neighbors:
            if parent.get(w) is None:
                parent[w] = v
                dfs(w, parent)

    parent = {v : None for v in range(1, G[N] + 1)}
    dfs(1, parent)
    for v in range(2, G[N] + 1):
        if parent.get(v) is None:
            return False
    return True


def generate_cubic_graph(n):
    points = [x for x in range(0, 3*n)]

    while True:
        group_pairs = set()

        for i in range(3*n):
            j = randrange(i, len(points))
            points[i], points[j] = points[j], points[i]

        matching_ok = True
        for start_idx in range(0, 3*n, 2):
            found_pair = False
            for v_idx in range(start_idx, 3*n):
                v = points[v_idx]
             
                for w_idx in range(v_idx+1, 3*n):
                    w = points[w_idx]
                    group_v = v // 3
                    group_w = w // 3
                    if group_v == group_w:
                        continue
                    group_pair = (group_v, group_w) if group_v < group_w else (group_w, group_v)
                    if group_pair in group_pairs:
                        continue
                    group_pairs.add(group_pair)
                    found_pair = True
                    break
                
                if found_pair:
                    points[v_idx+1], points[w_idx] = points[w_idx], points[v_idx+1]
                    break

            if not found_pair:
                matching_ok = False
                break
    
        if matching_ok:
            G = [n, 0, {}]        
            for group_pair in group_pairs:
                addEdge(G, (group_pair[0] + 1, group_pair[1] + 1, 1))

            cubic_graph = True
            for v, neighbors in G[ADJACENCY_LISTS].items():
                if len(neighbors) != 3:
                    cubic_graph = False
                    break

            if cubic_graph and isConnected(G):
                return G


def generate_cubic_graph_with_one_vertex_of_degree_two(n):
    G = generate_cubic_graph(n-1)
    
    chosenEdgeIndex = randrange(G[M])
    chosenEdge = None
    
    steps = 0
    while steps < G[M]:
        for v, neighbors in G[ADJACENCY_LISTS].items():
            if neighbors is None or len(neighbors) == 0:
                continue
            for w, neighborMultiplicity in neighbors.items():
                if steps == chosenEdgeIndex:
                    chosenEdge = (v, w)
                    steps = G[M]
                    break
                steps += 1
        
    removeEdge(G, chosenEdge)
    G[N] = n
    addEdge(G, (n, chosenEdge[0]))
    addEdge(G, (n, chosenEdge[1]))

    return G    


##### Main

n = int(input("Quantos vertices? "))

count = 0

while True:
    G = generate_cubic_graph_with_one_vertex_of_degree_two(n)
    printGraph(G)
    break
##    doubleTracing = findDoubleTracing(G)
##    if doubleTracing is not None:
##        count += 1
##        print("Double tracing ok (total so far = %d)" % count)
##    else:
##        print("Found a cubic graph that is NOT double-traceable!!!")
##        printGraph(G)
##        break


print("\nBye!")

    







