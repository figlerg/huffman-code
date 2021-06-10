from heapq import heapify, heappush, heappop


class Node(object):
    def __init__(self, id, p, children, l=0, is_leaf=False):
        self.children = children
        self.id = id
        self.p = p
        # self.l = l
        self.is_leaf = is_leaf

    # this defines the priority
    def __lt__(self, other):
        return self.p < other.p

    def __str__(self):
        return str(self.id)


def Huffman(P: list[float]):
    # P is assumed to be sorted
    nodes = []

    for i, p in enumerate(P):
        nodes.append(Node(i, p, children=[], l=0, is_leaf=True))

    heapify(nodes)

    while len(nodes) > 1:
        right_child = heappop(nodes)
        left_child = heappop(nodes)

        # sticks the two nodes with lowest prob together
        new_node = Node(id=None,
                        p=left_child.p + right_child.p,
                        children=[left_child, right_child], is_leaf=False)

        # pushes it to the right part of the priority queue
        # (this is cheap! Kein teures sortieren aus der angabe!)
        heappush(nodes, new_node)

    huffman_tree = nodes[0]

    lengths = visit(huffman_tree)

    return sorted(lengths, key=lambda x: x[1])


def visit(node):
    # is leaf, no children
    if node.is_leaf == True:
        return [['id=' + str(node.id), 0], ]
    # huffman never makes a node with one child

    # both children
    lengths = visit(node.children[0]) + visit(node.children[1])
    for i in range(len(lengths)):
        lengths[i][1] += 1
    return lengths


def canonical_huffman(lengths):
    codewords_dec = {}
    for i in range(len(lengths)):
        if i == 0:
            codewords_dec[i] = 0
        else:
            codewords_dec[i] = \
                (codewords_dec[i - 1] + 1) * 2 ** (lengths[i][1] - lengths[i - 1][1])

    codewords = {}

    for i, item in enumerate(codewords_dec.items()):
        codeword = bin(item[1])[2:]

        # add leading zeros
        codeword = (lengths[i][1] - len(codeword)) * '0' + codeword

        codewords[lengths[i][0]] = codeword

    return codewords


if __name__ == '__main__':
    ls = Huffman([0.4, 0.2,0.2,0.1,0.1])
    print(dict(ls))
    # answer: {'id=0': 1, 'id=1': 2, 'id=2': 3, 'id=3': 4, 'id=4': 5, 'id=5': 5}

    codewords = canonical_huffman(ls)
    print(codewords)
    # answer: { 'id=0': '0', 'id=1': '10', 'id=2': '110',
    #           'id=3': '1110', 'id=4': '11110', 'id=5': '11111'}
