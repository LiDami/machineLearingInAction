# -*- coding:utf8 -*-

from numpy import *
import operator
from os import listdir

def createDataSet():
	group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
	labels = ['B','B','A','A']
	return group,labels

def classify0(inX,dataSet,labels,k):
	# 距离计算
	#把行数赋值给dataSetSize
	dataSetSize = dataSet.shape[0]
	# （dataSetSize,1)为要产生的矩阵的行列大小
	# tile函数把inX矩阵复制成dataSetSize行1列，这里就是重复四次，与训练好的四行进行相减操作。然后与训练好的样本集求差
	#>>> a = np.array([0, 1, 2])
    #>>> np.tile(a, 2)
    #array([0, 1, 2, 0, 1, 2])
    #>>> np.tile(a, (2, 2))
    #array([[0, 1, 2, 0, 1, 2],
    #      [0, 1, 2, 0, 1, 2]])

	diffMat = tile(inX,(dataSetSize,1)) - dataSet
	sqDiffMat = diffMat ** 2
	#每行求和
	sqDistances = sqDiffMat.sum(axis =1)
	distances = sqDistances ** 0.5
	sortedDistIndicies = distances.argsort()
	classCount = {}
# 选择距离最小的K点
	for i in range(k):
		#获得训练好的样本对应的label
		voteIlabel = labels[sortedDistIndicies[i]]
		##加一，在该标签上计数加一，循环计算前k个最近距离里各个标签（类别）分别有多少个
		classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
     #    排序。。。。classCount.iteritems()把字典分解为元组列表
     #   key = operator.itemgetter(1),导入运算符模块的itemgetter方法，使用第几个元素排序
	# 	排序，翻转，逆排序。。。对个数label进行从大到小排序，返回最多的就是
	sortedClassCount = sorted(classCount.iteritems(),key = operator.itemgetter(1),reverse = True)
	# 返回排名第一的最多个数的那个类的标签
	return sortedClassCount[0][0]

# group,labels = createDataSet()
# print classify0([0.5,0.9],group,labels,3)

############
########### 把文本记录转换为numpy的解析程序
#############
def file2matrix(filename):
	fr = open(filename)
	arrayOLines = fr.readlines()
	numberOfLines = len(arrayOLines) #得到文件行数
	returnMat = zeros((numberOfLines,3)) #创建返回的numpy矩阵...返回zeros(行，列)
	classLabelVector = []
	index = 0
	for line in arrayOLines:
		line = line.strip() # 截掉所有的回车字符，然后使用tab \t 字符将得到的整行数据分割为一个列表
		listFromLine = line.split('\t')
		returnMat[index,:] = listFromLine[0:3] #存储前三列
		classLabelVector.append(int(listFromLine[-1])) #把labels存储最后一列到数组中
		index+=1
		#返回前三列的数据矩阵，和标签labels
	return returnMat,classLabelVector

datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
# print datingDataMat ,datingLabels[0:20]

#########
########使用matplotlib绘制散点图
#########
import matplotlib
import  matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(121) #(总行，总列，位置)。。就是这个图显示在整个画布的位置。如add_subplot(3,3,4).就是在三行三列的第四个小块位置
#使用了矩阵中的第二第三列的数据作为横纵坐标创建散点图scatter
ax.scatter(datingDataMat[:,1],datingDataMat[:,2],15.0*array(datingLabels),15.0*array(datingLabels))
plt.xlabel('Playing games times percentage')
plt.ylabel('Eating ice cream kilo')

#这个是每年飞行里数与玩游戏时间的散点图
ax1 = fig.add_subplot(122)
ax1.scatter(datingDataMat[:,0],datingDataMat[:,1],15.0*array(datingLabels),15.0*array(datingLabels))
plt.xlabel('Flying kilo each year')
plt.ylabel('Playing games times percentage')

plt.show()

#######
#######  为了不让飞行里程这一列影响太大，都把所有的数值归为[0,1]之间表示，即叫做归一化数值.公式：newVal = (oldVal-min)/(max-min)
#######
def autoNorm(dataSet):
	#选出每列的最大值最小值
	minVals = dataSet.min(0)
	maxVals = dataSet.max(0)
	#这个是分母
	ranges = maxVals - minVals
	#获取矩阵
	normDataSet = zeros(shape(dataSet))
	#获取行
	m = dataSet.shape[0]
	normDataSet = dataSet - tile(minVals,(m,1))
	normDataSet = normDataSet/tile(maxVals,(m,1))
	return normDataSet,ranges,minVals

#测试归一化结果
normMat,ranges,minVals = autoNorm(datingDataMat)
# print normMat,ranges,minVals

###########
############ 取数据中的10%进行测试分类器，算出错误率
###########
def datingClassTest():
	index = 0.10
	datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
	normMat,ranges,minVals = autoNorm(datingDataMat)
	m = normMat.shape[0]
	#获取10%的样本
	numTest = int(m*index)
	errorCount = 0.0
	for i in range(numTest):
		classifierResult = classify0(normMat[i,:],normMat[numTest:m,:],datingLabels[numTest:m],3)
		print  "The classifier %d,the real answer %d"%(classifierResult,datingLabels[i])
		#如果结果不一致，变量增加
		if(classifierResult != datingLabels[i]):errorCount +=1.0
		#打印错误率
	print  "The total error rate is :%f"%(errorCount/float(numTest))

##########
###########  开始使用算法
##########
def classifyPerson():
	resultList = ['not at all','in small doses','in large doses']
	percentTats = float(raw_input('percentage of time spent playing video games?'))
	ffMiles = float(raw_input("frequent flier miles earned per year?"))
	iceCream = float(raw_input('liters of ice cream consumed per pear?'))

	datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
	normMat,ranges,minvals = autoNorm(datingDataMat)
	inArr = array([ffMiles,percentTats,iceCream])
	#开始进入算法中
	classifierResult = classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
	print "You will probably like this person: ",resultList[classifierResult - 1]

###################################### 这里是手写识别  #########################################################

#####
###### 这个函数把每一个图都变为一行的向量，因为是32*32.所以是1024列，1行。
#####
def img2vector(filename):
	returnVect = zeros((1,1024))
	fr = open(filename)
	for i in range(32):
		#读取总行数
		lineStr = fr.readline()
		for j in range(32):
			#这里读取j行写入32*i+j列中
			returnVect[0,32*i+j] = int(lineStr[j])
	return returnVect


########
######### 测试算法
########
def handwritingClassTest():
	# 定义标签数组
	hwlabels = []
	#列出这个目录下的文件名
	trainingFileList = listdir('trainingDigits')
	m = len(trainingFileList)
	trainingMat = zeros((m,1024))
	for i in range(m):
		#获取文件名
		fileNameStr = trainingFileList[i]
		#切除...split分隔后是一个列表，[0]表示取其第一个元素
		fileStr = fileNameStr.split('.')[0]
		classNumStr = int(fileStr.split('_')[0])
		#切除后只保留了前面的数字，就是对应的label，存入进去
		hwlabels.append(classNumStr)
		trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)

		#开始进行测试数据集
	testFileList = listdir('testDigits')
	errorCount = 0
	mTest = len(testFileList)
	for i in range(mTest):
		fileNameStr = testFileList[i]
		fileStr = fileNameStr.split('.')[0]
		classNumStr = int(fileStr.split('_')[0])
		vectorUnderTest = img2vector('testDigits/%s' %fileNameStr)
		#开始算距离
		classifierResult = classify0(vectorUnderTest,trainingMat,hwlabels,3)
		print 'The classifier came back:%d ,the real answer is:%d' %(classifierResult,classNumStr)

		if(classifierResult != classNumStr):errorCount += 1.0
	print '\n the total number of errors is: %d'%errorCount
	print '\n the total error rate is:%f'%(errorCount/float(mTest))









