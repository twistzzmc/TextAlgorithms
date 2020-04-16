class SNode:
    def __init__(self, index=-1, parent_node=None, depth=-1):
        # Properties
        self.index = index
        self.depth = depth
        self.parent = parent_node
        # Links
        self.transition_links = []  # children
        self.suffix_link = None

    def __str__(self):
        return "SNode --- index: " + str(self.index) + ", depth: " + str(self.depth)

    def check_transition(self, suffix):
        for node, _suffix in self.transition_links:
            if _suffix == suffix:
                return True
        return False

    def get_transition(self, suffix):
        for node, _suffix in self.transition_links:
            if _suffix == suffix:
                return node
        return False

    def add_transition(self, snode, suffix=""):
        tran_link = self.get_transition(suffix)
        if tran_link:
            self.transition_links.remove((tran_link, suffix))
        self.transition_links.append((snode, suffix))


class SuffixTree:
    def __init__(self, text="", build_option=0):
        self.text = text + str(chr(57344))
        self.root = SNode()
        self.root.depth = 0
        self.root.index = 0
        self.root.parent = self.root
        self.root.suffix_link = self.root

        if not text == "":
            if build_option == 0:
                self._build_McCreight(text)
            elif build_option == 1:
                self._build_raw(text)

    def __str__(self, node=None, level=0):
        suffix_tree = ""
        if node is None:
            suffix_tree = "Root --- idx: " + str(self.root.index) + " depth: " + str(self.root.depth) + \
                " | " + self.text[self.root.index:self.root.depth + self.root.index]
            node = self.root
        else:
            if level > 0:
                for i in range(level):
                    suffix_tree += "\t"
            suffix_tree += str(level) + " in --- idx: " + str(node.index) + " depth: " + str(node.depth) + \
                " | " + self.text[node.index:node.index + node.depth]

        print(suffix_tree)
        for transition_link in node.transition_links:
            self.__str__(transition_link[0], level + 1)

        return ""

    def _build_McCreight(self, text):
        """
        McCreight algorithm using links
        :param text: string
        :return :
        """
        text += str(chr(57344))
        u = self.root
        d = 0
        for i in range(len(text)):
            while d == u.depth and u.check_transition(text[i + d]):
                u = u.get_transition(text[i + d])
                d = d + 1
                while d < u.depth and text[u.index + d] == text[i + d]:
                    d = d + 1
            if d < u.depth:
                u = self._create_node(text, u, d)
            self._create_leaf(text, i, u, d)
            if u.suffix_link is None:
                self._compute_slink(text, u)
            u = u.suffix_link
            d = d - 1
            if d < 0:
                d = 0

    @staticmethod
    def _create_node(text, u, d):
        index = u.index
        parent = u.parent
        v = SNode(index=index, depth=d)
        v.add_transition(u, text[index + d])
        u.parent = v
        parent.add_transition(v, text[index + parent.depth])
        v.parent = parent
        return v

    @staticmethod
    def _create_leaf(text, i, u, d):
        w = SNode()
        w.index = i
        w.depth = len(text) - i
        u.add_transition(w, text[i + d])
        w.parent = u
        return w

    def _compute_slink(self, text, u):
        d = u.depth
        v = u.parent.suffix_link
        while v.depth < d - 1:
            v = v.get_transition(text[u.index + v.depth + 1])
        if v.depth > d - 1:
            v = self._create_node(text, v, d - 1)
        u.suffix_link = v

    def _build_raw(self, text):
        """
        Building algorithm without using links (every time starts looking from root)
        :param text: string
        :return:
        """
        text += str(chr(57344))

        for i in range(len(text)):
            locus, is_leaf, new_index = self._find_locus(text, i)
            if not is_leaf:
                locus, index = self._add_node_raw(text, locus, new_index)
            else:
                index = i
            self._add_leaf_raw(text, locus, index)

    def _find_locus(self, text, i):
        locus = self.root
        level = 0
        while True:
            if not locus.check_transition(text[i]):
                return locus, True, i

            potential_locus = locus.get_transition(text[i])
            if potential_locus.depth > len(text) - i:
                return potential_locus, False, i

            i = i + potential_locus.depth
            locus = potential_locus

    @staticmethod
    def _add_leaf_raw(text, u, i):
        w = SNode()
        w.index = i
        w.depth = len(text) - i
        u.add_transition(w, text[i])
        w.parent = u

    @staticmethod
    def _add_node_raw(text, u, i):
        v_index = u.index
        v_depth = 0
        for j in range(len(text) - i):
            if text[j + v_index] == text[i + j]:
                v_depth = v_depth + 1
            else:
                break
        new_u_index = v_index + v_depth
        new_u_depth = u.depth - v_depth
        v = SNode(index=v_index, depth=v_depth)
        u.index = new_u_index
        u.depth = new_u_depth

        parent = u.parent
        parent.add_transition(v, text[v_index])
        v.add_transition(u, text[u.index])
        v.parent = parent
        u.parent = v

        return v, u.index + i - v_index
