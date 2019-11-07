#!/usr/bin/python

from decision_tree import DecisionTree

table_decision_tree = DecisionTree('table.csv')
table_ds_result = table_decision_tree.create_tree_dict(table_decision_tree.training_data, table_decision_tree.classes, table_decision_tree.features)
table_decision_tree.show_tree(table_ds_result, ' ')