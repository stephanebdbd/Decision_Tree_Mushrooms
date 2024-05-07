import sys, csv
from math import log2

class Mushroom:
    # Classe qui représente un champignon
    def __init__(self, edible: bool):
        self.__edible = edible
        self.__attributes = {}
    
    def is_edible(self):
    # Méthode qui retourne un booléen sur la comestibilité d'un champignon
        return self.__edible
    
    def add_attribute(self, name: str, value: str):
    # Méthode qui ajoute un attribut à un champignon en le reliant à sa valeur
        self.__attributes[name] = value
    
    def get_attribute(self, name: str):
    # Méthode qui retourne la valeur d'un attribut d'un champignon
        return self.__attributes[name]

    def get_attributes(self):
    # Méthode qui retourne une liste des attributs d'un champignon
        return list(self.__attributes.keys())

class Node:
# Classe qui représente un noeud d'un arbre de décision
    def __init__(self, criterion: str, is_leaf: bool=False):
        self.edges_ = []
        self.criterion_ = criterion
        self.is_leaf_ = is_leaf
    
    def get_criterion(self):
    # Méthode qui retourne le critère du noeud
        return self.criterion_

    def is_leaf(self):
    # Méthode qui retourne un booléen sur la nature du noeud
        return self.is_leaf_
    
    def add_edge(self, label: str, child: "Node"):
    # Méthode qui ajoute une arête à un noeud
        self.edges_.append(Edge(self, child, label))

class Edge:
# Classe qui représente une arête d'un arbre de décision
    def __init__(self, parent: Node, child: Node, label: str):
        self.parent_: Node = parent
        self.child_: Node = child
        self.label_: str = label
    
    def get_label(self):
    # Méthode qui retourne le label de l'arête
        return self.label_

    def get_child(self):
    # Méthode qui retourne le noeud enfant de l'arête
        return self.child_
    
    def get_parent(self):
    # Méthode qui retourne le noeud parent de l'arête
        return self.parent_

class BooleanTree:
# Classe qui stocke les données nécessaires pour créer un arbre booléen
    def __init__(self, node: Node, tab: int=0):
        self.node, self.tab = node, tab
        self.edges_ = [edge for edge in node.edges_ if edge.get_child().criterion_ != "No"]
        self.amount_or, self.edge = 0, None
    
    def get_edge_child(self):
    # Méthode qui retourne le noeud enfant de l'arête stocké
        edge = self.edge
        return edge.get_child()

class PythonScript:
    # Classe qui stocke les données nécessaires pour créer un script python
    def __init__(self, node:Node, tab: int=1):
        self.leaves, self.node = [], node
        self.tab = tab
        self.edge, self.if_ = None, False
        self.edges_ = node.edges_
        
    def clear_leaves(self):
    # Méthode qui vide la liste des feuilles
        self.leaves.clear()
    
    def edge_get_child(self):
    # Méthode qui retourne le noeud enfant de l'arête stocké
        edge = self.edge
        return edge.get_child()
    
    def leaves_append(self):
    # Méthode qui ajoute une feuille à la liste des feuilles
        label = self.edge.get_label()
        self.leaves.append(label)
    
def load_dataset(path: str):
# Fonction qui charge un dataset de champignons
    mushrooms = [] # Liste qui stocke les champignons
    with open(path, "r", encoding='UTF-8') as file: # Ouverture du fichier
        data = list(csv.reader(file))
        attributes = data[0][1:] # Liste des attributs
        for row in data[1:]: # Parcours des lignes du fichier
            mushroom = Mushroom(row[0] == "Yes") # Création d'un champignon
            for attribute, value in zip(attributes, row[1:]):
                mushroom.add_attribute(attribute, value) # Ajout des attributs
            mushrooms.append(mushroom)
    return mushrooms

def entropy(mushrooms: list[Mushroom]):
# Fonction qui calcule l'entropie d'un ensemble de champignons
    pY = sum([mushroom.is_edible() for mushroom in mushrooms]) / len(mushrooms)
    if pY == 0 or pY == 1: # Si la proportion de champignons comestibles est nulle ou égale à 1
        return 0 # L'entropie est nulle
    return log2(1 - pY)*(pY - 1) - log2(pY)*pY # Calcul de l'entropie

def get_sub_attributes(mushrooms: list[Mushroom], attribute: str):
# Fonction qui retourne les sous-attributs d'un attribut
    sub_attributes = set() # Ensemble qui stocke les sous-attributs
    for mushroom in mushrooms: # Parcours des champignons
        sub_attributes.add(mushroom.get_attribute(attribute)) # Ajout de l'attribut
    return sub_attributes

def Ca_v(mushrooms : list[Mushroom], attribute : str):
    # Fonction qui retourne les sous ensembles de champignons pour un attribut par rapport à ses valeurs
    sub_attributes = get_sub_attributes(mushrooms, attribute) # Récupération des sous attributs
    res = {sub_attribute: [] for sub_attribute in sub_attributes} # Dictionnaire qui stocke les sous ensembles
    for mushroom in mushrooms:
        res[mushroom.get_attribute(attribute)].append(mushroom) # Ajout du champignon dans le sous ensemble
    return res

def get_information_gain(mushrooms: list[Mushroom], attribute : str):
    # Fonction qui retourne le gain d'information d'un attribut
    h, h1, ca_v = entropy(mushrooms), 0, Ca_v(mushrooms, attribute)
    for c in ca_v.values(): # Parcours des sous ensembles
        pa_v = len(c) / len(mushrooms)
        h2 = entropy(c) # Calcul de l'entropie
        h1 += pa_v * h2 # Calcul pour chaque sous ensemble
    return h - h1 # Calcul du gain d'information

def get_best_attribute(mushrooms: list[Mushroom]):
    # Fonction qui retourne le meilleur attribut pour construire l'arbre de décision
    attributes = mushrooms[0].get_attributes()
    best_attribute = attributes[0]
    best_information_gain = get_information_gain(mushrooms, best_attribute)
    for attribute in attributes[1:]: # Parcours des attributs
        information_gain = get_information_gain(mushrooms, attribute) # Calcul du gain d'information
        if information_gain > best_information_gain: # Si le gain d'information est supérieur
            best_attribute = attribute # Mise à jour de l'attribut
            best_information_gain = information_gain # Mise à jour du gain d'information
    return best_attribute

def build_decision_tree(mushrooms: list[Mushroom]):
    # Fonction qui construit un arbre de décision
    best_attribute = get_best_attribute(mushrooms) # Récupération du meilleur attribut
    r = Node(best_attribute) # Création du noeud ayant comme racine le meilleur attribut
    ca_v = Ca_v(mushrooms, best_attribute) # Récupération des sous ensembles
    for sub_attribute, c in ca_v.items(): # Parcours des sous ensembles
        if entropy(c) == 0: # Si l'entropie est nulle
            criterion = "Yes" if c[0].is_edible() else "No"
            r.add_edge(sub_attribute, Node(criterion, True)) # Création d'une feuille
        else:
            r.add_edge(sub_attribute, build_decision_tree(c)) # Création d'un noeud via récursivité
    return r

def is_edible(root: Node, mushroom: Mushroom):
    # Fonction qui retourne un booléen sur la comestibilité d'un champignon
    while not root.is_leaf(): # Tant que le noeud n'est pas une feuille
        n, i = len(root.edges_), 0
        finished = False
        while i < n and not finished: # Parcours des arêtes
            edge = root.edges_[i]
            if mushroom.get_attribute(root.criterion_) == edge.get_label(): # Si l'attribut est égal au label
                root = edge.get_child() # Mise à jour du noeud
                finished = True
            i += 1
    return root.criterion_ == "Yes" # Retourne un booléen sur la comestibilité

def display(tree: Node):
    # Fonction qui affiche un arbre de décision
    def display_r(node: Node, tab: int=0, tree_str:str=""):
        # Fonction récursive qui affiche un arbre de décision
        for edge in node.edges_:  # Parcours des arêtes
            tree_str += "    "*tab + f"{node.criterion_} = {edge.get_label()}\n"
            # Affichage du critère et du label de l'arête
            child = edge.get_child()
            if not child.is_leaf(): # Si le noeud n'est pas une feuille
                tree_str += display_r(child, tab+1) # Appel récursif
            else:
                tree_str += "    "*(tab+1) + child.criterion_ + "\n"
                # Affichage de la comestibilité d'feuille
        return tree_str
    tree_str = display_r(tree) # Affichage de l'arbre
    print(tree_str) # Affichage de l'arbre
    return tree_str

def print_not_leaf(bt: BooleanTree, tree: str=""):
    # Fonction qui affiche un noeud non feuille
    node, edges, tab = bt.node, bt.edges_, bt.tab
    amount_or, child, edge = bt.amount_or, bt.get_edge_child(), bt.edge
    par = len([i.get_child().criterion_ != "No" for i in child.edges_]) > 1
    # Récupération des données nécessaires via la classe BooleanTree
    tree += f"({node.criterion_} = {edge.get_label()}" # Affichage du critère et du label de l'arête
    tree += " AND (\n" if par else " AND \n" # Affichage du "AND" si le noeud a plusieurs enfants
    tree += boolean_tree_r(BooleanTree(child, tab+1)) # Appel récursif
    tree += (")" if par else "") + (") OR " if amount_or < len(edges) else ")")
    # Affichage de la parenthèse fermante et du "OR" si le noeud a plusieurs enfants
    tree += "\n" + "    "*tab # Retour à la ligne et indentation
    return tree

def print_leaf(bt: BooleanTree, tree: str=""):
    # Fonction qui affiche une feuille
    node, edges, tab = bt.node, bt.edges_, bt.tab
    amount_or, edge = bt.amount_or, bt.edge
    # Récupération des données nécessaires via la classe BooleanTree
    tree += f"({node.criterion_} = {edge.get_label()})" # Affichage du critère et du label de l'arête
    tree += " OR " if amount_or < len(edges) else "" # Affichage du "OR" si le noeud a plusieurs enfants
    n = amount_or < len(edges)-1 and edges[amount_or].get_child().criterion_ == "Yes"
    tree += "\n" + "    "*tab if n and amount_or % 2 == 0 else ""
    # Retour à la ligne et indentation pour renre l'affichage plus lisible
    return tree

def boolean_tree_r(bt: BooleanTree, tree: str=""):
    # Fonction récursive qui affiche un arbre booléen
    tree += "    "*bt.tab # Indentation
    for bt.amount_or, bt.edge in enumerate(bt.edges_): # Parcours des arêtes
        bt.amount_or += 1
        child = bt.get_edge_child()
        if not child.is_leaf(): # Si ce n'est pas une feuille
            tree += print_not_leaf(bt) # Appel à la fonction qui print une arête
        elif child.criterion_ == "Yes":
            tree += print_leaf(bt) # Appel à la fonction qui print une feuille
    return tree

def boolean_tree(root: Node):
    # Fonction qui crée et renvoie un arbre booléen
    tree = "(" + boolean_tree_r(BooleanTree(root)) + ")"
    # Appel à la fonction récursive créatrice de l'arbre booléen
    print(tree)
    return tree

def print_criterions(ps: PythonScript, script: str=""):
    # Fonction qui print les critères des feuilles
    tab, node, leaves, if_ = ps.tab, ps.node, ps.leaves, ps.if_
    criterions = False
    # Récupération des données nécessaires via la classe PythonScript
    if len(leaves) > 3: # Si le nombre de feuilles est supérieur à 3
        script += "    "*tab + f"criterions = {leaves}\n"
        criterions = True # On met les critères dans une liste
    script += "    "*tab + ("elif" if if_ and not criterions else "if")
    ps.if_, if_ = True, True
    if len(leaves) == 1: # Si le nombre de feuilles est égal à 1
        script += f" mushroom.get_attribute('{node.criterion_}') == '{leaves[0]}':\n"
    elif len(leaves) > 0: # Si le nombre de feuilles est supérieur à 0, on regarde si on a mis les critères dans la liste
        script += f" mushroom.get_attribute('{node.criterion_}')"
        script += " in criterions:\n" if criterions else f" in {leaves}:\n"
        ps.clear_leaves()
    script += "    "*(tab+1) + "return True\n"
    return script

def print_if_not_leaves(ps: PythonScript, script: str=""):
    # Fonction qui print la condition si le noeud n'est pas une feuille
    tab, node, edge, if_ = ps.tab, ps.node, ps.edge, ps.if_
    script += "    "*tab + ("elif" if if_ else "if") # Affichage du "elif" ou du "if"
    script += f" mushroom.get_attribute('{node.criterion_}') == '{edge.get_label()}':\n"
    return script

def to_python_r(ps: PythonScript, script: str=""):
    # Fonction récursive qui crée un script python
    for edge in ps.edges_: # Parcours des arêtes
        ps.edge = edge
        child = ps.edge_get_child()
        if not child.is_leaf(): # Si le noeud n'est pas une feuille
            script += print_if_not_leaves(ps) # Appel à la fonction qui print la condition
            script += to_python_r(PythonScript(child, ps.tab+1)) # Appel récursif
        elif child.criterion_ == 'Yes':
                ps.leaves_append() # Ajout d'une feuille dans la liste
    script += print_criterions(ps) # Appel à la fonction qui print les valeurs des feuilles comesibles
    return script

def to_python(dt: Node, path: str):
    # Fonction qui crée un script python
    script = "from project import *\n\ndef is_edible(mushroom: Mushroom):\n"
    # Importation du fichier et création de la fonction
    script += to_python_r(PythonScript(dt)) # Appel à la fonction récursive
    script += "    else:\n" + "    "*(2) + "return False"
    # Ajout de la condition pour les feuilles non comestibles
    with open(path, "w") as file: # Ouverture du fichier
        file.write(script) # Écriture du script

def main(argv, argc):
    # Fonction principale "test"
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