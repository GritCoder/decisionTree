# _*_ coding:utf-8 _*_
from math import log
import operator
def calc_entropy(dataSet):#计算整个数据集的熵
    numEntries = len(dataSet)#数据集中实例个数
    labelCounts = {}#标签集
    for item in dataSet:
        currentLabel = item[-1]#获取标签
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0#标签不在标签集中，出现次数为0
        labelCounts[currentLabel] += 1#在标签集中，出现次数加1
    entropy = 0.0 #初始化熵为0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries  #计算某个类别出现的次数
        entropy -= prob * log(prob,2) #计算熵
    return entropy
def splitDataSet(dataset,axis,value):#划分数据集 参数是数据集、特征、特征对应的值
    retDataSet = []
    for item in dataset:
        if item[axis] == value: #理解划分数据集的含义，按照某个特征来进行划分，即在这个数据集中去掉这个特征(即去掉该列)
            reduceItem = item[:axis] #得到剩余的数据集部分
            reduceItem.extend(item[axis+1:]) #若明白这个道理，则此处代码则就很好理解了
            retDataSet.append(reduceItem)
    return retDataSet
def chooseBestFeatureToSplit(dataset):
    numFeatures = len(dataset[0])-1 #获取特征的个数
    baseEntropy = calc_entropy(dataset) #计算原始数据集的特征
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        itemList = [example[i] for example in dataset]
        #print(itemList)
        uniqueVal = set(itemList) #获得特征的取值个数(种类)
        #print(uniqueVal)
        newEntropy = 0.0
        for value in uniqueVal:
            subDataSet = splitDataSet(dataset,i,value)
            prob = len(subDataSet)/float(len(dataset))
            newEntropy += prob * calc_entropy(subDataSet)
            infoGain = baseEntropy - newEntropy
            if (infoGain > bestInfoGain):
                bestInfoGain = infoGain
                bestFeature = i
    return bestFeature #返回最佳特征划分的索引值
def majorityCnt(classList):#当类标签还是不能确定时，采用多数表决法
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)#字典逆序排序
    return sortedClassCount[0][0]#返回最大值，作为投票的依据
def createTree(dataset,labels): #递归构建决策树
    classList = [example[-1] for example in dataset]#得到类别的集合
    if classList.count(classList[0]) == len(classList):#类别完全相同 不用划分
        return classList[0]
    if len(dataset[0]) == 1: #遍历完所有特征，返回出现类别最多的类别 （严格来说并不是结束的条件 而是采用多数表决法返回，看了很多个博客基本都是这么理解的）
        return majorityCnt(classList)#机器学习实战上面解释作为另一个递归结束的条件 理解起来有点牵强
    bestFeature = chooseBestFeatureToSplit(dataset)
    bestFeatureLabel = labels[bestFeature]
    myTree = {bestFeatureLabel:{}} #用字典存储划分的树结构信息
    del(labels[bestFeature]) #删除已经用来分类过的特征
    featureVal = [example[bestFeature] for example in dataset]
    uniqueVal = set(featureVal)
    for value in uniqueVal:
        subLabels = labels[:]
        myTree[bestFeatureLabel][value] = createTree(splitDataSet(dataset,bestFeature,value),subLabels)
    return myTree
def classify(inputTree,labels,testVec):
    firstStr = list(inputTree.keys())[0]#获取第一个节点的键
    secondDict = inputTree[firstStr]#获取第一个节点的值
    labelIndex = labels.index(firstStr)#获取第一个键在标签集合中的索引值，算是开始匹配的一个切入点
    for key in secondDict.keys():#键即为分类标签
        if testVec[labelIndex] == key:#判断是否属于某个类标签
            if type(secondDict[key]).__name__ == "dict":#若满足上个条件之后，仍然不是叶子节点 则进行递归调用来分类
                classLabel = classify(secondDict[key],labels,testVec)
            else:
                classLabel = secondDict[key]#此时为叶子节点了 键的值即为最终的分类结果  这两点需要理解
    return classLabel #返回分类结果
def storeTree(inputTree,filename):
    import pickle #pickle模块是对Python对象结构进行二进制序列化和反序列化的协议实现，简单说就是把Python数据变成流的形式。
    fw = open(filename,"wb")#本质上是方便文件的读写
    pickle.dump(inputTree,fw)  #用于序列化的两个模块 #json：用于字符串和Python数据类型间进行转换
    fw.close()               #pickle: 用于python特有的类型和python的数据类型间进行转换
def grabTree(filename):#反序列化
    import pickle
    fr = open(filename,"rb") #一定要注意rb wb这种方式 否则会报编码相关的错
    return pickle.load(fr)
#def predict_eye():

if __name__ == "__main__":
    dataset = [ #这里仅作为演示,实际的数据集可能从数据库或者文件中读入
        [1,1,'yes'],
        [1,1,'yes'],
        [1,0,'no'],
        [0,1,'no'],
        [0,1,'no']
    ]
    Labels = ['no_surfacing','flippers']
    #result = calc_entropy(dataset)  #输入的数据集必须符合算法的要求（即是格式化过的才可以）
    #print(result)#熵越高，则表明混合的数据越多
    # dataset[0][-1] = 'maybe'
    # result  calc_entropy(dataset)
    # print(r=esult)
    #res = splitDataSet(dataset,0,1)
    #print(res)
    #bestFeature = chooseBestFeatureToSplit(dataset)
    #print(bestFeature)
    myTree = createTree(dataset,Labels)
    #print(myTree)
    classLabel = classify(myTree,['no_surfacing','flippers'],[1,0])#测试分类树 #注：如果第二个参数传入Labels 则程序报错，传入其值则正确
    #print(classLabel)                                                #这个细节还有待解决 可能是引用与值传递的细节问题
    storeTree(myTree,"classifyStorage.txt")
    #print(grabTree("classifyStorage.txt"))
    fr = open("lenses.txt")#读取测试集文件
    #print(fr.read())
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]#从文件中获得数据集
    #print(lenses)
    lensesLabel = ['age','prescript','astimatic','tearRate']
    lensesTree = createTree(lenses,lensesLabel)
    #print(lensesTree)
    print(classify(lensesTree,['age','prescript','astimatic','tearRate'],['young', 'myope', 'no', 'reduced']))

