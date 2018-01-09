# -*- coding:utf8 -*-

from math import  log
import operator

#####
######  计算熵。。。H = - ΣP*logP
######
def calcShannonEnt(dataSet):
    numLen = len(dataSet)
    #新建一个字典
    labelCount = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        #如果label不在当前字典里，新建一个key
        if currentLabel not in labelCount.keys():
            labelCount[currentLabel] = 0
        #统计key出现的次数
        labelCount[currentLabel] += 1
    #print labelCount  # 结果为：{'yes': 2, 'no': 3}
    shannonEnt = 0.0
    #开始计算熵
    for key in labelCount:
        prob = float(labelCount[key])/numLen
        shannonEnt -= prob * log(prob,2)
    return shannonEnt

#####
###### 测试上面的函数
#####
def createDataSet():
    dataSet = [
        [1,1,'yes'],
        [1,1,'yes'],
        [1,0,'no'],
        [0,1,'no'],
        [0,1,'no']]
    labels = ['no surfacing','flippers']
    return dataSet,labels

######
####### 划分数据集,axis为特征的列，value为那个特征的值，返回除axis[]=value的列的所有列集
######
def splitDataSet(dataSet,axis,value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            #这里打印出特征axis之前的其他特征值，当然不包含最后一位是[ )的形式，即不打印含有特征的list
            reducedFeatV = featVec[:axis]
            #print retDataSet
            reducedFeatV.extend(featVec[axis+1:])
            #这个append，是含有[]符号的添加
            retDataSet.append(reducedFeatV)
    return retDataSet

######
####### 选择最好的数据划分方式，开始计算信息增益。H= - ΣP*logP - - - ΣP Σp*logp
######
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1 #行，出去最后一列标签的剩下特征的个数
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0;bestFeature = -1
    #遍历每个特征列
    for i in range(numFeatures):
        #获取特征列
        featList = [example[i] for example in dataSet]
        #去除特征列中重复的，留下唯一的特征
        uniqueVals = set(featList)
        #初始化经验熵
        newEntropy = 0.0
        #遍历特征列中，划分数据集，计算熵，计算经验熵，然后得到信息增益
        for value in uniqueVals:
            #得到划分数据集后的数据
            subDataSet = splitDataSet(dataSet,i,value)
            #计算概率
            prob = len(subDataSet)/float(len(dataSet))
            #经验熵，在H(D|A)
            newEntropy += prob * calcShannonEnt(subDataSet)
        #计算信息增益
        infoGain = baseEntropy - newEntropy
        #返回最大的增益
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

#######
######## 返回出现次数最多的分类名称
#######
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not  in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

########
######### 创建树
########
def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    #情况1：如果类别完全相同，就停止划分
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    #情况2：在只有一个特征的时候，返回出现次数最多的
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    #情况3，正常情况
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabels = labels[bestFeat]
    myTree = {bestFeatLabels:{}}
    del(labels[bestFeat]) #清空，在下一次调用时
    #得到列表包含的所有属性值
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        #复制标签，为了不让原始列表改变
        subLabels = labels[:]
        #递归调用决策树函数
        myTree[bestFeatLabels][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree

######
###### 测试算法：使用决策树执行分类
#####
def classify(inputTree,featLabels,testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key],featLabels,testVec)
            else:
                classLabel = secondDict[key]
    return classLabel

######
####### 决策树的存储，是=使用pickle
#####
def storeTree(inputTree,fileName):
    import pickle
    fw =open(fileName,'w')
    pickle.dump(inputTree,fw)
    fw.close()
def grabTree(fileName):
    import pickle
    fr = open(fileName)
    return pickle.load(fr)







