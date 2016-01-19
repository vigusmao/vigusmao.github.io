#!/usr/bin/env python3

"""Randomized codec for graph-based
   software watermarking
"""

from random import randint

def encode(key):
    """Translates the given key onto the
       randomized watermark graph.
    """
    binary = bin(key)[2:]
    n = len(binary)
    S = [[0],[]]
    A = [0] + [None] * (n-1)
    back_to = [None] * n

    for v in range(1, n):
        vertex_parity = v % 2
        vertex_complement = (v+1) % 2
        stack_parity = (int(binary[v]) + v) % 2
        stack_complement = (stack_parity + 1) % 2

        size = len(S[stack_parity])
        if size > 0:
            j = randint(0, size-1)
            w = S[stack_parity][j]
            back_to[v] = w
            S[stack_parity][j+1:] = []
            S[stack_complement][A[w]:] = []

        S[vertex_parity] += [v]
        A[v] = len(S[vertex_complement])

    vertices = [v for v in range(n+1)]
    path_edges = [(v, v+1) for v in range(n)]
    back_edges = [(v, back_to[v]) for v in range(n)]

    watermark = (vertices, path_edges, back_edges)
    return watermark

def decode(watermark):
    """Decodes the given watermark.
    """
    back_edges = watermark[2]
    n = len(watermark[0]) - 1

    bits = [0] * n
    bits[0] = 1
    key = 2**(n-1)
     
    for i in range(len(back_edges)):
        if back_edges[i][1] == None:
            bits[i] = 0
        else:
            bits[i] = (i - back_edges[i][1]) % 2

        key += bits[i] * 2**(n-i-1) 

    return key

def print_watermark(watermark):
    """Prints the watermark.
    """
    vertices = watermark[0]
    back_edges = watermark[2]
    n = len(vertices) - 1

    # prints the path edges 
    print("\nWatermark (Hamiltonian path):")
    for v in vertices[:-1]:
        print(v+1, end="")
        print("-->", end="")
    print(vertices[-1]+1)

    # prints the back edges
    print("\nWatermark (back edges):")

    for i in range(len(back_edges)):
        print(back_edges[i][0]+1, end="")
        back_to = back_edges[i][1]
        if back_to == None:
            print()
            continue
        print(" ----> " + str(back_to+1))
    print(n+1)

def main():
    """Tests the encoding/decoding.
    """
    try:
        key = eval(input("Please type the key (<enter> to quit): "))
    except:
        return

    if key < 1:
        return

    watermark = encode(key)
    print_watermark(watermark)

    print("\nTesting decoding procedure...")
    retrieved_key = decode(watermark)
    print("Retrieved key = %d" % retrieved_key)
    if retrieved_key == key:
        print("Watermark decoded successfully.")
    else:
        print("Decoding failed.")

main()
