# -*- coding:utf-8 -*-
# __author__='chenliclchen'

from matplotlib import pyplot as plt

def plot_node(node_text, parent_pt, center_parent, nodetype):
    # s 标签； xy 注释的位置（就是箭头的起始位置）；xytext 标签的位置；
    # xycoords 注释位置（xy）坐标的类型；textcoords 标签位置(xytext)坐标的类型；arrowprops 字典，箭头的属性
    # https: // matplotlib.org / users / annotations.html
    ax.annotate(node_text, xy=parent_pt, xytext=center_parent,
                xycoords='axes fraction', textcoords='axes fraction',
                va='center', ha='center', bbox=nodetype, arrowprops=arrow_args)

tree = {'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}}
decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")
# 1(num)是作为一个id，如果这个id已经存在就激活返回引用否则就创建返回引用
# figsize 元组，图片大小，宽高; dpi 图片分辨率； facecolor 是背景色; edgecolor 边框色；
fig = plt.figure(1, facecolor='w')
fig.clf()
# frameon=False 是否显示坐标轴架构
ax = plt.subplot(111, frameon=False)
plot_node('de', (0.1, 0.5), (0.5, 0.1), decisionNode)
plot_node('leaf', (0.3, 0.8), (0.8, 0.1), leafNode)
plt.show()