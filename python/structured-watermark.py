# -------------------------------------------------------------
#
#   Randomized graph-based watermarking for structured software
#   Codec Maceio 4
#   Rio de Janeiro, March 2016
#
# -------------------------------------------------------------

from random import randint

# watermark stucture over a list
KEY_LENGTH = 0
PATH_EDGES = 1
BACK_EDGES = 2
FW_EDGES = 3
SELF_LOOPS = 4

# global
VERBOSE = False


def encode(key):
    watermark = [None] * 5

    # converts integer key to binary
    binary = bin(key)[2:]
    N = len(binary)
    watermark[KEY_LENGTH] = N

    if VERBOSE:   
        print("B = %s (n = %d)" % (binary, N))

    watermark[PATH_EDGES] = [True] * (N+1) + [False]
    watermark[BACK_EDGES] = [None] * (N+2)
    watermark[FW_EDGES] = [None] * (N+2)

    S = [[0],[]]              # stacks S0 and S1
    A = [0] + [None] * (N+1)  # records the size of S' by the time each vertex is added to S
    D = [0] * (N+2)           # keeps track of the number of incoming backedges

    #max_incoming_back_edges = randint(1, int(N**0.5))
    max_incoming_back_edges = N

    bit_pos = 1
    v = 1
    
    while bit_pos < N:

        if v >= 2 and watermark[FW_EDGES][v-2] == v:
            # this is a fill-in vertex, which does not correspond to any bit -- let's just skip it
            v += 1
            continue
        
        bit = int(binary[bit_pos])

        vertex_parity = v % 2
        vertex_complement = (v+1) % 2

        stack_parity = (bit + v) % 2
        stack_complement = (stack_parity + 1) % 2

        size = len(S[stack_parity])
        if watermark[BACK_EDGES][v-1] != None:
            # We do not allow a vertex to have a back edge with the same head as
            # the back edge of its predecessor along the path
            size -= 1

        add_to_stack = True
       
        if size > 0:
        # a back edge *may* be added
            
            if watermark[FW_EDGES][v-1] != None:
            # if the previous vertex is the tail of a forward edge
                if bit == 1:
                    j = size-1  # we want a back edge to its predecessor in the path
                    watermark[PATH_EDGES][v] = False
                    # vertices v-1, v and v+1 will correspond to a while...do
                else: 
                    j = None
                    # vertices v-1, v and v+1 will correspond to an if...then
            else:       
                j = randint(0, size-1)

            if j != None:
            # a back edge will be added
                w = S[stack_parity][j]
                watermark[BACK_EDGES][v] = w
                D[w] += 1

                S[stack_parity][j+1:] = []
                if D[w] == max_incoming_back_edges:
                    del(S[stack_parity][j])
            
                S[stack_complement][A[w]:] = []

                add_to_stack = False

        else:
        # no back edge can be added

            if bit == 0:
            # bit "0"
                # let's just leave it without back edges or forward edges 
                
                if watermark[FW_EDGES][v-1] != None:
                # if the previous vertex is the tail of a forward edge   

                    add_to_stack = False
                    # vertex v cannot be the head of any back edge yet to be added
            else:
            # bit "1"
                # a forward edge will be added to an extra "fill-in" vertex
                watermark[PATH_EDGES][-1:] = [True, False]
                watermark[BACK_EDGES] += [None]
                watermark[FW_EDGES] += [None]
                watermark[FW_EDGES][v] = v+2

                A += [None]
                D += [0]

        if add_to_stack:
            S[vertex_parity] += [v]
            A[v] = len(S[vertex_complement])

        bit_pos +=1
        v += 1

    return watermark


def decode(watermark):
    N = watermark[KEY_LENGTH]
    bits = [0] * N
    bits[0] = 1
    key = 2**(N-1)

    bit_pos = 1
    v = 1
    
    while  bit_pos < N:
        if v >= 2 and watermark[FW_EDGES][v-2] == v:
            # this is a fill-in vertex, which does not correspond to any bit -- let's just skip it
            v += 1
            continue

        elif watermark[FW_EDGES][v] != None:
            # it has a fwd edge, hence it's a 1
            bits[bit_pos] = 1
        elif watermark[BACK_EDGES][v] == None:
            # it has neither fwd or back edges, hende it's a 0
            bits[bit_pos] = 0
        else:
            # it has a back edge, let's check the parity of the "jump length"
            bits[bit_pos] = (v - watermark[BACK_EDGES][v]) % 2

        key += bits[bit_pos] * 2**(N-bit_pos-1)

        bit_pos +=1
        v += 1

    return key


def print_watermark(watermark, print_edges):
    KEY_LENGTH = len(watermark[PATH_EDGES])

    if print_edges:

        # prints the path edges 
        print("\nPath edges:\n")
        printed_some = False
        for v in range(0, KEY_LENGTH):
            if watermark[PATH_EDGES][v]:
                print("%3d ---> %d" % (v+1, v+2))
                printed_some = True
        if not printed_some:
            print("  None.")

        # prints the back edges
        print("\nBack edges:\n")
        printed_some = False
        for v in range(0, KEY_LENGTH):
            destination = watermark[BACK_EDGES][v]
            if destination != None:
                print("%3d << %d" % (destination+1, v+1))
                printed_some = True
        if not printed_some:
            print("  None.")

        # prints the forward edges
        print("\nForward edges:\n")
        printed_some = False
        for v in range(0, KEY_LENGTH):
            destination = watermark[FW_EDGES][v]
            if destination != None:
                print("%3d >> %d" % (v+1, destination+1))
                printed_some = True
        if not printed_some:
            print("  None.")


    print("\nWatermark:\n")
    print("", end="")
    for v in range(0, KEY_LENGTH):
        w = watermark[BACK_EDGES][v]
        if w != None:
            print(" "*(2 + len(str(v+1)) - len(str(w+1))) + "%d<<" % (w+1), end="")
        else:
            print("", end=" "*(4 + len(str(v+1))))
                  
    print("\n    ", end="")
    for v in range(0, KEY_LENGTH-1):
        print("%d" % (v+1), end="")
        if watermark[PATH_EDGES][v]:
            print("--->", end="")
        else:
            print("    ", end="")
    print(KEY_LENGTH)

    print("    ", end="")
    for v in range(0, KEY_LENGTH):
        w = watermark[FW_EDGES][v]
        if w != None:
            print(">>%d" % (w+1), end=" "*(2 + len(str(v+1))-len(str(w+1))))
        else:
            print("", end=" "*(4 + len(str(v+1))))
    print()


def print_line(caracter = '-'): 
    print("\n" + caracter * 40 + "\n")
    

##########
#        #
#  Main  #
#        #
##########

while True:
    try:
        key_list = list(eval(input(
            "Options: " +
            "\n  an integer positive key --> for encoding/decoding in verbose mode;" +
            "\n  min_key, max_key (comma-separated) --> for testing over a range;" +
            "\n  <enter> --> quit." +
            "\n\nPlease type the key: ") + ","))
    except:
        break

    min_key = key_list[0]
    max_key = key_list[1] if len(key_list) > 1 else key_list[0]
    if min_key < 1 or max_key < min_key:
        break

    VERBOSE = max_key == min_key
    successes = 0

    for key in range(min_key, max_key + 1):       

        watermark = encode(key)

        if VERBOSE:
            print_watermark(watermark, True)
            print("Testing decoding procedure...")

        retrieved_key = decode(watermark)

        if VERBOSE:
            print("Retrieved key: %d" % retrieved_key)
        if retrieved_key == key:
            successes += 1
        else:
            print("Decoding failed!!!" +
                  "\nEncoded: %d \nRetrieved: %d" % (key, retrieved_key))
            break

    print("%d key(s) encoded/decoded successfully." % successes)
    print_line("=")

     
print("Bye.\n")
