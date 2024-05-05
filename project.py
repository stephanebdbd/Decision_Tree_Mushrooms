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
    def __init__(self, parent: "Node", child: "Node", label: str):
        self.parent_: "Node" = parent
        self.child_: "Node" = child
        self.label_: str = label
    
    def get_label(self):
        return self.label_

    def get_child(self):
        return self.child_
    
    def get_parent(self):
        return self.parent_
    
def load_dataset(path: str):
    mushrooms, data = [], []
    with open(path, "r", encoding='UTF8') as file:
        for line in file:
            data.append(line.strip().split(','))
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
    h, h1 = entropy(mushrooms), 0
    ca_v = Ca_v(mushrooms, attribute)
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

def print_not_leaf(node: Node, child: Node, edge: Edge, edges: list[Edge], tab: int, amount_or: int):
    par = len([i.get_child().criterion_ != "No" for i in child.edges_]) > 1
    print(f"({node.criterion_} = {edge.get_label()}", " AND (" if par else " AND ", sep="")
    boolean_tree_r(child, tab+1)
    print(")" if par else "", ") OR " if amount_or < len(edges) else ")", end="", sep="")
    print("\n" + "    "*tab, end="")

def print_leaf(node: Node, child: Node, edge: Edge, edges: list[Edge], tab: int, amount_or: int):
    print(f"({node.criterion_} = {edge.get_label()})", end="")
    print(" OR " if amount_or < len(edges) else "", end="")
    n = amount_or < len(edges) and edges[amount_or].get_child().criterion_ == "Yes"
    print("\n" + "    "*tab if n and amount_or % 2 == 0 else "", end="")

def boolean_tree_r(node: Node, tab: int=0):
    print("    "*tab, end="")
    edges = [edge for edge in node.edges_ if edge.get_child().criterion_ != "No"]
    for amount_or, edge in enumerate(edges):
        amount_or += 1
        child = edge.get_child()
        if not child.is_leaf():
            print_not_leaf(node, child, edge, edges, tab, amount_or)
        elif child.criterion_ == "Yes":
            print_leaf(node, child, edge, edges, tab, amount_or)

def boolean_tree(root: Node):
    print("(", end="")
    boolean_tree_r(root)
    print(")")

def print_criterions(leaves: list[str], file, node: Node, edge: Edge, if_: bool, tab: int):
    criterions = False
    if len(leaves) > 0:
        if len(leaves) > 3:
            print("    "*tab + f"criterions = {leaves}", file=file)
            criterions = True
        print("    "*tab, end="", file=file)
        print("elif" if if_ and not criterions else "if", end="", file=file)
        if_ = True
        if len(leaves) == 1:
            print(f" mushroom.get_attribute('{node.criterion_}') == '{leaves[0]}':", file=file)
        else:
            print(f" mushroom.get_attribute('{node.criterion_}')", end="", file=file)
            print(" in criterions:" if criterions else f" in {leaves}:", file=file)
            leaves.clear()
        print("    "*(tab+1) + "return True", file=file)

def print_if_leaves(leaves: list[str], file, node: Node, child: Node, edge: Edge, if_: bool, tab: int):
    print("    "*tab, end="", file=file)
    print("elif" if if_ else "if", end="", file=file)
    print(f" mushroom.get_attribute('{node.criterion_}') == '{edge.get_label()}':", file=file)

def to_python_r(node: Node, file, tab: int=1):
    leaves, if_ = [], False
    for edge in node.edges_:
        child = edge.get_child()
        if not child.is_leaf():
            print_if_leaves(leaves, file, node, child, edge, if_, tab)
            if_ = True
            to_python_r(child, file, tab+1)
        else:
            if child.criterion_ == 'Yes':
                leaves.append(edge.get_label())
    print_criterions(leaves, file, node, edge, if_, tab)

def to_python(dt: Node, path: str):
    with open(path, "w") as file:
        print("from project import *\n", file=file)
        print("def is_edible(mushroom: Mushroom):", file=file)
        to_python_r(dt, file)
        print("    else:\n" + "    "*(2) + "return False", end="", file=file)