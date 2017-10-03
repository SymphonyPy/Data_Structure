class Node:
    def __init__(self, freq):
        self.left = None
        self.right = None
        self.father = None
        self.freq = freq

    def isLeft(self):
        return self.father.left == self


def create_Nodes(freqs):
    return [Node(freq) for freq in freqs]


def create_Huffman_Tree(nodes):
    queue = nodes[:]
    while len(queue) > 1:
        queue.sort(key=lambda item: item.freq)
        node_left = queue.pop(0)
        node_right = queue.pop(0)
        node_father = Node(node_left.freq + node_right.freq)
        node_father.left = node_left
        node_father.right = node_right
        node_left.father = node_father
        node_right.father = node_father
        queue.append(node_father)
    queue[0].father = None
    return queue[0]


def huffman_Encoding(nodes, root):
    codes = [''] * len(nodes)
    for i in range(len(nodes)):
        node_tmp = nodes[i]
        while node_tmp != root:
            if node_tmp.isLeft():
                codes[i] = '0' + codes[i]
            else:
                codes[i] = '1' + codes[i]
            node_tmp = node_tmp.father
    return codes


def cal_count_freq(content):
    chars = []
    chars_freqs = []
    for i in range(0, len(content)):
        if content[i] in chars:
            pass
        else:
            chars.append(content[i])
            char_freq = (content[i], content.count(content[i]))
            chars_freqs.append(char_freq)
    return chars_freqs


def cal_Huffman_codes(chars_freqs):
    nodes = create_Nodes([item[1] for item in chars_freqs])
    root = create_Huffman_Tree(nodes)
    Huffman_codes = huffman_Encoding(nodes, root)
    return Huffman_codes