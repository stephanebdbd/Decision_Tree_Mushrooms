import sys, csv
from math import log2

class Mushroom:
    def __init__(self, edible: bool):
        self.__edible = edible
        self.__attributes = {}
    
    def is_edible(self):
        return self.__edible
    
    def add_attribute(self, name: str, value: str):
        self.__attributes[name] = value
    
    def get_attribute(self, name: str):
        return self.__attributes[name]

    def get_attributes(self):
        return list(self.__attributes.keys())

class Node:
    def __init__(self, criterion: str, is_leaf: bool=False):
        self.edges_ = []
        self.criterion_ = criterion
        self.is_leaf_ = is_leaf
    
    def get_criterion(self):
        return self.criterion_

    def is_leaf(self):
        return self.is_leaf_
    
    def add_edge(self, label: str, child: "Node"):
        self.edges_.append(Edge(self, child, label))

class Edge:
    def __init__(self, parent: Node, child: Node, label: str):
        self.parent_: Node = parent
        self.child_: Node = child
        self.label_: str = label
    
    def get_label(self):
        return self.label_

    def get_child(self):
        return self.child_
    
    def get_parent(self):
        return self.parent_

class BooleanTree:
    def __init__(self, node: Node, tab: int=0):
        self.node, self.tab = node, tab
        self.edges_ = [edge for edge in node.edges_ if edge.get_child().criterion_ != "No"]
        self.amount_or, self.edge = 0, None
    
    def get_edge_child(self):
        edge = self.edge
        return edge.get_child()

class PythonScript:
    def __init__(self, file, node:Node, tab: int=1):
        self.leaves, self.node = [], node
        self.file, self.tab = file, tab
        self.edge, self.if_ = None, False
        self.edges_ = node.edges_
        
    def clear_leaves(self):
        self.leaves.clear()
    
    def edge_get_child(self):
        edge = self.edge
        return edge.get_child()
    
    def leaves_append(self):
        label = self.edge.get_label()
        self.leaves.append(label)
    
def load_dataset(path: str):
    mushrooms = []
    with open(path, "r", encoding='UTF-8') as file:
        data = list(csv.reader(file))
        attributes = data[0][1:]
        for row in data[1:]:
            mushroom = Mushroom(row[0] == "Yes")
            for attribute, value in zip(attributes, row[1:]):
                mushroom.add_attribute(attribute, value)
            mushrooms.append(mushroom)
    return mushrooms

def entropy(mushrooms: list[Mushroom]):
    pY = sum([mushroom.is_edible() for mushroom in mushrooms]) / len(mushrooms)
    if pY == 0 or pY == 1:
        return 0
    return log2(1 - pY)*(pY - 1) - log2(pY)*pY

def get_sub_attributes(mushrooms: list[Mushroom], attribute: str):
    sub_attributes = set()
    for mushroom in mushrooms:
        sub_attributes.add(mushroom.get_attribute(attribute))
    return sub_attributes

def Ca_v(mushrooms : list[Mushroom], attribute : str):
    sub_attributes = get_sub_attributes(mushrooms, attribute)
    res = {sub_attribute: [] for sub_attribute in sub_attributes}
    for mushroom in mushrooms:
        res[mushroom.get_attribute(attribute)].append(mushroom)
    return res

def get_information_gain(mushrooms: list[Mushroom], attribute : str):
    h, h1, ca_v = entropy(mushrooms), 0, Ca_v(mushrooms, attribute)
    for c in ca_v.values():
        pa_v = len(c) / len(mushrooms)
        h2 = entropy(c)
        h1 += pa_v * h2
    return h - h1

def get_best_attribute(mushrooms: list[Mushroom]):
    attributes = mushrooms[0].get_attributes()
    best_attribute = attributes[0]
    best_information_gain = get_information_gain(mushrooms, best_attribute)
    for attribute in attributes[1:]:
        information_gain = get_information_gain(mushrooms, attribute)
        if information_gain > best_information_gain:
            best_attribute = attribute
            best_information_gain = information_gain
    return best_attribute

def build_decision_tree(mushrooms: list[Mushroom]):
    best_attribute = get_best_attribute(mushrooms)
    r = Node(best_attribute)
    ca_v = Ca_v(mushrooms, best_attribute)
    for sub_attribute, c in ca_v.items():
        if entropy(c) == 0:
            criterion = "Yes" if c[0].is_edible() else "No"
            r.add_edge(sub_attribute, Node(criterion, True))
        else:
            r.add_edge(sub_attribute, build_decision_tree(c))
    return r

def display(tree: Node):
    def display_r(node: Node, tab: int=0):
        for edge in node.edges_:
            print("    "*tab + f"{node.criterion_} = {edge.get_label()}")
            child = edge.get_child()
            if not child.is_leaf():
                display_r(child, tab+1)
            else:
                print("    "*(tab+1) + child.criterion_)
    display_r(tree)

def is_edible(root: Node, mushroom: Mushroom):
    while not root.is_leaf():
        n, i = len(root.edges_), 0
        finished = False
        while i < n and not finished:
            edge = root.edges_[i]
            if mushroom.get_attribute(root.criterion_) == edge.get_label():
                root = edge.get_child()
                finished = True
            i += 1
    return root.criterion_ == "Yes"

def print_not_leaf(bt: BooleanTree):
    node, edges, tab = bt.node, bt.edges_, bt.tab
    amount_or, child, edge = bt.amount_or, bt.get_edge_child(), bt.edge
    par = len([i.get_child().criterion_ != "No" for i in child.edges_]) > 1
    print(f"({node.criterion_} = {edge.get_label()}", end="")
    print(" AND (" if par else " AND ")
    boolean_tree_r(BooleanTree(child, tab+1))
    print(")" if par else "", end="")
    print(") OR " if amount_or < len(edges) else ")", end="")
    print("\n" + "    "*tab, end="")

def print_leaf(bt: BooleanTree):
    node, edges, tab = bt.node, bt.edges_, bt.tab
    amount_or, edge = bt.amount_or, bt.edge
    print(f"({node.criterion_} = {edge.get_label()})", end="")
    print(" OR " if amount_or < len(edges) else "", end="")
    n = amount_or < len(edges)-1 and edges[amount_or].get_child().criterion_ == "Yes"
    print("\n" + "    "*tab if n and amount_or % 2 == 0 else "", end="")

def boolean_tree_r(bt: BooleanTree):
    print("    "*bt.tab, end="")
    for bt.amount_or, bt.edge in enumerate(bt.edges_):
        bt.amount_or += 1
        child = bt.get_edge_child()
        if not child.is_leaf():
            print_not_leaf(bt)
        elif child.criterion_ == "Yes":
            print_leaf(bt)

def boolean_tree(root: Node):
    print("(", end="")
    boolean_tree_r(BooleanTree(root))
    print(")")

def print_criterions(ps: PythonScript):
    tab, file, node, leaves, if_ = ps.tab, ps.file, ps.node, ps.leaves, ps.if_
    criterions = False
    if len(leaves) > 3:
        print("    "*tab + f"criterions = {leaves}", file=file)
        criterions = True
    print("    "*tab, end="", file=file)
    print("elif" if if_ and not criterions else "if", end="", file=file)
    ps.if_, if_ = True, True
    if len(leaves) == 1:
        print(f" mushroom.get_attribute('{node.criterion_}') == '{leaves[0]}':", file=file)
    elif len(leaves) > 0:
        print(f" mushroom.get_attribute('{node.criterion_}')", end="", file=file)
        print(" in criterions:" if criterions else f" in {leaves}:", file=file)
        ps.clear_leaves()
    print("    "*(tab+1) + "return True", file=file)

def print_if_leaves(ps: PythonScript):
    tab, file, node, edge, if_ = ps.tab, ps.file, ps.node, ps.edge, ps.if_
    print("    "*tab, end="", file=file)
    print("elif" if if_ else "if", end="", file=file)
    print(f" mushroom.get_attribute('{node.criterion_}') == '{edge.get_label()}':", file=file)

def to_python_r(ps: PythonScript):
    for edge in ps.edges_:
        ps.edge = edge
        child = ps.edge_get_child()
        if not child.is_leaf():
            print_if_leaves(ps)
            to_python_r(PythonScript(ps.file, child, ps.tab+1))
        elif child.criterion_ == 'Yes':
                ps.leaves_append()
    print_criterions(ps)

def to_python(dt: Node, path: str):
    with open(path, "w") as file:
        print("from project import *\n", file=file)
        print("def is_edible(mushroom: Mushroom):", file=file)
        to_python_r(PythonScript(file, dt))
        print("    else:\n" + "    "*(2) + "return False", end="", file=file)

def main(argv, argc):
    path1 = "mushrooms.csv" if argc < 2 else argv[1]
    path2 = "decision_tree.py" if argc < 3 else argv[2]
    mushrooms = load_dataset(path1)
    dt = build_decision_tree(mushrooms)
    display(dt)
    print()
    boolean_tree(dt)
    to_python(dt, path2)

if __name__ == "__main__":
    main(sys.argv, len(sys.argv))