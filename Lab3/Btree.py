import random


class Node:
    def __init__(self):
        self.keys = []
        self.child = []

    @property
    def leaf(self):
        return not self.child


class BTree:
    def __init__(self, t):
        self.t = t
        self.min_keys = t - 1
        self.max_keys = 2 * t - 1
        self.root = Node()
        self.comps = 0

    def insert(self, key):
        if len(self.root.keys) != self.max_keys:
            self.insert_in_node(self.root, key)
        else:
            new_root = Node()
            new_root.child.append(self.root)
            self.split_child(new_root, 0)
            self.root = new_root
            self.insert(key)

    def insert_in_node(self, node, key):
        i = len(node.keys) - 1
        while i >= 0 and node.keys[i][0] >= key[0]:
            i -= 1
        if node.leaf:
            node.keys.insert(i + 1, key)
        else:
            if len(node.child[i + 1].keys) == self.max_keys:
                self.split_child(node, i + 1)
                if node.keys[i + 1][0] < key[0]:
                    i += 1
            self.insert_in_node(node.child[i + 1], key)

    def split_child(self, parent, i):
        new_child = Node()
        half_max = self.max_keys // 2
        child = parent.child[i]
        middle = child.keys[half_max]
        new_child.keys = child.keys[half_max + 1:]
        child.keys = child.keys[:half_max]
        if not child.leaf:
            new_child.child = child.child[half_max + 1:]
            child.child = child.child[:half_max + 1]
        parent.keys.insert(i, middle)
        parent.child.insert(i + 1, new_child)

    def search(self, key):
        res = self.search_in_node(key, self.root)
        return res[-1][1:] if res else res

    def search_in_node(self, key, node, parent=None):
        keys = list(node.keys)
        n = len(keys)
        if not n % 2:
            keys.append((float('inf'), 0))
            n += 1
        rounded_middle = n // 2 + int(n % 2)
        middle = n // 2
        while middle:
            self.comps += 1
            if keys[rounded_middle - 1][0] == key:
                return node, parent, rounded_middle - 1, node.keys[rounded_middle - 1]
            elif keys[rounded_middle - 1][0] < key:
                rounded_middle = rounded_middle + middle // 2 + int(middle % 2)
            else:
                rounded_middle = rounded_middle - middle // 2 - int(middle % 2)
            middle = middle // 2
        if keys[rounded_middle - 1][0] == key:
            self.comps += 1
            return node, parent, rounded_middle - 1, node.keys[rounded_middle - 1]
        if node.leaf:
            return None
        else:
            if keys[rounded_middle - 1][0] > key:
                self.comps += 1
                return self.search_in_node(key, node.child[rounded_middle - 1], node)
            else:
                return self.search_in_node(key, node.child[rounded_middle], node)

    def edit(self, key):
        r = self.search_in_node(key[0], self.root)
        if r:
            node, _, i, _ = r
            node.keys[i] = key
            return True
        else:
            return None

    def delete(self, k):
        r = self.search_in_node(k, self.root)
        if r:
            node, parent, _, _ = r
        else:
            return False

        i = self.delete_in_node(node, k)

        if node.leaf:
            if len(node.keys) < self.min_keys:
                i = parent.child.index(node)
                if i != 0 and len(parent.child[i - 1].keys) > self.min_keys:
                    node.keys.insert(0, parent.keys.pop(i - 1))
                    parent.keys.insert(i - 1, parent.child[i - 1].keys.pop())
                else:
                    if i != len(parent.child) - 1 and len(parent.child[i + 1].keys) > self.min_keys:
                        node.keys.append(parent.keys.pop(i))
                        parent.keys.insert(i, parent.child[i + 1].keys.pop(0))
                    elif i == len(parent.child) - 1:
                        node.keys = parent.child[i - 1].keys + [parent.keys.pop(i - 1)] + node.keys
                        parent.child.pop(i - 1)
                    else:
                        node.keys = node.keys + [parent.keys.pop(i)] + parent.child[i + 1].keys
                        parent.child.pop(i + 1)
        else:
            sibling = node.child[i]
            while not sibling.leaf:
                sibling = sibling.child[-1]
            if len(sibling.keys) > self.min_keys:
                node.keys.insert(i, sibling.keys.pop())
            else:
                parent = node
                sibling = node.child[i + 1]
                while not sibling.leaf:
                    parent = sibling
                    sibling = parent.child[0]

                if len(sibling.keys) > self.min_keys:
                    node.keys.insert(i, sibling.keys.pop(0))
                else:
                    if parent == node:
                        node.child[i].keys += node.child[i + 1].keys
                        node.child[i].child += node.child[i + 1].child
                        node.child.pop(i + 1)
                    else:
                        node.keys.insert(i, sibling.keys.pop(0))
                        if len(parent.child[1].keys) > self.min_keys:
                            sibling.keys.append(parent.keys.pop(0))
                            parent.keys.insert(i, parent.child[1].keys.pop(0))
                        else:
                            sibling.keys = sibling.keys + [parent.keys.pop(0)] + parent.child[1].keys
                            parent.child.pop(1)
        return True

    @staticmethod
    def delete_in_node(node, k):
        for i, key in enumerate(node.keys):
            if key[0] == k:
                node.keys.pop(i)
                return i

    def __repr__(self):
        def show(x, l):
            r = "\t" * l + str([a[0] for a in x.keys])[1:-1] + "\n"
            for child in x.child:
                r += show(child, l + 1)
            return r

        return show(self.root, 0)

    def insert_random_values(self):
        values = list(range(10000))
        random.shuffle(values)
        for value in values:
            self.insert((value, float('inf')))

    def test(self):
        for i in range(1, 11):
            self.search(100 * i)
            print(f"Search number: {i}\nComparisons: {self.comps}")
            self.comps = 0


tree = BTree(10)
tree.insert_random_values()
tree.test()
