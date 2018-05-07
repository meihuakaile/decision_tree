# -*- coding:utf-8 -*-
# __author__='chenliclchen'
from __future__ import division
import operator
import math
import numpy as np

def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    return dataSet, labels

# 加载隐形眼镜的数据集
def load_lenses_data(path='./lenses/lenses.txt'):
    file = open(path)
    dataset = []
    for line in file.readlines():
        data = line.split('\t', 4)
        data[-1] = data[-1].replace('\r\n', '')
        dataset.append(data)
    labels = ['age', 'prescript', 'astigmatic', 'tearRate']
    file.close()
    return dataset, labels

# 计算出现次数最多的类别
def get_most_vote(class_list):
    result_dict = {}
    for item in class_list:
        if item in result_dict.keys():
            result_dict[item] += 1
        else:
            result_dict[item] = 1
    sorted_dict = sorted(result_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_dict[0][0]

# 计算某特征某值的熵
def cac_entropy(dataset):
    class_list = [data[-1] for data in dataset]
    dataset_num = len(dataset)
    dict = {}
    for item in class_list:
        if item in dict.keys():
            dict[item] += 1
        else:
            dict[item] = 1
    probs = 0.0
    for item in dict.keys():
        prob = dict[item] / dataset_num
        probs += prob * math.log(prob, 2)
    return probs * -1

# 计算最好增益的特征
def get_best_feature(dataset):
    feature_nums = len(dataset[0]) - 1
    data_array = np.array(dataset)
    # 计算条件熵，即基础熵
    base_entropy = cac_entropy(dataset)
    # 最好的增益 条件熵 - 基础熵
    best_gain = 0.0
    # 最好增益的下标
    best_gain_ind = -1
    for indy in xrange(feature_nums):
        value_list = [data[indy] for data in dataset]
        value_len = len(value_list)
        values = set(value_list)
        new_entropy = 0.0
        for value in values:
            data = list(data_array[data_array[:, indy] == str(value), :])
            one_data_entropy = cac_entropy(data)
            prob = value_list.count(value) / value_len
            new_entropy += prob * one_data_entropy
        one_feature_gain = base_entropy - new_entropy
        if one_feature_gain >= best_gain:
            best_gain = one_feature_gain
            best_gain_ind = indy
    return best_gain_ind

# 计算决策树
def get_tree(dataset, labels):
    class_list = [data[-1] for data in dataset]
    # 数据集只剩一种类别
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]
    # 特征用完，数据集不为0
    if len(dataset) != 0 and len(labels) == 0:
        return get_most_vote(class_list)
    # 选出当前节点最好的特征
    best_feature = get_best_feature(dataset)
    tree = {labels[best_feature]: {}}
    # 除去当前特征值列的新数据集
    new_data = []
    for data in dataset:
        new_item = data[:best_feature]
        new_item.extend(data[best_feature+1:])
        new_data.append(new_item)
    new_labels = labels[:]
    del(new_labels[best_feature])

    # 当前特征值选择不同分支时，递归
    values = [data[best_feature] for data in dataset]
    feature_values = set(values)
    for value in feature_values:
        one_feature_data = []
        for ind in xrange(len(dataset)):
            if dataset[ind][best_feature] == value:
                tmp = new_data[ind][:]
                one_feature_data.append(tmp)
        tree[labels[best_feature]][value] = get_tree(one_feature_data, new_labels)
    return tree

# 分类
def classify(data, tree, labels):
    if isinstance(tree, str):
        return tree
    elif isinstance(tree, dict):
        key = tree.keys()[0]
        value = data[labels.index(key)]
        return classify(data, tree[key][value], labels)

# 存储
def save_tree(tree, save_path='tree.pkl'):
    import pickle
    file = open(save_path, 'w')
    pickle.dump(tree, file)
    file.close()

dataset, labels = createDataSet()
# {'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}}
dataset, labels = load_lenses_data()
# {'tearRate': {'reduced': 'no lenses', 'normal': {'astigmatic': {'yes': {'prescript': {'hyper': {'age': {'pre': 'no lenses', 'presbyopic': 'no lenses', 'young': 'hard'}}, 'myope': 'hard'}}, 'no': {'age': {'pre': 'soft', 'presbyopic': {'prescript': {'hyper': 'soft', 'myope': 'no lenses'}}, 'young': 'soft'}}}}}}
tree = get_tree(dataset, labels)
save_tree(tree)
print 'tree is : ', tree
data = ['young', 'hyper', 'yes', 'normal']
labels = ['age', 'prescript', 'astigmatic', 'tearRate']
result = classify(data, tree, labels)
print 'data is :', data, 'result is : ', result