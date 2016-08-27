# Simulador de resultados de tenis-de-mesa
# Vinicius Gusmao, agosto de 2016

from random import random
 
# config
PROB_A = 0.55  # a probabilidade de um ponto qualquer ser vencido pelo jogador A
TAMANHO_PARTIDA = 11  # a duracao de uma partida, em pontos
N_PARTIDAS = 10  # o numero de partidas da simulacao
IMPRIMIR_PONTOS = False
IMPRIMIR_PARTIDAS = True

# const
A = 0
B = 1

def imprimir_pontos(pontos):
    print("%2d x %2d" % (pontos[A], pontos[B]))


total_pontos = [0, 0]
total_partidas = [0, 0]
   
for i in range(N_PARTIDAS):
    pontos = [0, 0]
    campeao = None
    while campeao == None:
        if random() < PROB_A:
            pontos[A] += 1
        else:
            pontos[B] += 1

        if IMPRIMIR_PONTOS:
            imprimir_pontos(pontos)

        if pontos[A] >= TAMANHO_PARTIDA and \
           pontos[B] < max(TAMANHO_PARTIDA - 1, pontos[A] - 1):
            campeao = A
        elif pontos[B] >= TAMANHO_PARTIDA and \
             pontos[A] < max(TAMANHO_PARTIDA - 1, pontos[B] - 1):
            campeao = B

    total_partidas[campeao] += 1
    total_pontos[A] += pontos[A]
    total_pontos[B] += pontos[B]

    if IMPRIMIR_PARTIDAS:
        if IMPRIMIR_PONTOS:
            print()  # nao ha necessidade de repetir o placar final, apenas pule uma linha
        else:
            imprimir_pontos(pontos)  # a partida terminou, imprima o resultado final
        

total_pontos_disputados = total_pontos[A] + total_pontos[B]

print("\nTotal de pontos do jogador A: %d (%.2f%%)" % \
      (total_pontos[A], 100.0 * total_pontos[A] / total_pontos_disputados))
print("Total de pontos do jogador B: %d (%.2f%%)" % \
      (total_pontos[B], 100.0 * total_pontos[B] / total_pontos_disputados))

print("\nMedia de pontos por partida do jogador A: %.1f" % \
      (1.0 * total_pontos[A] / N_PARTIDAS))
print("Media de pontos por partida do jogador B: %.1f" % \
      (1.0 * total_pontos[B] / N_PARTIDAS))

print("\nTotal de partidas vencidas pelo jogador A: %d (%.2f%%)" % \
      (total_partidas[A], 100.0 * total_partidas[A] / N_PARTIDAS))
print("Total de partidas vencidas pelo jogador B: %d (%.2f%%)" % \
      (total_partidas[B], 100.0 * total_partidas[B] / N_PARTIDAS))
      
        

