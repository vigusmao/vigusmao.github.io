# -----------------------------------------------------
#
#   Graph-based watermarking
#   Rio de Janeiro, March 2013
#
# -----------------------------------------------------

from time import time
from random import randint


DEBUG = False
KEY_RANGE = True
PRINT_TESTS = False
PRINT_KEY_SUMMARY = False
PRINT_FAILURES = True
PRINT_TREE = False
FILTER_BY_PROPERTIES = True
LINEAR_TIME_ALGORITHM = True


#   Key-shift parameter
K = 0


N, B, S, T = 0, 0, 0, 0


def generate_watermark(key):

    global N, B, S, T;

    if DEBUG: print("w (key) = %d" % key)
    
    # converts integer key to binary
    binary = bin(key)[2:]
    N = len(binary)
    n_0 = 0
    for i in range(1, N+1):
        if binary[i - 1] == "0":
            n_0 += 1
    n_1 = N - n_0
    if DEBUG:
        print("\nB (binary) =", binary)
        print("\nn (size of B) =", N)
        print("n_0 (number of 0's in B) =", n_0)
        print("n_1 (number of 1's in B) =", n_1)

    f_0 = -1
    for i in range(1, N+1):
        if binary[i - 1] == "0":
            f_0 = i
            break
    if DEBUG: print("f_0 =", f_0)

    # adds 0's and 1's to the original binary
    extended_binary = "0" * (len(binary) + 2 * K) + binary + "10" * K + "1"
    B = len(extended_binary)
    if DEBUG: print("B' (extended binary) =", extended_binary)

    # flips all digits
    flipped_extended_binary = ""
    for digit in extended_binary:
        flipped_extended_binary += str((int(digit) + 1) % 2)
    if DEBUG:
        print("B* (flipped extended binary) =", flipped_extended_binary)
        print("n* (size of B*) =", B) 

    # determines the indexes of 0's and 1's in B*
    x, y = [], []
    for index in range(len(flipped_extended_binary)):
        if flipped_extended_binary[index] == "0":
            x += [index+1]
        else:
            y += [index+1]
    if DEBUG: print("X (indexes of 0's in B*) =", x,
                    "\nY (indexes of 1's in B*) =", y)

    # obtains the bitonic permutation
    bitonic_permutation = x[:] + y[::-1]
    if DEBUG: print("P_b (bitonic permutation) =", bitonic_permutation)

    # determines all n 2-cycles and the single 1-cycle
    central_index = B // 2
    cycles = []
    for index in range(central_index):
        cycle = (bitonic_permutation[index], bitonic_permutation[-1-index])
        if cycle[0] > cycle[1]:
            cycle = (cycle[1], cycle[0])
        cycles += [cycle]
    cycles += [(bitonic_permutation[central_index],) * 2]
    if DEBUG: print("cycles =", cycles)

    # obtains the self-inverting permutation
    permutation = [None] * (B+1)
    for cycle in cycles:
        permutation[cycle[0]] = cycle[1]
        permutation[cycle[1]] = cycle[0]
    self_inverting_permutation = permutation[1:]
    if DEBUG: print("P_s (self-inverting permutation) =", self_inverting_permutation)

    if DEBUG: print("f =", bitonic_permutation[central_index])

    # adds S and T to the permutation, obtaining the preorder traversal of the representative tree
    global S
    S = B+1
    preorder_traversal = [S] + self_inverting_permutation + [T]

    # determines p(x) for all x in 1,...,2n+1
    parents = [None] * (B+1)
    children = []
    for i in range(S+1):
        children += [[]]
    stack = [S]
    for element in preorder_traversal[1:-1]:
        while element > stack[-1]:
            del stack[-1]
        parents[element] = stack[-1]
        children[stack[-1]] += [element]
        stack += [element]

    return bitonic_permutation, parents, children


def print_watermark(path_edges, tree_edges):

    # prints the path edges 
    print("\nWatermark (Hamiltonian path):\n")
    for i in range(2*N + 2, 0, -1):
        if i == S:
            origin = "S"
        else:
            origin = str(i)
        print(origin, end="")
        if path_edges[i]:
            print("-->", end="")
        else:
            print("  [REMOVED]  ", end="")
    print("T")

    # prints the tree edges
    print("\nWatermark (tree edges):\n")

    for i in range(B, 0, -1):
        parent = tree_edges[i]
        msg = ""
        if parent < 0: # if logically deleted
            parent = parent * (-1)
            msg = " [REMOVED]"
        if parent == S: parent = "S"
        print(str(i) + " ----> " + str(parent) + msg)


def print_tree(children, tree_edges):
    
    print("\nRepresentative tree:")
    for i in range(S, 0, -1):
        parent = i
        if parent == S: parent = "S"
        print("\n%s ------ " % str(parent), end="")
        children_str = ""
        for j in children[i]:
            if tree_edges[j] > 0: # if not logically deleted
                children_str += str(j) + ", "
        if len(children_str) > 0:
            children_str = children_str[:-2]
        print(children_str, end="")
        
    print("")


def delete_path_edge(path_edges, origin):
    path_edges[origin] = False # logical deletion


def delete_tree_edge(tree_edges, origin):
    tree_edges[origin] = tree_edges[origin] * (-1) # logical deletion (we don't want to lose the destination info)


def DFS(neighbors, forest):

    visited = [False] * (S+1)

    vertex = S
    while vertex > T: 
        if not visited[vertex]:
            forest += [[]]
            DFS_recurse(vertex, neighbors, visited, forest[-1])
        vertex -= 1


def DFS_recurse(vertex, neighbors, visited, seq_tree):
    
    visited[vertex] = True
    seq_tree += [vertex]

    for vizinho in neighbors[vertex]: # by construction, each adjacency list is ordered by label
        DFS_recurse(vizinho, neighbors, visited, seq_tree)

def choose(n, k):
    if 0 <= k <= n:
        p = 1
        for t in range(min(k, n - k)):
            p = (p * (n - t)) // (t + 1)
        return p
    else:
        return 0
 
def revert_edges(neighbors, tree_edges):
    for i in range(1, len(tree_edges)):
        destino = tree_edges[i]
        if destino > 0:
            neighbors[destino] += [i]


def get_indegree(vertex, path_edges, tree_edges, children_lists, excluded_neighbors_list):
    
    indegree = 0
    if vertex != S:
        if path_edges[vertex+1] and (vertex+1 not in excluded_neighbors_list):
            indegree += 1
    if vertex != T:
        for child in children_lists[vertex]:
            if (tree_edges[child]) and (child not in excluded_neighbors_list):
                indegree += 1
    
    return indegree


def get_outdegree(vertex, path_edges, tree_edges, excluded_neighbors_list):

    if vertex == T:
        return 0
    if vertex == S:
        if 2*N + 2 not in excluded_neighbors_list:
            return 1
        else:
            return 0
    
    outdegree = 0
    if path_edges[vertex] and (vertex - 1 not in excluded_neighbors_list):
        outdegree += 1
    if (tree_edges[vertex] > 0) and (tree_edges[vertex] not in excluded_neighbors_list):
        outdegree += 1

    return outdegree
    

def collect_vertices_by_indegree(input_vertices, output_vertices, path_edges, tree_edges,
                                 children_lists, excluded_neighbors_list, intended_indegree):

    for v in input_vertices:
        indegree = get_indegree(v, path_edges, tree_edges, children_lists, excluded_neighbors_list)
        if indegree == intended_indegree:
            output_vertices.add(v)
            
def collect_vertices_by_outdegree(input_vertices, output_vertices, path_edges, tree_edges,
                                  excluded_neighbors_list, intended_outdegree):

    for v in input_vertices:
        outdegree = get_outdegree(v, path_edges, tree_edges, excluded_neighbors_list)
        if outdegree == intended_outdegree:
            output_vertices.add(v)

def locate_bitonic_apex(permutation):
    greatest = 0
    index_of_greatest = 0
    for index in range(len(permutation)):
        if permutation[index] > greatest:
            greatest = permutation[index]
            index_of_greatest = index
    return greatest, index_of_greatest

def check_bitonic_property(permutation):
    
    if permutation[1] > permutation[0]:
        direction = 1
    else:
        direction = -1

    index = 1
    changed_direction = False
    while index < len(permutation):
        if (permutation[index] - permutation[index-1]) * direction < 0:
            if changed_direction:
                return False
            else:
                direction = -1 * direction
                changed_direction = True
        index += 1
    return True

def check_apex_vicinity(permutation):
    greatest, index_of_greatest = locate_bitonic_apex(permutation)

    for i in range(1, K + 1):
        if permutation[index_maior - i] != greatest - 2*i or \
           permutation[index_maior + i] != greatest - 2*i + 1:
            return False

    return True

def obtain_bitonic(permutation):
    bitonic_permutation = [None] * len(permutation)

    for i in range(len(permutation)):
        if permutation[i] == i+1: 
            central_element = i+1
            if central_element <= len(permutation) // 2: # invalid central element
                return None
            bitonic_permutation[len(permutation)//2] = central_element
            break

    pairs = {}
    for i in range(len(permutation)):
        pairs[permutation[i]] = i+1
        pairs[i+1] = permutation[i]
            
    for i in range(1, len(permutation)//2 + 1):
        bitonic_permutation[-i] = i
        bitonic_permutation[i-1] = pairs[i]
    
    if check_bitonic_property(bitonic_permutation) and \
       check_apex_vicinity(bitonic_permutation):
        return tuple(bitonic_permutation)
    else:
        return None

def determine_all_bitonic_permutation_candidates(permutations, bitonic_permutations):

    for permutation in permutations:
        bitonic = obtain_bitonic(permutation)
        if bitonic != None:
            bitonic_permutations.add(bitonic)

def check_self_invertibility(permutation):
    for i in range(len(permutation)):
        if permutation[permutation[i]-1] != i+1:
            return False
    return True

def reconstruct_self_inverting_permutations(blocks, self_inverting_permutations):

    def place_block(sequence, blocks, block_index, position, block_order, finished_sequences):
        block = blocks[block_order[block_index]]

        # places the current block at the specified position
        if position >= len(sequence):
            sequence += block
        else:
            sequence[position:position] = block[:]

        # if block was last, adds the sequence to the list of finished sequences
        if block_index == len(blocks) - 1:
            finished_sequences.add(tuple(sequence))
        else:
            for next_block_position in range(0, len(sequence) + 1):
                place_block(sequence[:], blocks, block_index + 1,
                               next_block_position, block_order, finished_sequences)

    if len(blocks) == 1:
        self_inverting_permutations.add(tuple(blocks[0])) # only one block, nothing to do
    else:    

        free_blocks_count = len(blocks) - 1

        permutations = []
        generate_permutations(free_blocks_count, free_blocks_count, permutations)

        sequences = set()

        for permutation in permutations:
            place_block([], blocks, 0, 0, [0] + permutation, sequences)

        for sequence in sequences:
            if check_self_invertibility(sequence):
                self_inverting_permutations.add(sequence)


def get_partial_hamiltonian_path(path_edges, tree_edges, children_lists, v):

    tree_edges_copy = tree_edges[:]
    x = v
    h = [x]
               
    while True:
        if S > x > T:
            tree_edges_copy[x] *= -1
        
        candidates = []
        for w in children_lists[x]:
            if tree_edges_copy[w] > 0:
                candidates += [w]

        if (x < S) and (path_edges[x+1]):
            candidates += [x+1]

        if len(candidates) == 0:
            return h

        if len(candidates) > 1:
            if DEBUG: print("\nAmbiguity determining H(%d)." % v)
            return []

        if candidates[0] not in h:
            h = [candidates[0]] + h
            x = candidates[0]
        else:
            break
                
    return h
        

## Generates all permutations of 'desired_size' elements among the x first postive integers starting from 'initial_value'
def generate_permutations(x, desired_size, permutations, initial_value = 1):

    def generate(temp_permutation, available_numbers, desired_size, permutations):

        index = 0
        while index < len(available_numbers):
            y = available_numbers.pop(index)
            temp_permutation += [y]

            if len(temp_permutation) == desired_size:
                permutations += [temp_permutation[:]]
            else:  
                generate(temp_permutation, available_numbers[:], desired_size, permutations)

            temp_permutation.pop(len(temp_permutation) - 1)
            available_numbers[0:0] = [y]
            index += 1

    temp_permutation = []
    available_numbers = list(range(initial_value, x + initial_value))
    generate(temp_permutation, available_numbers, desired_size, permutations) 


## Generates all subsets of {1, ..., 'set_size'} having cardinality 'subset_size'
def generate_subsets(set_size, subset_size, subsets):
    
    k = subset_size
    k_size_permutations = []
    generate_permutations(set_size, k, k_size_permutations)
    subsets_holder = set()
    for k_size_permutation in k_size_permutations:
        subset = frozenset(k_size_permutation[:])
        if not subset in subsets_holder:
            subsets_holder.add(subset)
            subsets += [subset]


def print_test_data(key, instance):

    if not DEBUG: print("key = %d" % key)
    missing_path_edges = instance[0]
    missing_tree_edges = instance[1]
    if (len(missing_path_edges) > 0) or (len(missing_tree_edges) > 0):
        print("%d missing edge(s): " % (len(missing_path_edges) + len(missing_tree_edges)), end="")
        msg = ""
        for missing_path_edge_origin in missing_path_edges:
            msg += "path edge with origin in " + str(missing_path_edge_origin) + ", "
        for missing_tree_edge_origin in missing_tree_edges:
            msg += "tree edge with origin in " + str(missing_tree_edge_origin) + ", "
        print(msg[:-2])


def print_permutations(permutations, type, log = None):

    msg = ""
    if len(permutations) == 0:
        msg = "No permutation %s was restored." % type
    elif len(permutations) == 1:
        msg = "1 permutation %s was restored:" % type
    else:
        msg = "%d permutations %s were restored:" % (len(permutations), type)

    for permutation in permutations:
        msg += "\n  " + str(permutation)

    if log != None:
        log[0] = log[0] + msg + "\n"
    else:
        print(msg)


def print_key_summary(key, tests_count, successes_count):

    print("\n\nkey = %d" % key)
    print("tests = %d" % tests_count)
    print("successes = %d (%.5f%%)" % (successes_count,
                                      successes_count * 100 / tests_count))


def print_results_summary(total_tests_count, total_successes_count):

    print("\n\nNUMBER OF TESTS = %d" % total_tests_count)
    print("TOTAL SUCCESSES = %d (%.5f%%)" % (total_successes_count,
                                               total_successes_count * 100 / total_tests_count))


def print_blank_line(caracter = '-'): 
        print("\n" + caracter * 40 + "\n")
    

def restore_hamiltonian_path(path_edges, tree_edges, children_lists):
    
    V0 = set()
    collect_vertices_by_outdegree(set(range(2*N+3)), V0, path_edges, tree_edges, [], 0)

    if len(V0) == 1:

        v0 = list(V0)[0]
        hv0 = get_partial_hamiltonian_path(path_edges, tree_edges, children_lists, v0)
        tree_edges_copy = tree_edges[:]
        for i in hv0:
            if S > i > T:
                tree_edges_copy[i] *= -1

        if len(hv0) == 2*N + 3:
            if DEBUG: print("\nFigure 4(a)")
            return hv0

        V1 = set()
        collect_vertices_by_outdegree(set(range(2*N + 3)) - set(hv0), V1, path_edges, tree_edges, [], 1)
        
        candidate_paths = []
        for v1 in V1:
            hv1 = get_partial_hamiltonian_path(path_edges, tree_edges_copy, children_lists, v1)
            if len(hv1) > 0:
                if len(hv1) + len(hv0) == 2*N + 3:
                    candidate_paths += [hv1]

        if tree_edges[N+1] > 0: # if tree edge with origin in n+1 is not missing, the root is determined right away
            i = len(candidate_paths) - 1
            while i >= 0:
                if (len(candidate_paths[i]) + len(hv0) == 2*N + 3) and \
                   (candidate_paths[i][0] != tree_edges[N+1]):
                    del(candidate_paths[i])
                i -= 1
                
        if len(candidate_paths) == 1: # a single candidate that completes the desired length survived
            if DEBUG: print("\nFigure 4(b,c)")
            h = candidate_paths[0] + hv0
            if len(h) == 2*N + 3:
                return h
        

        elif len(candidate_paths) == 0:  
            for v1 in V1:
                hv1 = get_partial_hamiltonian_path(path_edges, tree_edges_copy, children_lists, v1)
                if len(hv1) > 0 and (len(hv1) + len(hv0) < 2*N + 3):
                # now we only care about segments that will *not* complete the intended length
                    break
            
        else:
            # Two possible continuations for the Hamiltonian path... will choose the correct one.
            path = None
            for candidate_path in candidate_paths:
                root = candidate_path[0]
                other_vertex = candidate_path[1]
                # we know edges 2n+1-->2n and 2n+2<--n+1 are missing

                # Condition 1:
                # the root must have 3 ore more children, except if n is a child of 2n
                condition1ok = False
                if tree_edges[N] != 2*N:
                    # Condition 1 can be bypassed, since n is not a child of 2n.
                    condition1ok = True
                if not condition1ok:
                    for v in range(1, 2*N+1):
                        if tree_edges[v] == root:
                            # Condition 1 ok. The root has at least three children.
                            condition1ok = True
                            break
                # Condition 2:
                # all non-children descendants of the root must descend from the same root's child
                condition2ok = True
                root_children_with_children = 0
                if len(children_lists[other_vertex]) > 0:
                    root_children_with_children += 1
                for v in range(1, 2*N+1):
                    if tree_edges[v] == root and len(children_lists[v]) > 0:
                        root_children_with_children += 1
                        # Found a child of the root with children of its own.
                if root_children_with_children > 1:
                    condition2ok = False
                    

                # Only one candidate path can possibly satisfy both conditions
                if condition1ok and condition2ok:
                    path = candidate_path + hv0
                    break

            if path != None:
                if DEBUG: print("\nFigure 4(b,c)")
                return path

        # if no H(v1) completed the whole hamiltonian path,
        # we know that one of the following cases is true:
        # (i)  V1 has only one v1 such that H(v1) could be determined without ambiguity;
        # (ii) there are two v1 such that H(v1) could be determined without ambiguity, but in this case
        #      the tree edge with origin in 2n+1 is not missing and can be used to decide the correct path
        candidate_paths = []
        for v1 in V1:
            hv1 = get_partial_hamiltonian_path(path_edges, tree_edges_copy, children_lists, v1)
            if len(hv1) > 0:
                if (len(hv1) + len(hv0) != 2*N + 3) and \
                   tree_edges[N+1] not in hv1:
                    break

        for i in hv1:
            if S > i > T:
                tree_edges_copy[i] *= -1
        
        # |V1| is necessarily >= 2, here
        V1prime = V1 - set([v1])
        for v1prime in V1prime:
            hv1prime = get_partial_hamiltonian_path(path_edges, tree_edges_copy, children_lists, v1prime)

            if len(hv1prime) > 0:
                if tree_edges[N+1] == hv1prime[0]:
                    if DEBUG: print("\nFigure 4(d)")
                    return hv1prime + hv1 + hv0

        return []
        
    else:
        v0, v0prime = list(V0)[0], list(V0)[1]
        hv0 = get_partial_hamiltonian_path(path_edges, tree_edges, children_lists, v0)
        hv0prime = get_partial_hamiltonian_path(path_edges, tree_edges, children_lists, v0prime)
        tree_edges_copy = tree_edges[:]
        for i in hv0 + hv0prime:
            if S > i > T:
                tree_edges_copy[i] *= -1

        if len(hv0) == 0: # an ambiguity was found in hv0, therefore it is not the rightmost segment
            v0prime, v0 = v0, v0prime
            hv0prime, hv0 = hv0, hv0prime

        if len(hv0prime) == 0: # now the ambiguity will have been sorted out
            hv0prime = get_partial_hamiltonian_path(path_edges, tree_edges_copy, children_lists, v0prime)
            for i in hv0prime:
                if S > i > T:
                    tree_edges_copy[i] *= -1
        if len(hv0) + len(hv0prime) == 2*N + 3:
            if DEBUG: print("\nFigures 4(e,f)")
            return hv0prime + hv0

        V1 = set()
        collect_vertices_by_indegree(set(range(2*N + 3)) - set(hv0 + hv0prime), V1, path_edges, tree_edges,
                                     children_lists, hv0 + hv0prime, 0)
        collect_vertices_by_indegree(set(range(2*N + 3)) - set(hv0 + hv0prime), V1, path_edges, tree_edges,
                                     children_lists, hv0 + hv0prime, 1)

        v1 = list(V1)[0]
        hv1 = get_partial_hamiltonian_path(path_edges, tree_edges_copy, children_lists, v1)
        if DEBUG: print("\nFigures 4(g,h)")
        return hv0prime + hv1 + hv0


def test_codec(keys = None, number_of_missing_edges = 0):

    predetermined_keys = keys != None

    while True:

        total_tests_count = 0
        total_successes_count = 0
        total_failures_count = 0
            
        if predetermined_keys:
            test_removal_all_subsets = 'Y'
        else:
            if KEY_RANGE:
                try:
                    first_key = eval(input("Please type the first key in the range (<enter> to quit): "))
                    last_key = eval(input("Please type the last key in the range (<enter> to quit): "))
                    randomize_keys = input("Choose keys randomly in the range? (Y/N) ")
                    if randomize_keys in 'Yy':
                        number_of_random_keys = eval(input("How many keys in the range? "))
                    test_removal_all_subsets = 'Y'
                    number_of_missing_edges = eval(input("How many edges should be removed? "))
                except:
                    break
            else:
                try:
                    first_key = eval(input("Please type the key (<enter> to quit): "))
                    last_key = first_key
                    randomize_keys = 'N'
                    test_removal_all_subsets = input("Remove edges exhaustively (Y/N)? ")
                    if test_removal_all_subsets in 'Yy':
                        number_of_missing_edges = eval(input("How many edges should be removed? "))
                except:
                    break

            print("\n")

            if randomize_keys in 'Yy':
                keys = []
                for i in range(number_of_random_keys):
                    keys += [randint(first_key, last_key)]
            else:
                keys = range(first_key, last_key + 1)

        total_time = 0

        for key in keys:
            if PRINT_KEY_SUMMARY or DEBUG:
                print("\n")

            tests_count = 0
            successes_count = 0
            
            original_bitonic_permutation, original_tree_edges, children = generate_watermark(key)

            instances = []

            if test_removal_all_subsets in 'Yy':
                subsets = []
                if number_of_missing_edges > 0:
                    generate_subsets(4*N + 3, number_of_missing_edges, subsets)
                    for subset in subsets:
                        missing_path_edges = set()
                        missing_tree_edges = set()
                        for removed_edge in subset:
                            if removed_edge <= 2*N+2:
                                missing_path_edges.add(removed_edge)
                            else:
                                missing_tree_edges.add(removed_edge - (2*N + 2))
                        instances += [(missing_path_edges, missing_tree_edges)]
                        
            else:
                if DEBUG:
                    print("")
                missing_path_edges = set()
                missing_tree_edges = set()
                while True:
                    try:
                        origin = eval(input("Please type the origin of the *path* edge to be removed (<enter> to continue): "))
                        missing_path_edges.add(origin)
                    except:
                        break
                while True:
                    try:
                        origin = eval(input("Please type the origin of the *tree* edge to be removed (<enter> to continue): "))
                        missing_tree_edges.add(origin)
                    except:
                        break
                instances += [(missing_path_edges, missing_tree_edges)]

            if len(instances) == 0:
                instances += [(set(), set())]
            
            for instance in instances:

                if PRINT_TESTS or DEBUG: 
                    print_test_data(key, instance)

                total_tests_count += 1
                tests_count += 1

                path_edges = [True] * (2*N + 3) # vertices 1 to 2N+2 shall be the origin of a path edge
                tree_edges = original_tree_edges[:]
                
                for missing_path_edge_origin in instance[0]:
                    delete_path_edge(path_edges, missing_path_edge_origin)
                for missing_tree_edge_origin in instance[1]:
                    delete_tree_edge(tree_edges, missing_tree_edge_origin)

                if DEBUG: print_watermark(path_edges, tree_edges)
                if DEBUG or PRINT_TREE: print_tree(children, tree_edges)

                children_lists = []
                for i in range (S+1):
                    children_lists += [[]]
                revert_edges(children_lists, tree_edges)

                forest = []
                DFS(children_lists, forest)

                if DEBUG:
                    print("\nConnected components of the search forest:") 
                    forest[0][0] = "S"
                    for tree in forest:
                        print("  ", tree)

                start_time = time()

                # Restores the (possibly damaged) hamiltonian path

                hampath = restore_hamiltonian_path(path_edges, tree_edges, children_lists)
                
                ham_ok = True
                if len(hampath) != 2*N + 3:
                    ham_ok = False
                else:
                    for i in range(0, 2*N + 3):
                        if hampath[i] != 2*N + 2 - i:
                            ham_ok = False
                            break

                if ham_ok:    
                    if DEBUG: print("\nHamiltonian path restored successfully -- vertices have been labeled accordingly.")
                    retrieved_key = 0
                else:
                    if DEBUG:
                        print("\nFailed to restore Hamiltonian path -- vertices could not be labeled.")
                    retrieved_key = -1



                if LINEAR_TIME_ALGORITHM:

                #############################
                ##                         ##
                ##  Linear-time algorithm  ##
                ##                         ##
                #############################
                        

                # Restores the representative tree
                    if retrieved_key == 0:
                            
                        f_value = 0
                        
                        # checks whether f = 2n+1

                        f_2n_plus_1 = True
                        for child in children[2*N+1]:
                            if tree_edges[child] > 0: # if not logically deleted
                                f_2n_plus_1 = False
                                break

                        if f_2n_plus_1:
                            for i in range(1, N+1): # checks the parents of the small vertices
                                if tree_edges[i] < 0: # bypasses logically deleted edges
                                    continue
                                if tree_edges[i] != 2*N:
                                    f_2n_plus_1 = False
                                    break

                        if f_2n_plus_1:

                            f_value = 2*N + 1
                            if DEBUG: print("Fixed element f found (case f = 2n+1): ", f_value)
                            retrieved_key = 2**((f_value-1)/2)-1
                            
                        else:

                        # we already know f is not 2n+1 

                            # Condition (i)
                            for x in range(N+1, 2*N+1):
                                pai_x = tree_edges[x]
                                if (pai_x > 0) and (pai_x != S):
                                    for y in children[pai_x]:
                                        if y == x:
                                            continue
                                        if tree_edges[y] > 0:
                                            irmao_x = y
                                            if x > y:
                                                f_value = x
                                                break
                                if f_value > 0:
                                    if DEBUG: print("Fixed element f found by Condition (i): ", f_value)
                                    break

                            if f_value == 0:

                                # Condition (ii)
                                for x in range(N+1, 2*N+1):
                                    sub_tree_raiz_x = []
                                    visited = [False] * (S+1)
                                    DFS_recurse(x, children_lists, visited, sub_tree_raiz_x)
                                    if len(sub_tree_raiz_x) == 1:
                                        continue
                                    #print("x = %d" % x)
                                    #print("sub_tree_raiz_x =", sub_tree_raiz_x)
                                    set_tree_solta = set()
                                    for y in range(x - N, N+1):
                                        if not visited[y]:
                                            set_tree_solta.add(y)
                                    #print("set_tree_solta =", set_tree_solta)
                                    if len(set_tree_solta) == 0:
                                        f_value = x
                                    else:
                                        for tree in forest[1:]:
                                            set_tree = set(tree)
                                    #print("set_tree =", set_tree)
                                            if len(set_tree.symmetric_difference(set_tree_solta)) == 0:
                                                f_value = x
                                                break
                                    if f_value > 0:
                                        if DEBUG: print("Fixed element f found by Condition (ii): ", f_value)
                                        break

                            if f_value == 0:

                                # Condition (iii)
                                for x in range(N+1, 2*N+1):
                                    tudo_OK = False
                                    for tree in forest:
                                        ultimo = tree[-1]
                                        if ultimo >= N+1:
                                            if ultimo == x:
                                                tudo_OK = True
                                            else:
                                                tudo_OK = False
                                                break
                                    if tudo_OK:
                                        f_value = x
                                        if DEBUG: print("Fixed element f found by Condition (iii): ", f_value)
                                        break

                            if f_value == 0:
                                if DEBUG: print("Fixed element f was not found.")
                                

                        root_children = set()
                        for x in range(N+1, 2*N+2):
                            if tree_edges[x] == S:
                                root_children.add(x)        

                    if retrieved_key == 0:
                        
                        # Step 1
                        
                        conexo = True
                        for x in range(N+1, 2*N+2):
                            if x == f_value:
                                continue
                            if tree_edges[x] < 0: # aresta removida
                                conexo = False
                                break
                        if conexo:
                            for x in root_children:
                                if x == 2*N + 1:
                                    continue
                                retrieved_key += 2**(2*N - x)
                            if DEBUG: print("Retrieved key = %d (in Step 1)" % retrieved_key)


                    if retrieved_key == 0:
                        
                        isolated_vertices = set(range(N+1, 2*N+2))
                        isolated_vertices.remove(f_value)
                        for x in range(N+1, 2*N+2):
                            if tree_edges[x] > N:
                                if x in isolated_vertices:
                                    isolated_vertices.remove(x)
                                if tree_edges[x] in isolated_vertices:
                                    isolated_vertices.remove(tree_edges[x])

                        if len(isolated_vertices) == 0:

                        # Step 2
                            for x in root_children:
                                if x == 2*N + 1:
                                    continue
                                retrieved_key += 2**(2*N - x)
                            if DEBUG: print("Retrieved key = %d (in Step 2)" % retrieved_key)
                            
                        elif len(isolated_vertices) == 2:

                        # Step 3
                            for x in root_children:
                                if x == 2*N + 1:
                                    continue
                                retrieved_key += 2**(2*N - x)
                            for x in isolated_vertices:
                                retrieved_key += 2**(2*N - x)
                            if DEBUG: print("Retrieved key = %d (in Step 3)" % retrieved_key)

                        elif len(isolated_vertices) == 1:

                        # Step 4
                            isolated_vertex = isolated_vertices.pop()
                            if DEBUG: print("isolated_vertex =", isolated_vertex)
                            for x in root_children:
                                if x == 2*N + 1:
                                    continue
                                retrieved_key += 2**(2*N - x)
                            if DEBUG: print("root_children =", root_children)
                                    
                            subtree_root_f = []
                            visited = [False] * (S+1)
                            DFS_recurse(f_value, children_lists, visited, subtree_root_f)
                            if DEBUG: print("subtree_root_f =", subtree_root_f)
                            if len(subtree_root_f) == 2*N - f_value + 2:
                                y = subtree_root_f[-1]
                                if DEBUG: print("N =", N)
                                if DEBUG: print("y =", y)
                                if (len(root_children) < y) and (isolated_vertex < 2*N+1):
                                    retrieved_key += 2**(2*N - isolated_vertex)
                            else:
                                if isolated_vertex < 2*N+1:
                                    retrieved_key += 2**(2*N - isolated_vertex)
                            if DEBUG: print("Retrieved key = %d (in Step 4)" % retrieved_key)
                                

                else:
                    
                #############################
                ##                         ##
                ##  Brute force algorithm  ##
                ##                         ##
                #############################

                    del forest[0][0]

                    self_inverting_permutations = set()
                    reconstruct_self_inverting_permutations(forest, self_inverting_permutations)

                    if DEBUG: print("self inverting permutations =", self_inverting_permutations)

                    bitonic_permutations = set()
                    determine_all_bitonic_permutation_candidates(self_inverting_permutations,
                                                                 bitonic_permutations)

                    if DEBUG: print("bitonic permutations =", bitonic_permutations)

                    success = False
                    if len(bitonic_permutations) == 1:
                        bitonic_permutation = list(bitonic_permutations)[0]
                        if DEBUG: print("bitonic permutation =", bitonic_permutation)
                        Y = []
                        for i in range(1, len(bitonic_permutation)):
                            if bitonic_permutation[i] < bitonic_permutation[i-1]:
                                Y += [bitonic_permutation[i]]
                        binary = [0] * (2*N + 2)
                        for y in Y:
                            binary[y] = 1
                        binary = binary[N+1:2*N+1]
                        if DEBUG: print("binary =", binary)
                        retrieved_key = 0
                        for i in range(N):
                            retrieved_key += ((binary[i] + 1) % 2) * 2**(N-1-i)
                        if DEBUG: print("retrieved key =", retrieved_key)
                    else:
                        retrieved_key = -1




                if retrieved_key == key:
                    total_successes_count += 1
                    successes_count += 1
                    if DEBUG or PRINT_TESTS: print("Success.")
                else:
                    total_failures_count += 1
                    if DEBUG or PRINT_TESTS or PRINT_FAILURES:
                        print_test_data(key, instance)
                        print("Failure.")


                if DEBUG: print_blank_line()

                elapsed_time = time() - start_time
                total_time += elapsed_time

            if (PRINT_KEY_SUMMARY or DEBUG) and (len(instance[0]) + len(instance[1]) > 0):
                print_key_summary(key, tests_count, successes_count)
                print_blank_line()
                        
        print_results_summary(total_tests_count, total_successes_count)

        print("\nTotal decoding time = %.5f seconds" % total_time)
        print("Average time per instance = %.5f microseconds" % (10**6 * total_time / total_tests_count))
        print("\n")

        print_blank_line("=")

        if predetermined_keys:
            break
        

def compute_distance(key1, key2):

    distance = 0
    
    for i in range(1, len(key1)):
        if key1[i] != key2[i]:
            distance += 1

    return distance



def count_k_synonyms():

    try:
        initial_n = eval(input("Initial key size: "))
        final_n = eval(input("Final key size: "))
        k = eval(input("Intended distance: "))
    except:
        initial_n = -1

    if initial_n > 0:
        print_synonyms = input("Print synonym watermarks (Y/N)? ")

        print("")
        
        for n in range(initial_n, final_n + 1):

            first_key = 2**(n - 1)
            last_key = 2**n - 1
            key_count = first_key
            
            watermarks = {}

            for key in range(first_key, last_key + 1):

                bitonic, tree_edges, tree = generate_watermark(key)
                watermarks[key] = tuple(tree_edges)

            synonyms = {}
            total_subsets = 0
            irrecoverable_subsets = 0
            subsets_per_instance = choose(2*n+1, k) # subsets of k tree edges
            for key1 in range(first_key, last_key):
                for key2 in range(key1 + 1, last_key + 1):
                    distance = compute_distance(watermarks[key1], watermarks[key2])
                    if distance <= k:
                        if key1 not in synonyms:
                            synonyms[key1] = set()
                        if key2 not in synonyms:
                            synonyms[key2] = set()
                        total_subsets += subsets_per_instance
                        free_subsets = 1
                        if k > distance:
                            free_subsets *= choose(2*N + 1 - distance, k - distance)    
                        irrecoverable_subsets += 2 * free_subsets
                        synonyms[key1].add(key2)
                        synonyms[key2].add(key1)
                        if print_synonyms in 'Yy':
                            print("\nkey = %d, watermark =" % key1, watermarks[key1][-1:0:-1],
                                  "\nkey = %d, watermark =" % key2, watermarks[key2][-1:0:-1])

            synonym_count = len(synonyms)

            print("\nThere are %d (out of %d) %d-synonym keys of size %d (%.2f%%)." \
                  % (synonym_count, key_count, k, n, synonym_count*100/key_count))
            print("The removal of %d subsets (out of %d) of %d tree edges leads to irrecoverable watermarks." \
                  % (irrecoverable_subsets, total_subsets, k))
            print("The probability that an attack to", k, "tree edges (chosen uniformly at random)")
            print("  leads to an irrecoverable watermark for keys of size %d is %.5f%%." \
                  % (n, 100 * irrecoverable_subsets / total_subsets))
            



##########
#        #
#  Main  #
#        #
##########

##keys = []
##range_min = 2**20
##range_max = 2**21
##for i in range(10000):
##    keys += [randint(range_min, range_max)]

#test_codec()
count_k_synonyms()


print("Bye.\n")
