'''
在构建决策树之后，此部分主要用于绘制树形图
'''
'''import matplotlib.pyplot as plt
decisionNode = dict(boxstyle="sawtooth",fc="o.8")
leafNode = dict(boxstyle="round4",fc="0.8")
arrow_args = dict(arrowstyle="<-")
def plotNode(nodeTxt,centerPt,parent,nodeType):
    creatPlot.ax1.annotate(nodeTxt,xy=parent,xycoords="axes fraction",xytext=centerPt,textcoords="axes fraction",\
                           va="center",ha="center",bbox="nodeType",arrowprops=arrow_args)
def creatPlot():
    fig = plt.figure(1,facecolor="white")
    fig.clf()
    creatPlot.ax1 = plt.subplot(111,frameon=False)
    plotNode("决策结点",(0.5,0.1),(0.1,0.5),decisionNode)
    plotNode("叶节点",(0.8,0.1),(0.3,0.8),leafNode)
    plt.show()
#creatPlot()'''
import decision_tree.trees as T
dataset = [  # 这里仅作为演示,实际的数据集可能从数据库或者文件中读入
    [1, 1, 'yes'],
    [1, 1, 'yes'],
    [1, 0, 'no'],
    [0, 1, 'no'], #为了方便其他模块调用，提高代码重用性，也可单独把数据集与标签集拿出来使用
    [0, 1, 'no']
]
labels = ['no surfacing', 'flippers']
def getNumLeafs(myTree):#获得树叶节点个数
    numLeafs = 0
    firstStr = list(myTree.keys())[0]#获取树的第一个键
    secondDict = myTree[firstStr]#获取树的第一个键的值
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == "dict":#判断子节点是否是字典类型,若是，继续进行递归调用
            numLeafs += getNumLeafs(secondDict[key])#递归进行调用
        else:
            numLeafs += 1
    return numLeafs
def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == "dict":
            thisDepth = 1 + getNumLeafs(myTree)
        else:
            thisDepth = 1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth
def plotMidText(cntrPt,parentPt,txtString):
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid,yMid,txtString)
def plotTree(myTree,parentPt,nodeTxt):
    numLeafs = getTreeDepth(myTree)
    depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)/2.0/plotTree.totallW,plotTree.yOff))

myTree = T.createTree(dataset,labels)
#print(getNumLeafs(myTree))
#print(getTreeDepth(myTree))


