import csv

class Mushroom:
    def __init__(self, edible: bool):
        self.__edible = edible
        self.__attributes = {'edible': 'Yes' if edible else 'No'}
    
    def is_edible(self):
        return self.__edible
    
    def add_attribute(self, name: str, value: str):
        self.__attributes[name] = value
    
    def get_attribute(self, name: str):
        return self.__attributes[name]

class Node:
    def __init__(self, criterion: str, is_leaf: bool=False):
        self.edges_ = []
    
    def is_leaf(self):
        return
    
    def add_edge(self, label: str, child: 'Node'):
        return

class Edge:
    def __init__(self, parent: 'Node', child: 'Node', label: str):
        self.parent_: 'Node' = parent
        self.child_: 'Node' = child
        self.label_: str = label
    
def load_dataset(path: str):
    mushrooms = []
    with open(path, 'r') as file:
        data = list(csv.reader(file))
        attributes = data[0]
        for row in data[1:]:
            mushroom = Mushroom(row[0] == 'Yes')
            for attribute, value in zip(attributes[1:], row[1:]):
                mushroom.add_attribute(attribute, value)
            mushrooms.append(mushroom)
    return mushrooms

load_dataset('mushrooms.csv')