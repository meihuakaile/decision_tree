# -*- coding:utf-8 -*-
# __author__='chenliclchen'

from matplotlib import pyplot as plt

# 画每个节点
def plot_node(node_text, parent_pt, center_parent, nodetype):
    # s 标签； xy 注释的位置（就是箭头的起始位置）；xytext 标签的位置；
    # xycoords 注释位置（xy）坐标的类型； textcoords 标签位置(xytext)坐标的类型； arrowprops 字典，箭头的属性
    ax.annotate(node_text, xy=parent_pt, xytext=center_parent,
                xycoords='axes fraction', textcoords='axes fraction',
                va='center', ha='center', bbox=nodetype, arrowprops=arrow_args)

# 画箭头上的内容，也就是每个节点的选择值
def plot_text(parent_pt, center_parent, text):
    x = (parent_pt[0] - center_parent[0]) / 2 + center_parent[0]
    y = (parent_pt[1] - center_parent[1]) / 2 + center_parent[1]
    ax.text(x, y, text)

# 计算树的深度，为了画树的y坐标做准备
def get_tree_deep(tree):
    if isinstance(tree, str):
        return 1
    elif isinstance(tree, dict):
        key = tree.keys()[0]
        value = tree[key]
        deep = 0
        for item in value.keys():
            this_deep = 1 + get_tree_deep(value[item])
            deep = this_deep if this_deep > deep else deep
        return deep

# 计算叶子节点，为画树时的x坐标准备
def get_leafnode_num(tree, leafnode_num):
    if isinstance(tree, str):
        leafnode_num += 1
        return leafnode_num
    elif isinstance(tree, dict):
        key = tree.keys()[0]
        value = tree[key]
        for item in value.keys():
            leafnode_num = get_leafnode_num(value[item], leafnode_num)
        return leafnode_num

# node_text是节点里的内容； parent_pt是箭头出发的位置； center_parent箭头结束的位置 ；
# key是箭头上的标示，也是决策树的选择值； had_draw_leafnode 已经画过的叶子节点，为了计算下一个叶子节点的x坐标
def draw_tree(node_text, parent_pt, center_parent, key, had_draw_leafnode):
    if isinstance(node_text, str):
        plot_text(parent_pt, center_parent, key)
        plot_node(node_text, parent_pt, center_parent, decisionNode)
        had_draw_leafnode += 1
        return had_draw_leafnode
    elif isinstance(node_text, dict):
        next_key = node_text.keys()[0]
        value = node_text[next_key]
        plot_text(parent_pt, center_parent, key)
        plot_node(next_key, parent_pt, center_parent, leafNode)
        for item in value.keys():
            this_leafnum_node = get_leafnode_num(value[item], 0)
            next_xind = had_draw_leafnode * x_off + (this_leafnum_node - 1) * x_off / 2
            had_draw_leafnode = draw_tree(value[item], center_parent, (next_xind, center_parent[1]-y_off), item, had_draw_leafnode)
        return had_draw_leafnode

# tree = {'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}}
# tree = {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
# tree = {'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}, 3: 'maybe'}}
tree = {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}, 3: 'maybe'}}

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")
# 1(num)是作为一个id，如果这个id已经存在就激活返回引用否则就创建返回引用
# figsize 元组，图片大小，宽高; dpi 图片分辨率； facecolor 是背景色; edgecolor 边框色；
fig = plt.figure(1, facecolor='w')
fig.clf()
# 不显示坐标数据
axprops = dict(xticks=[], yticks=[])
# frameon=False 是否显示坐标轴架构
ax = plt.subplot(111, frameon=False, **axprops)

# 为了计算画每个节点时xy坐标需要移动的大小
tree_deep = get_tree_deep(tree)
leafnum_node = get_leafnode_num(tree, 0)
x_off = 1.0 / (leafnum_node - 1)
y_off = 1.0 / (tree_deep - 1)
# 画树并展示
draw_tree(tree, (0.5, 1.0), (0.5, 1.0), '', 0)
plt.show()
