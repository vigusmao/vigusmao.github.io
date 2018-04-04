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
    def backtrack(currentPath, visitedEdges):
        if len(currentPath) == 2 * G[M]:
            return True  # found a double tracing!

        latestEdge = currentPath[-1] if len(currentPath) > 0 else None
        currentVertex = latestEdge[1] if latestEdge is not None else 1
        
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

                    if backtrack(currentPath, visitedEdges) == True:
                        return True

                    # restores the previous state so we can move along to the next candidate state
                    currentPath.pop()
                    visitedEdges.remove(edge)

        return False
    
    ###

    currentPath = []
    visitedEdges = set()
    return currentPath if backtrack(currentPath, visitedEdges) else None
    

''' Adds a non-oriented edge (v,w) to the given graph '''
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
                

def printGraph(G):
    for v in range(1, G[N] + 1):
        neighbors = sorted([w for w in G[ADJACENCY_LISTS].get(v, {}).keys()])
        print(str(v) + " ---> " + str(neighbors))

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

            if cubic_graph:
                return G



##### Main

n = int(input("Quantos vertices? "))

count = 0

while True:
    G = generate_cubic_graph(n)

    doubleTracing = findDoubleTracing(G)
    if doubleTracing is not None:
        count += 1
        print("Double tracing ok (total so far = %d)" % count)
    else:
        print("Found a cubic graph that is NOT double-traceable!!!")
        printGraph(G)
        break


print("\nBye!")

    







