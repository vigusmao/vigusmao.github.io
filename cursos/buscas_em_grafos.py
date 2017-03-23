prof_entrada = {}  # hash map (aka 'dicionario')
prof_saida = {}
pai = {}


def criar_grafo(n):
    grafo = []
    for _ in range(n):
        grafo.append(set())    
    return grafo

def adicionar_aresta(G, vertice1, vertice2):
    G[vertice1].add(vertice2)
    G[vertice2].add(vertice1)

def busca_prof(G, v):
    prof_entrada[v] = len(prof_entrada) + 1
    for w in G[v]:
        if prof_entrada.get(w) is None:
            pai[w] = v

            # posso fazer algo com relacao aa aresta de arvore aqui
            print("O vertice %d eh filho do vertice %d" % (w, v))
            
            busca_prof(G, w)  # chamada recursiva
            
            # posso fazer algo com relacao aa aresta de arvore aqui
            print("Terminei a visita ao filho %d de %d" % (w,v))
            
        else:
            if prof_saida.get(w) is None and pai[v] != w:
                # visito aresta de retorno (v, w)
                print("Encontrei aresta de retorno (%d,%d)" % (v,w))
                
    prof_saida[v] = len(prof_saida) + 1

             
                    
            



## Main

    
