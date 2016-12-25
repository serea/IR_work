# -*- coding: utf-8 -*-
import jieba
import itertools
import collections
import math
import codecs

#输入：ASCII或UNICODE字符串
#功能：判断字符串是否是数值（整数、浮点数、负数等）
#输出：如果是数值则输出True，否则输出False
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

#输入：新闻文本字符串
#功能：对文本分词，去除符号和长度为1的词
#输出：分词列表
def tokentext(textstr):
    wordgenerator=jieba.cut(textstr)
    prewordlist=list(iter(wordgenerator))

    #我们认为单个词符号或者是无意义的
    wordlist=[]
    for word in prewordlist:
        if is_number(word):
            continue
        if len(word)>1:
            #单个词的长度肯定为1，符号在分词时也是单独分的，所以长度也必然为1
            wordlist.append(word)

    return wordlist

#######################
#以下为bayes相关
#######################

#输入：存储条件概率的文件名，默认为文件conprob.txt
#功能：快速初始化贝叶斯模型，生成条件概率字典
#输出：条件概率字典conprob,键-值形如 u'鹿角胶':tuple(0.25,0.25,0.25,0.25,0.25,0.25,0.75)
def bayesfastinitial(conprobname = 'conprob.txt'):
    f = codecs.open(conprobname, encoding='utf-8')
    lines = f.readlines()

    conprob = {}
    for line in lines:
        line = line.strip('\n')
        llist = line.split('\t')
        word = (llist[0]).strip()
        prob = tuple([float(item) for item in llist[1:]])
        conprob[word] = prob

    f.close()
    #print '快速初始化完成！'
    return conprob

#输入：新闻内容，条件概率字典（通过调用初始化函数获得）
#功能：贝叶斯分类
#输出：分类结果字典，键为类别编号，值为属于该类别的概率
def bayes(textstring, conprob):
    tsset = set(tokentext(textstring))
    res = {1:0,2:0,3:0,4:0,5:0,6:0,7:0}
    wordset = set(conprob.keys())
    for i in range(len(res)):
        prob = 0
        sameset = tsset&wordset
        for word in list(sameset):
            prob += conprob[word][i]
        res[i+1] = prob

    return sorted(res.iteritems(),key=lambda d:d[1],reverse=True)

#输入：文件名，该文件为某一篇新闻的新闻内容字符串
#功能：对输入的新闻使用bayes分类
#输出：打印分类结果
def bayestestonefile(filename):
    f = open(filename)
    content = f.read().strip()
    conprob = bayesfastinitial()
    catedict = bayes(content, conprob)
    print catedict

#输入：测试数据集文件名
#功能：使用贝叶斯模型测试测试数据集
#输出：打印分类结果
def bayestest(filename):
    f = open(filename)
    conlist = f.readlines()
    true = []
    predict = []

    conprob = bayesfastinitial()

    for news in conlist:
        textlist = news.strip('\n').split('\t')
        true.append(int(textlist[1]))
        content = textlist[3]
        prekind = bayes(content, conprob)
        predict.append(prekind[0][0])

    count = 0
    res = []
    for i in range(len(true)):
        if true[i]==predict[i]:
            count+=1
            res.append(true[i])

    P = float(count)/len(true)
    print "总准确率："+str(P)
    truedict = dict(collections.Counter(true))
    resdict = {1:0,2:0,3:0,4:0,5:0,6:0,7:0}
    resdict.update(dict(collections.Counter(res)))
    print "财经："+str(float(resdict[1])/truedict[1])
    print "科技："+str(float(resdict[2])/truedict[2])
    print "汽车："+str(float(resdict[3])/truedict[3])
    print "房产："+str(float(resdict[4])/truedict[4])
    print "体育："+str(float(resdict[5])/truedict[5])
    print "娱乐："+str(float(resdict[6])/truedict[6])
    print "其他："+str(float(resdict[7])/truedict[7])

#######################
#以下为kNN相关
#######################

#输入：文本字符串
#功能：计算文本的tf向量表示，进行了归一化
#输出：tf:字典形式
def textcal(textstring):
    wordlist = tokentext(textstring)
    tf = dict(collections.Counter(wordlist))
    total = math.sqrt(sum([x*x for x in tf.values()]))
    for key in tf.keys():
        tf[key] = tf[key]/total

    return tf

#输入：默认文件tfidf.txt
#功能：kNN初始化，导入所有训练文档的tfidf向量
#输出：tfidf:列表，元素为字典，每个文档对应一个字典
#      category:列表，类别标签
def kNNinitial(tfidfname = 'tfidf.txt'):
    tfidf = []
    tdnum = []
    category = []

    f = open(tfidfname)
    tdlist = f.readlines()

    for eachlist in tdlist:
        textlist = eachlist.strip('\n').split('\t')
        tdnum.append(int(textlist[0]))
        category.append(int(textlist[1]))
        keys = []
        values = []
        for wordvalue in textlist[2:]:
            wl = wordvalue.split(',')
            keys.append(wl[0])
            values.append(float(wl[1]))
        tfidf.append(dict(zip(keys,values)))

    f.close()

    return tfidf,category

#输入：文本字符串、tfidf列表，类别标签列表、参数N
#功能：使用kNN预测
#输出：catedict:列表，元素为元组，元组第一个值为类别标签，第二个值为排序后的前N个最相似文档中属于该类别的文档数量；注意该列表已经按照元组的第二个值从大到小进行排序
def kNN(textstring, tfidf, category, N):
    strtf = textcal(textstring)
    strwset = set(strtf.keys())
    result = {}#键为序号，值为余弦相似度

    for index,td in enumerate(tfidf):
        tdwset = set(td.keys())
        sameset = strwset&tdwset
        cos = 0
        for word in list(sameset):
            cos = cos+strtf[word]*td[word]
        result[index] = cos

    result = sorted(result.iteritems(),key=lambda d:d[1],reverse=True)

    Nres = result[:N]
    catedict = {1:0,2:0,3:0,4:0,5:0,6:0,7:0}
    for ele in Nres:
        catedict[category[ele[0]]] += 1

    catedict = sorted(catedict.iteritems(),key=lambda d:d[1],reverse=True)

    return catedict

#输入：文件名，该文件为某一篇新闻的新闻内容字符串，N为kNN模型的参数，默认为25
#功能：对输入的新闻使用kNN分类
#输出：打印分类结果
def kNNtestonefile(filename, N=25):
    f = open(filename)
    content = f.read().strip()
    tfidf,category = kNNinitial()
    catedict = kNN(content, tfidf, category, N)
    print catedict

#输入：测试数据集文件名，参数N默认为25
#功能：使用kNN测试测试数据集
#输出：打印分类结果
def kNNtest(filename, N = 25):
    #使用测试文件
    f = open(filename)
    conlist = f.readlines()
    true = []
    predict = []

    tfidf,category = kNNinitial()
    for news in conlist:
        textlist = news.strip('\n').split('\t')
        true.append(int(textlist[1]))
        content = textlist[3]
        prekind = kNN(content, tfidf, category, N)
        predict.append(prekind[0][0])

    count = 0
    res = []
    for i in range(len(true)):
        if true[i]==predict[i]:
            count+=1
            res.append(true[i])

    P = float(count)/len(true)
    print "总准确率："+str(P)
    truedict = dict(collections.Counter(true))
    resdict = {1:0,2:0,3:0,4:0,5:0,6:0,7:0}
    resdict.update(dict(collections.Counter(res)))
    print "财经："+str(float(resdict[1])/truedict[1])
    print "科技："+str(float(resdict[2])/truedict[2])
    print "汽车："+str(float(resdict[3])/truedict[3])
    print "房产："+str(float(resdict[4])/truedict[4])
    print "体育："+str(float(resdict[5])/truedict[5])
    print "娱乐："+str(float(resdict[6])/truedict[6])
    print "其他："+str(float(resdict[7])/truedict[7])