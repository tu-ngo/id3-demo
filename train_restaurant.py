#!/usr/bin/python

from decision_tree import DecisionTree

tree = DecisionTree('restaurant.csv')
decision_result = tree.create_tree_dict(tree.training_data, tree.classes, tree.features)
tree.show_tree(decision_result, ' ')