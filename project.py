import csv

class Mushroom:
    def __init__(self, edible: bool):
        self.__edible = edible
    
    def is_edible(self):
        return self.__edible
    
    def add_attribute(self, name: str, value: str):
        return
    
    def get_attribute(self, name: str):
        return

class Node:
    def __init__(self, criterion: str, is_leaf: bool=False):
        self.edges_ = []
    
    def is_leaf(self):
        return
    
    def add_edge(self, label: str, child: 'Node'):
        return
    
def load_dataset(path: str):
    return