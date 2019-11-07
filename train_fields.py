#!/usr/bin/python

from decision_tree import DecisionTree

tree = DecisionTree('field.csv')
decision_tree_result = tree.create_tree_dict(tree.training_data, tree.classes, tree.features)
tree.show_tree(decision_tree_result, ' ')