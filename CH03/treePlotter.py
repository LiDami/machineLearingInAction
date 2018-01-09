# -*- coding:utf8 -*-

import matplotlib.pyplot as plt

####
##### 定义文本框和箭头格式
####
decisionNode = dict(boxstyle="sawtooth",fc="0.8") #带锯齿
leafNode = dict(boxstyle="round4",fc="0.8")  #带圆
arrow_args = dict(arrowstyle="<-")

#####
###### 绘制带箭头的注解
#####
def plotNode(nodeTxt,centerPt,parentPt,nodeType):
    # 被注释的地方xy(x, y)和插入文本的地方xytext(x, y)
    createPlot.ax1.annotate(nodeTxt,xy=parentPt,xycoords='axes fraction',xytext=centerPt,textcoords='axes fraction',\
                            va='center',ha='center',bbox=nodeType,arrowprops=arrow_args)

# def createPlot():
#     fig = plt.figure(1,facecolor='white')
#     fig.clf() #创建一个新图形后并清空绘图区
#     createPlot.ax1 = plt.subplot(111,frameon=False)
#     #（注解的文字，注解的坐标，不带箭头的坐标，注解显示的方式）
#     plotNode(U'decisionNode',(0.5,0.1),(0.1,0.5),decisionNode)
#     plotNode(U'leafNode',(0.8,0.1),(0.3,0.8),leafNode)
#     plt.grid()
#     plt.show()

########
######### 获取叶节点的数目和树的层数
#######
def getNumLeafs(myTree):
    numleafs = 0
    firstStr = myTree.keys()[0] #获取第一个key
    secondDict = myTree[firstStr] # 获取第一个key对应的value
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict': #判断类型，若还为字典型，则该节点是一个判断节点，需要继续递归调用此函数
            numleafs += getNumLeafs(secondDict[key])
        else: numleafs += 1
    return numleafs
def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key]) # 一层就加1
        else: thisDepth = 1 # 从根节点开始，如果中途就停止了，就设置为1，因为寻找的是形成树的最长路径，最长路径的长度即为深度
        if thisDepth > maxDepth : maxDepth = thisDepth
    return maxDepth

###### 只是为了方便测试数据
def testData(i):
    listOfTrees = [{'no surfacing':{0:'no',1:{'flippers':\
                                                  {0:'no',1:'yes'}}}},
                   {'no surfacing':{0:'no',1:{'flippers':\
                                                  {0:{'head':{0:'no',1:'yes'}},1:'no'}}}}
                   ]
    return listOfTrees[i]

######
####### 在父节点之间填充信息
######
def plotMidText(centrPt,parentPt,txtString):
    xMid = (parentPt[0] - centrPt[0])/2.0 + centrPt[0]
    yMid = (parentPt[1] - centrPt[1])/2.0 + centrPt[1]
    createPlot.ax1.text(xMid,yMid,txtString)

#####
###### 逻辑绘制树
#####
def plotTree(myTree,parentPt,nodeTxt):
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)
    firstStr = myTree.keys()[0]
    centrPt = (plotTree.xOff + (1 + float(numLeafs))/2.0/plotTree.totalW,plotTree.yOff)
    #绘制头结点
    plotMidText(centrPt,parentPt,nodeTxt)
    plotNode(firstStr,centrPt,parentPt,decisionNode)
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key],centrPt,str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key],(plotTree.xOff,plotTree.yOff),centrPt,leafNode)
            plotMidText((plotTree.xOff,plotTree.yOff),centrPt,str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD

def createPlot(inTree):
    fig = plt.figure(1,facecolor='white')
    fig.clf()
    axprops = dict(xticks=[],yticks=[])
    createPlot.ax1 = plt.subplot(111,frameon=False,**axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(inTree,(0.5,1.0),'')
    plt.grid()
    plt.show()













