from random import randrange 

# readability constants
N = 0
M = 1
ADJACENCY_LISTS = 2


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
            


n = int(input("Quantos vertices? "))

G = generate_cubic_graph(n)
printGraph(G)


