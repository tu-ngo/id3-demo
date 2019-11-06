# This program implements ID3 algorithm in python. The input should be a file
# containing the training data.
# The format of training data is as follows:
#     A. At the first line put the attribute (column) names separated by comma.
#     B. In the consequence lines, attribute values must come in the order of
#     attribute names and separated by comma.
#
# The output is a decision tree and its demonstration.

import math


class DecisionTree:
    def __init__(self, file_name):
        fid = open(file_name, "r")
        data = []
        d = []
        for line in fid.readlines():
            d.append(line.strip())
        for d1 in d:
            data.append(d1.split(","))
        fid.close()

        self.features = self.get_features(data)
        data = data[1:]
        self.classes = self.get_classes(data)
        data = self.get_pure_data(data)
        self.training_data = data

    def get_classes(self, data):
        data = data[1:]
        classes = []
        for d in range(len(data)):
            classes.append(data[d][-1])

        return classes

    def get_features(self, data):
        features = data[0]
        features = features[:-1]
        return features

    def get_pure_data(self, data_rows):
        data_rows = data_rows[1:]
        for d in range(len(data_rows)):
            data_rows[d] = data_rows[d][:-1]
        return data_rows

    def zero_list(self, size):
        d = []
        for i in range(size):
            d.append(0)
        return d

    def get_arg_max(self, arr):
        m = max(arr)
        ix = arr.index(m)
        return ix

    def get_distinct_values(self, data_list):
        distinct_values = []
        for item in data_list:
            if (distinct_values.count(item) == 0):
                distinct_values.append(item)
        return distinct_values

    def get_distinct_values_from_table(self, data_table, column):
        distinct_values = []
        for row in data_table:
            if (distinct_values.count(row[column]) == 0):
                distinct_values.append(row[column])
        return distinct_values

    def get_entropy(self, p):
        if (p != 0):
            return -p * math.log(p, 2)
        else:
            return 0

    def create_tree(self, training_data, classes, features, max_level=-1, level=0):
        n_data = len(training_data)
        n_features = len(features)

        try:
            self.features
        except:
            self.features = features

        new_classes = self.get_distinct_values(classes)
        frequency = self.zero_list(len(new_classes))
        total_entropy = 0
        index = 0
        for a_class in new_classes:
            frequency[index] = classes.count(a_class)
            prob = float(frequency[index]) / n_data
            total_entropy += self.get_entropy(prob)
            index += 1

        default = classes[self.get_arg_max(frequency)]
        if (n_data == 0 or n_features == 0 or (max_level >= 0 and level > max_level)):
            return default
        elif classes.count(classes[0]) == n_data:
            return classes[0]
        else:
            gain = self.zero_list(n_features)
            for feature in range(n_features):
                g = self.get_gain(training_data, classes, feature)
                gain[feature] = total_entropy - g

            best_feature = self.get_arg_max(gain)
            new_tree = {features[best_feature]: {}}

            values = self.get_distinct_values_from_table(training_data, best_feature)
            for value in values:
                new_data = []
                new_classes = []
                index = 0
                for row in training_data:
                    if row[best_feature] == value:
                        if best_feature == 0:
                            new_row = row[1:]
                            new_names = features[1:]
                        elif best_feature == n_features:
                            new_row = row[:-1]
                            new_names = features[:-1]
                        else:
                            new_row = row[:best_feature]
                            new_row.extend(row[best_feature + 1:])
                            new_names = features[:best_feature]
                            new_names.extend(features[best_feature + 1:])
                        new_data.append(new_row)
                        new_classes.append(classes[index])
                    index += 1

                subtree = self.create_tree(new_data, new_classes, new_names, max_level, level + 1)

                new_tree[features[best_feature]][value] = subtree
            return new_tree

        print(new_classes)

    def get_gain(self, data, classes, feature):
        gain = 0
        ndata = len(data)

        values = self.get_distinct_values_from_table(data, feature)
        feature_counts = self.zero_list(len(values))
        entropy = self.zero_list(len(values))
        value_index = 0
        for value in values:
            data_index = 0
            new_classes = []
            for row in data:
                if row[feature] == value:
                    feature_counts[value_index] += 1
                    new_classes.append(classes[data_index])
                data_index += 1

            class_values = self.get_distinct_values(new_classes)
            class_counts = self.zero_list(len(class_values))
            class_index = 0
            for classValue in class_values:
                for a_class in new_classes:
                    if a_class == classValue:
                        class_counts[class_index] += 1
                class_index += 1

            for class_index in range(len(class_values)):
                pr = float(class_counts[class_index]) / sum(class_counts)
                entropy[value_index] += self.get_entropy(pr)

            pn = float(feature_counts[value_index]) / ndata
            gain = gain + pn * entropy[value_index]

            value_index += 1
        return gain

    def show_tree(self, dic, seperator):
        if (type(dic) == dict):
            for item in dic.items():
                print(seperator, item[0])
                self.show_tree(item[1], seperator + " | ")
        else:
            print(seperator + " -> (", dic + ")")


# tree = DecisionTree('restaurant.csv')
# tree = DecisionTree('field.csv')
tree = DecisionTree('dataset.csv')
tree1 = tree.create_tree(tree.training_data, tree.classes, tree.features)
tree.show_tree(tree1, ' ')
