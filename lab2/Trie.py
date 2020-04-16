class TrieNode:
    limit_children = 5

    def __init__(self, letter):
        self.children = [None]*self.limit_children
        self.is_end_of_word = False
        self.letter = letter

    def __repr__(self):
        if_word = "Word " if self.is_end_of_word else "Not a word; "
        children = ""
        for child in range(self.limit_children):
            if self.children[child] is not None:
                children += str(chr(97 + child)) + " "

        return if_word + "Letter: " + self.letter + "; " + "Children: " + children


class Trie:
    def __init__(self, text=""):
        self.root = self.get_node("root")

        if not text == "":
            text += "d"
            self.insert_suffixes(text)

    @staticmethod
    def get_node(letter):
        return TrieNode(letter)

    @staticmethod
    def _char_to_index(ch):
        return ord(ch) - ord('a')  # to use for only small letters
        # return ord(ch)  # to use for unknown characters

    def insert(self, key):
        p_crawl = self.root
        length = len(key)

        for level in range(length):
            index = self._char_to_index(key[level])

            if not p_crawl.children[index]:
                p_crawl.children[index] = self.get_node(key[level])
            p_crawl = p_crawl.children[index]

        p_crawl.is_end_of_word = True

    def search(self, key):
        p_crawl = self.root
        length = len(key)

        for level in range(length):
            index = self._char_to_index(key[level])

            if not p_crawl.children[index]:
                return False
            p_crawl = p_crawl.children[index]

        return p_crawl is not None and p_crawl.is_end_of_word

    def lazy_insert_suffixes(self, text):
        for i in range(len(text)):
            self.insert(text[i:])

    def _head(self, suffix):
        p_crawl = self.root
        length = len(suffix)

        for level in range(length):
            index = self._char_to_index(suffix[level])

            if not p_crawl.children[index]:
                return p_crawl, level
            p_crawl = p_crawl.children[index]

        return p_crawl, 0

    def insert_suffixes(self, text):
        self.insert(text)

        for level in range(1, len(text)):
            head, head_level = self._head(text[level:])

            # print("The suffix I put in: " + text[level:])
            # print("The suffix I actively put in: " + text[level + head_level:])
            # print("Head: " + str(head))
            # print("Suffix level:", level)
            # print("Found head level:", head_level)

            self.graft(head, text[head_level + level:])

    def graft(self, head, text):
        p_crawl = head
        length = len(text)

        for level in range(length):
            index = self._char_to_index(text[level])

            if not p_crawl.children[index]:
                p_crawl.children[index] = self.get_node(text[level])
            p_crawl = p_crawl.children[index]

        p_crawl.is_end_of_word = True

    @staticmethod
    def display(root, string, level):
        if root.is_end_of_word:
            string = string[:level] + '\0' + string[level + 1:]
            print(string)

        for i in range(root.limit_children):
            if root.children[i]:
                string = string[:level] + str(chr(97 + i)) + string[level + 1:]
                Trie.display(root.children[i], string, level + 1)
