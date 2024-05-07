import unittest
from project import *

class TestMushroomDataLoading(unittest.TestCase):
    def setUp(self):
        self.mushrooms = load_dataset('mushrooms.csv')

    def test_load_dataset(self):
        m1 = self.mushrooms[0]
        self.assertFalse(m1.is_edible(), "Le premier champignon devrait être non comestible.")
        self.assertEqual(m1.get_attribute('cap-shape'), 'Convex')
        self.assertEqual(m1.get_attribute('odor'), 'Pungent')

        m2 = self.mushrooms[1]
        self.assertTrue(m2.is_edible(), "Le deuxième champignon devrait être comestible.")
        self.assertEqual(m2.get_attribute('cap-color'), 'Yellow')
        self.assertEqual(m2.get_attribute('odor'), 'Almond')

        m3 = self.mushrooms[2]
        self.assertTrue(m3.is_edible(), "Le troisième champignon devrait être comestible.")
        self.assertEqual(m3.get_attribute('cap-shape'), 'Bell')
        self.assertEqual(m3.get_attribute('odor'), 'Anise')

def make_mushroom(attributes):
    ret = Mushroom(None)
    for k, v in attributes.items():
        ret.add_attribute(k, v)
    return ret

class TestBuildTree(unittest.TestCase):
    def setUp(self):
        self.test_tree_root = build_decision_tree(load_dataset('mushrooms.csv'))

    def test_tree_main_attribute(self):
        self.assertEqual(self.test_tree_root.criterion_, 'odor', "Le premier critère de division doit être 'odor'")
        nos = ['Pungent', 'Creosote', 'Foul', 'Fishy', 'Spicy', 'Musty']
        odors = {edge.label_: edge.child_ for edge in self.test_tree_root.edges_}
        for odor in nos:
            self.assertTrue(
                odors[odor].is_leaf() and odors[odor].criterion_ == 'No',
                f'Les champignons avec une odeur \'{odor}\' doivent être non-comestibles'
            )
    def test_tree_prediction(self):
        root = self.test_tree_root
        self.assertTrue(is_edible(root, make_mushroom({'odor': 'Almond'})))
        self.assertFalse(is_edible(root, make_mushroom({'odor': 'None', 'spore-print-color': 'Green'})))

class PersonnalTestsPart1(unittest.TestCase):
# Classe contenant les tests de la 1ère partie du projet
# Les tests sont effectués sur les fonctions de calcul d'entropie et d'information gain
    def setUp(self):
        self.mushrooms = load_dataset('mushrooms.csv')
        self.test_tree_root = build_decision_tree(self.mushrooms)
    
    def test_entropy(self):
    # Test de la fonction d'entropie
        edible = [m for m in self.mushrooms if m.is_edible()]
        poisonous = [m for m in self.mushrooms if not m.is_edible()]
        self.assertEqual(entropy(edible), 0) # Entropie de la liste des champignons comestibles
        self.assertEqual(entropy(poisonous), 0) # Entropie de la liste des champignons non comestibles
        self.assertEqual(entropy(self.mushrooms), 0.9990678968724604)
        # Entropie de la liste des champignons
    
    def test_information_gain(self):
    # Test de la fonction d'information gain
        tree = self.test_tree_root
        self.assertEqual(tree.criterion_, get_best_attribute(self.mushrooms)) # Le critère de division des champignons
        self.assertEqual(get_information_gain(self.mushrooms, 'odor'), 0.9060749773839998) # Information gain pour le critère 'odor'
        mushrooms = [m for m in self.mushrooms if m.get_attribute('odor') == 'None']
        tree_e = [e for e in tree.edges_ if e.get_label() == "None"][0]
        tree = tree_e.child_
        self.assertEqual(tree.criterion_, get_best_attribute(mushrooms)) # Le critère de division après la division par la valeur 'None' de 'odor'
        self.assertEqual(get_information_gain(mushrooms, 'spore-print-color'), 0.14493721491485229) # Information gain pour le critère 'spore-print-color'

class PersonnalTestsPart2(unittest.TestCase):
# Classe contenant les tests de la 2ème partie du projet
# Les tests sont effectués sur les fonctions d'affichage de l'arbre de décision et de génération de code Python
    def setUp(self):
        self.mushrooms = load_dataset('mushrooms.csv')
        self.test_tree_root = build_decision_tree(self.mushrooms)
        self.path = "decision_tree.py"
    
    def test_is_edible(self):
    # Test de la fonction is_edible
        root = self.test_tree_root
        self.assertTrue(is_edible(root, make_mushroom({'odor': 'Almond'}))) # Champignon comestible
        self.assertFalse(is_edible(root, make_mushroom({'odor': 'None', 'spore-print-color': 'Green'}))) # Champignon non comestible
    
    def test_display(self):
    # Test de la fonction d'affichage de l'arbre de décision
        tree_d = display(self.test_tree_root).split()
        tree_d = [t.strip() for t in tree_d if "=" not in t] # Listes des attributs et valeurs affichés
        tree = self.test_tree_root
        self.assertEqual(tree.criterion_, "odor") # Le critère de division de l'arbre
        stack = {tree.criterion_ : [(edge, edge.get_parent()) for edge in tree.edges_]} # Dictionnaire des listes des arêtes et des nœuds parents en fonction des attributs
        while sum(len(l) for l in stack.values()) > 0: # Tant qu'il reste des éléments dans le dictionnaire
            criterion, label = tree_d.pop(0), tree_d.pop(0) # Récupération de l'attribut et de la valeur affichés
            edge, node = stack[criterion].pop(0) # Récupération de la première arête et du premier nœud parent
            if tree_d[0] in ["No", "Yes"]: # Si le nœud est une feuille
                node = edge.get_child()
                criterion = tree_d.pop(0) # Récupération de la valeur de la feuille
                self.assertTrue(node.is_leaf()) # Le nœud doit être une feuille
            self.assertEqual(node.criterion_, criterion) # Le nœud doit avoir le même attribut que celui affiché
            self.assertEqual(edge.get_label(), label) # L'arête doit avoir la même valeur que celle affichée
            if not node.is_leaf(): # Si le nœud n'est pas une feuille
                self.modify_stack(stack, edge) # Mise à jour du dictionnaire

    def modify_stack(self, stack, edge):
    # Fonction de mise à jour du dictionnaire des arêtes et des nœuds parents
        node = edge.get_child() # Récupération du nœud enfant
        suite = [(e, e.get_parent()) for e in node.edges_] # Liste des arêtes et des nœuds parents
        if len(suite) > 0: # Si la liste n'est pas vide
            next_c = suite[0][-1].criterion_ # Récupération de l'attribut du premier nœud parent
            if not next_c in stack: 
                stack[next_c] = suite # Ajout de la liste au dictionnaire
            else:
                stack[next_c].extend(suite) # Ajout des éléments de la liste au dictionnaire
            
    def test_to_python(self):
    # Test de la fonction de génération de code Python
        to_python(self.test_tree_root, self.path) # Génération du code Python
        from decision_tree import is_edible # Importation de la fonction is_edible
        self.assertTrue(is_edible(make_mushroom({'odor': 'Almond'}))) # Champignon comestible
        self.assertFalse(is_edible(make_mushroom({'odor': 'None', 'spore-print-color': 'Green'}))) # Champignon non comestible

class TestBooleanTree(unittest.TestCase):
# Classe contenant les tests de la génération de l'arbre booléen
    def setUp(self):
        self.mushrooms = load_dataset('mushrooms.csv')
        self.tree = build_decision_tree(self.mushrooms)
        self.boolean_tree = boolean_tree(self.tree)
    
    def test_count_parenthesis(self):
        # Test du nombre de parenthèses
        tree = self.boolean_tree
        self.assertEqual(tree.count("("), tree.count(")")) 
        # Test du nombre de parenthèses pour 3 arbres différents
        
        tree2 = build_decision_tree(self.mushrooms)
        bt2 = boolean_tree(tree2)
        self.assertEqual(bt2.count("("), bt2.count(")"))

        tree3 = build_decision_tree(self.mushrooms)
        bt3 = boolean_tree(tree3)
        self.assertEqual(bt3.count("("), bt3.count(")"))
    
    def test_boolean_tree(self):
        # Test de l'arbre booléen
        tree = self.tree
        tree_bt = self.boolean_tree
        tree_bt = tree_bt.replace("(", "").replace(")", "")
        tree_bt = tree_bt.split()
        tree_bt = [t.strip() for t in tree_bt if t.strip() not in ["OR", "AND", "="]]
        # Listes des éléments de l'arbre booléen
        self.assertEqual(tree.criterion_, "odor")
        stack = {tree.criterion_ : [(edge, edge.get_parent()) for edge in tree.edges_ if edge.get_child().criterion_ != "No"]}
        # Dictionnaire des listes des arêtes et des nœuds parents en fonction des attributs
        while sum(len(value) for value in stack.values()) > 0: # Tant qu'il reste des éléments dans le dictionnaire
            criterion, label = tree_bt.pop(0), tree_bt.pop(0)
            edge, node = stack[criterion].pop(0)
            # Récupération de l'attribut et de la valeur affichés, de la première arête et du premier nœud parent
            self.assertEqual(node.criterion_, criterion) # Le nœud doit avoir le même attribut que celui affiché
            self.assertEqual(edge.get_label(), label) # L'arête doit avoir la même valeur que celle affichée
            if not node.is_leaf(): # Si le nœud n'est pas une feuille
                self.modify_stack(stack, edge) # Mise à jour du dictionnaire
    
    def modify_stack(self, stack, edge):
    # Fonction de mise à jour du dictionnaire des arêtes et des nœuds parents
        node = edge.get_child() # Récupération du nœud enfant
        suite = [(e, e.get_parent()) for e in node.edges_ if e.get_child().criterion_ != "No"]
        # Liste des arêtes et des nœuds parents
        if len(suite) > 0: # Si la liste n'est pas vide
            next_c = suite[0][-1].criterion_ # Récupération de l'attribut du premier nœud parent
            if not next_c in stack: # Si l'attribut n'est pas dans le dictionnaire
                stack[next_c] = suite # Ajout de la liste au dictionnaire
            else:
                stack[next_c].extend(suite) # Ajout des éléments de la liste au dictionnaire

if __name__ == '__main__':
    unittest.main()