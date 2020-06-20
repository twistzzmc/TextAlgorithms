import heapq as hq
from bitarray import bitarray


class StaticNode:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __repr__(self):
        return "char: " + str(self.char) + " | freq: " + str(self.freq)

    def __lt__(self, other):
        return self.freq < other.freq


class StaticHuffmanTree:
    def __init__(self, text=None):
        self.root = self._huffman_heap(self._get_frequency(text))
        self.compressed_text = self._encode(text)

    def __str__(self, node=None, level=0, direction=None):
        huffman_tree = ""
        if node is None:
            node = self.root

        if level > 0:
            for i in range(level):
                huffman_tree += "\t"
        huffman_tree += str(level) + " --- " + str(node)

        if direction is not None:
            huffman_tree += " -- " + direction

        print(huffman_tree)
        if node.left is not None:
            self.__str__(node.left, level + 1, "left")
        if node.right is not None:
            self.__str__(node.right, level + 1, "right")

        return ""

    @staticmethod
    def _get_frequency(text):
        letter_count = dict()

        for letter in text:
            if letter not in letter_count:
                letter_count[letter] = 1
            else:
                letter_count[letter] = letter_count[letter] + 1

        return letter_count

    def _get_code(self):
        letter_code = dict()

        def utility_get_code(node, direction, code):
            if direction == "left":
                code += "0"
            elif direction == "right":
                code += "1"

            if node.char is not None:
                letter_code[node.char] = code
            else:
                utility_get_code(node.left, "left", code)
                utility_get_code(node.right, "right", code)

        utility_get_code(self.root, "", "")
        return letter_code

    def _encode(self, text):
        letter_code = self._get_code()
        encoding = bitarray()

        for letter in text:
            encoding += bitarray(letter_code[letter])

        return encoding

    def decode(self):
        text = ""
        node = self.root
        for bit in self.compressed_text.to01():
            if node.char is not None:
                text += node.char
                node = self.root

            if bit == '0':
                node = node.left
            else:
                node = node.right

        return text

    @staticmethod
    def _huffman(letter_counts):
        nodes = []
        for a, weight in letter_counts.items():
            nodes.append(StaticNode(weight, a))
        internal_nodes = []
        leafs = sorted(nodes, key=lambda n: n.freq)

        while len(leafs) + len(internal_nodes) > 1:
            head = []

            if len(leafs) >= 2:
                head += leafs[:2]
            elif len(leafs) == 1:
                head += leafs[:1]

            if len(internal_nodes) >= 2:
                head += internal_nodes[:2]
            elif len(internal_nodes) == 1:
                head += internal_nodes[:1]

            el_1, el_2 = sorted(head, key=lambda n: n.freq)[:2]
            internal_nodes.append(StaticNode(el_1.freq + el_2.freq, left=el_1, right=el_2))

            if len(leafs) > 0 and el_1 == leafs[0]:
                leafs = leafs[1:]
            else:
                internal_nodes = internal_nodes[1:]

            if len(leafs) > 0 and el_2 == leafs[0]:
                leafs = leafs[1:]
            else:
                internal_nodes = internal_nodes[1:]

        return internal_nodes[0]

    @staticmethod
    def _huffman_heap(letter_counts):
        nodes = []
        for a, freq in letter_counts.items():
            hq.heappush(nodes, StaticNode(freq, a))

        while len(nodes) > 1:
            el1 = hq.heappop(nodes)
            el2 = hq.heappop(nodes)

            hq.heappush(nodes, StaticNode(el1.freq + el2.freq, left=el1, right=el2))

        return nodes[0]
