# encoding: utf-8

'''
@author: LiDami
@license: (C) Copyright 2013-2017, BigBigData Manager Corporation Limited.
@contact: li.dami@foxmail.com
@software: MacBookPro
@file: bayes.py
@time: 2018/1/7 19:35
@desc:
'''
from numpy import *
import re
import feedparser


def loadDataSet():
    postingList = [
        ['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
        ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
        ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
        ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
        ['my', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
        ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
    ]
    classVec = [0, 1, 0, 1, 0, 1]
    return postingList, classVec

# 把所有的文档去重，展示去重后的词条列表
def createVocabList(dataSet):
    #     新建一个set存放
    vocabSet = set([])
    #     遍历传入的文档
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    # 转换为list
    return list(vocabSet)

# 把词条转换为向量，存在的显示1，不存在的显示0
def setOfWords2Vec(vocabSet, inputSet):
    returnVec = [0] * len(vocabSet)
    for word in inputSet:
        if word in vocabSet:
            returnVec[vocabSet.index(word)] += 1
        else:
            print("the word:%s is not my vocabulary!" % word)
    return returnVec

# p(ci|w)=p(w|ci)*p(ci)/p(w)
# 1，先计算p(ci),即每个类别占总文档的比例
# 2，在计算p(w|ci),在类1中词条向量出现的总数概率
# @trainMatrix为转换后的词向量矩阵
# @trainCategory每篇文档对应的类别
def trainNB0(trainMatrix, trainCategory):
    #    1, 计算p(ci)
    # 获取矩阵中稳当的数目
    numTrainDocs = len(trainMatrix)
    # 获取每一个类别中的词条向量的长度
    numWords = len(trainMatrix[0])
    # 计算ci为1类别的p(ci)
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    #     2,计算p(w|ci)
    # 定义分子分母
    p0Num = ones(numWords);
    p1Num = ones(numWords)
    p0Denom = 2.0;
    p1Denom = 2.0
    # 对于每一篇文档中的词条向量
    for i in range(numTrainDocs):
        # 统计所有类别为1的词条的出现的次数
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            # 统计类别为1的词条的总数目
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
        # 计算p(w|ci)
    p1Vect = log(p1Num / p1Denom)
    p0Vect = log(p0Num / p0Denom)
    return p0Vect, p1Vect, pAbusive

# 计算待分类文档属于哪个类
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

# 综合一下分类测试整体函数
def testingNB():
    listObj, listClass = loadDataSet()
    myVocabList = createVocabList(listObj)
    trainMat = []
    for posDoc in listObj:
        trainMat.append(setOfWords2Vec(myVocabList, posDoc))
    p0V, p1V, pAb = trainNB0(trainMat, listClass)

    #     测试文档1
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print (testEntry, 'classified as :', classifyNB(thisDoc, p0V, p1V, pAb))
    # 测试文档2
    testEntry1 = ['stupid', 'garbage']
    # 同样转为词条向量，并转为NumPy数组的形式
    thisDoc1 = array(setOfWords2Vec(myVocabList, testEntry1))
    print(testEntry1, 'classified as:', classifyNB(thisDoc1, p0V, p1V, pAb))

# -----------------------------------------------垃圾邮件过滤-----------------------------------------------------------
# 处理数据长字符串
def testParse(bigString):
    listOfTokens = re.split(r'\W*',bigString)
    return [tok.lower() for tok in listOfTokens if len(tok)>2]

def spanTest():
    docList = [];classList = [];fullList = []
# 1,导入并解析文本文件
    for i in range(1,26):
        wordList = testParse(open('email/spam/%d.txt'%i).read())
        # print wordList
        docList.append(wordList)
        fullList.extend(wordList)
        classList.append(1)
        wordList = testParse(open('email/ham/%d.txt'%i).read())
        docList.append(wordList)
        fullList.extend(wordList)
        classList.append(0)
    # 构成无重复的字符串
    vocabList = createVocabList(docList)
#2，随机构建训练集
    trainingSet = range(50);testSet = []
    # 从50个中随机选出10个作为索引，构建测试集 testSet
    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
#3，算出先验概率等
    trainMat = [];trainClasses = []
    for docIndex in trainingSet:
        # 转换为词条向量，然后添加到训练矩阵中
        # a = docList[docIndex]
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
# 4，对测试集分类
    for docIndex in testSet:
        # 转换为词条向量
        wordVector = setOfWords2Vec(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam)!=classList[docIndex]:
            errorCount += 1
    print ('the error rate is: ',float(errorCount)/len(testSet))

# --------------------------------------从广告中获取区域倾向-----------------------------------------------------------
# RSS源分类器、获取高频词
def calMostFreq(vocabList,fullTest):
    import operator
    freqDict = {}
    for token in vocabList:
        #key---V:单词---个数
        freqDict[token] = fullTest.count(token)
    #按照value进行排序
    sortFreq = sorted(freqDict.items(),key=operator.itemgetter(1),reverse=True)
    return sortFreq[:30]

def localWords(feed1,feed0):
    #获取数据
    docList=[];classList=[];fullList=[]
    minLen=min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen):
        wordList = testParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullList.extend(wordList)
        classList.append(1)
        wordList = testParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullList.extend(wordList)
        classList.append(0)
    #删除高频词，降低错误率
    vocabList = createVocabList(docList)
    top30Words = calMostFreq(vocabList,fullList)
    for pairW in top30Words:
        if pairW[0] in vocabList:
            vocabList.remove(pairW[0])
    #开始交叉验证的训练和测试
    trainingSet = range(2*minLen);testSet = []
    for i in range(20):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        # del(trainingSet[randIndex])

    trainMat=[];trainClasses=[]
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0

    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
    print('the error rate is :',float(errorCount)/len(testSet))
    return  vocabList,p0V,p1V

# 最具表征性的词汇显示函数
def getTopWords(ny,sf):
    vocabList,p0V,p1V=localWords(ny,sf)
    topNY=[];topSF=[]
    for i in range(len(p0V)):
        if p0V[i]>-6.0:topSF.append((vocabList[i],p0V[i]))
        if p1V[i]>-6.0:topNY.append((vocabList[i],p1V[i]))
    sortedSF=sorted(topSF,key=lambda pair:pair[1],reverse=True)
    print "SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**"
    for item in sortedSF:
        print item[0]
    sortedNY=sorted(topNY,key=lambda pair:pair[1],reverse=True)
    print "NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**"
    for item in sortedNY:
        print item[0]

if __name__ == '__main__':
    # spanTest()
    ny = feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
    sy = feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
    vocabList, pSF, pNY = localWords(ny, sy)
