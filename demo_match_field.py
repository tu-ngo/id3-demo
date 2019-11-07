#!/usr/bin/python

from decision_tree import DecisionTree
from csv_reader import CsvRows

tree = DecisionTree('field.csv')
decision_tree_result = tree.create_tree_dict(tree.training_data, tree.classes, tree.features)
tree.show_tree(decision_tree_result, ' ')

csv_rows = CsvRows('field.csv')

for row in csv_rows.get_records():
    result = tree.evaluate(decision_tree_result, row)
    print (result + '  ==> ', row)
