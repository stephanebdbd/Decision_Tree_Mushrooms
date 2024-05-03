import csv
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
        self.__criterion = criterion
        self.__is_leaf = is_leaf
    
    def get_criterion(self):
        return self.__criterion

    @property
    def is_leaf(self):
        return self.__is_leaf
    
    def add_edge(self, label: str, child: 'Node'):
        self.edges_.append(Edge(self, child, label))

class Edge:
    def __init__(self, parent: 'Node', child: 'Node', label: str):
        self.parent_: 'Node' = parent
        self.child_: 'Node' = child
        self.label_: str = label
    
def load_dataset(path: str):
    mushrooms = []
    with open(path, 'r') as file:
        data = list(csv.reader(file))
        attributes = data[0][1:]
        for row in data[1:]:
            mushroom = Mushroom(row[0] == 'Yes')
            for attribute, value in zip(attributes, row[1:]):
                mushroom.add_attribute(attribute, value)
            mushrooms.append(mushroom)
    return mushrooms

def entropy(data: list):
    pY = sum([mushroom.is_edible() for mushroom in data]) / len(data)
    if pY == 0 or pY == 1:
        return 0
    return log2(1 - pY)*(pY - 1) - log2(pY)*pY

def Ca_v(mushrooms : list[Mushroom], attribute : str, value : str):
    res = []
    for mushroom in mushrooms:
        if mushroom.get_attribute(attribute) == value:
            res.append(mushroom)
    return res

def get_information_gain(mushrooms: list[Mushroom], attribute : str):
    h = entropy(mushrooms)
    subs_attributes = get_sub_attributes(mushrooms, attribute)
    h1 = 0
    for sub_attribute in subs_attributes:
        ca_v = Ca_v(mushrooms, attribute, sub_attribute)
        pa_v = len(ca_v) / len(mushrooms)
        h2 = entropy(ca_v)
        h1 += pa_v * h2
    return h - h1

def get_sub_attributes(mushrooms: list[Mushroom], attribute: str):
    sub_attributes = set()
    for mushroom in mushrooms:
        sub_attributes.add(mushroom.get_attribute(attribute))
    return sub_attributes

def get_best_attribute(mushrooms: list[Mushroom], attributes: list[str]):
    best_attribute = attributes[0]
    best_information_gain = get_information_gain(mushrooms, best_attribute)
    for attribute in attributes[1:]:
        information_gain = get_information_gain(mushrooms, attribute)
        if information_gain > best_information_gain:
            best_attribute = attribute
            best_information_gain = information_gain
    return best_attribute
    

def build_decision_tree(mushrooms: list[Mushroom]):
    attributes = mushrooms[0].get_attributes()
    return build_decision_tree_r(mushrooms, attributes)

def build_decision_tree_r(mushrooms: list[Mushroom], attributes: list[str], r: Node = None):
    pass
    

def display(tree: Node):
    pass

def is_edible(root: Node, mushroom: Mushroom):
    pass