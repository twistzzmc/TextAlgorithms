from bitarray import bitarray


class AdaptiveNode:
    def __init__(self, char, weight=0, freq=0, left=None, right=None, parent=None):
        self.char = char
        self.weight = weight
        self.freq = freq
        self.left = left
        self.right = right
        self.parent = parent

    def __repr__(self):
        return "char: " + str(self.char) + " -- weight: " + str(self.weight) + " -- freq: " + str(self.freq)

    def __lt__(self, other):
        return self.freq < other.freq


class AdaptiveHuffmanTree:
    def __init__(self, text, number_of_characters=128, first_char_ord=0):
        self.number_of_characters = number_of_characters
        self.e = self._calculate_e_and_n()[0]
        self.r = int(self._calculate_e_and_n()[1])
        self.first_char_ord = first_char_ord - 1
        root, compressed_text = self.adaptive_huffman(text)
        self.root = root
        self.compressed_text = compressed_text

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

        return "Compressed text:   " + self.compressed_text.to01() + \
               "\nDecompressed text: " + self.decode()

    def _calculate_e_and_n(self):
        e = 0
        power_of_e = 1
        while True:
            if power_of_e > self.number_of_characters:
                return e - 1, self.number_of_characters - (power_of_e / 2)

            e += 1
            power_of_e *= 2

    def adaptive_huffman(self, text):
        init_weight = (2 * self.number_of_characters) - 1
        nodes = {"nyt": AdaptiveNode("nyt", init_weight, 0)}
        root = nodes["nyt"]
        bit_compression = bitarray('')

        for letter in list(text):
            if letter not in nodes:
                updated_node = nodes["nyt"]
                bit_compression += self._code(updated_node, True, letter)
                node = AdaptiveNode(letter, updated_node.weight - 1, 1, parent=updated_node)
                nodes[letter] = node
                del nodes["nyt"]
                zero_node = AdaptiveNode("nyt", node.weight - 1, 0, parent=updated_node)
                updated_node.left = zero_node
                updated_node.right = node
                nodes["nyt"] = zero_node
                self._update_parents(node.parent, 1)
            else:
                node = nodes[letter]
                bit_compression += self._code(node, False, letter)
                node.freq += 1
                self._update_parents(node.parent, 1)

        return root, bit_compression

    def _code(self, node, first_appearance, letter):
        if first_appearance:
            code = self._calculate_node_code(node)

            k = ord(letter) - self.first_char_ord
            if k < 2 * self.r:
                number_of_bits = self.e + 1
                number = k - 1
            else:
                number_of_bits = self.e
                number = k - self.r - 1

            bit_number = bitarray("{0:b}".format(number))
            while len(bit_number) < number_of_bits:
                bit_number = bitarray('0') + bit_number

            code += bit_number
            return code
        else:
            return self._calculate_node_code(node)

    @staticmethod
    def _calculate_node_code(node):
        code = bitarray('')
        while node.parent is not None:
            if node.parent.left == node:
                code += bitarray('0')
            else:
                code += bitarray('1')

            node = node.parent

        return code[::-1]

    @staticmethod
    def _update_parents(parent, freq):
        while parent is not None:
            parent.freq += freq

            if parent.left.freq > parent.right.freq:
                tmp = parent.left
                parent.left = parent.right
                parent.right = tmp

                tmp = parent.left.weight
                parent.left.weight = parent.right.weight
                parent.right.weight = tmp

            parent = parent.parent

    def decode(self):
        nodes = {"nyt": AdaptiveNode("nyt", freq=0)}
        root = nodes["nyt"]
        current_bit = 0
        text = ""

        while len(self.compressed_text) > current_bit:
            decoded_node, current_bit = self._decode_find_node(root, current_bit)

            if decoded_node.freq == 0:
                bit_number = self.compressed_text[current_bit:current_bit + self.e]

                if int(bit_number.to01(), 2) < self.r:
                    bit_number = self.compressed_text[current_bit: current_bit + self.e + 1]
                    letter = chr(int(bit_number.to01(), 2) + 1 + self.first_char_ord)
                    current_bit += self.e + 1
                else:
                    letter = chr(int(bit_number.to01(), 2) + 11 + self.first_char_ord)
                    current_bit += self.e
            else:
                letter = decoded_node.char

            text += letter

            if letter not in nodes:
                updated_node = nodes["nyt"]
                node = AdaptiveNode(letter, updated_node.weight - 1, 1, parent=updated_node)
                nodes[letter] = node
                del nodes["nyt"]
                zero_node = AdaptiveNode("nyt", node.weight - 1, 0, parent=updated_node)
                updated_node.left = zero_node
                updated_node.right = node
                nodes["nyt"] = zero_node
                self._update_parents(node.parent, 1)
            else:
                node = nodes[letter]
                node.freq += 1
                self._update_parents(node.parent, 1)

        return text

    def _decode_find_node(self, root, current_bit):
        if current_bit == 0:
            return root, 0
        else:
            node = root
            while node.left is not None and node.right is not None:
                node = node.left if int(self.compressed_text.to01()[current_bit]) == 0 else node.right
                current_bit += 1
            return node, current_bit
