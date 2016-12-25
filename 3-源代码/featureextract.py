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

##############
#tfidf相关
##############

#输入：文档词条列表，每个元素为一个文档的未去重列表
#功能：计算每个文档中每个单词的词项频率
#输出：tf列表，元素为字典，每个文档对应一个字典，该字典表示该文档的所有单词的tf
def caltf(fullwordlist):
    tf = []
    for wordlistlist in fullwordlist:
        for wordlist in wordlistlist:
            tf.append(dict(collections.Counter(wordlist)))

    return tf

#输入：文档词条列表，每个元素为一个文本的未去重词条列表
#功能：计算指定文档集合里的df
#输出：df:文档频率，既可以是所有文档集中的文档频率，也可以是某一类别文档集中的文档频率
def caldf(fullwordlist):
    df={}

    for wordlist in fullwordlist:
        dwset = set(wordlist)
        keyset = set(df.keys())
        sameset = keyset&dwset
        diffset = dwset-keyset    #不是所有不相同的元素，而是求差集，否则结果错误
        samedict = dict(zip(list(sameset),[df[list(sameset)[i]]+1 for i in range(len(list(sameset)))]))
        diffdict = {}.fromkeys(list(diffset),1)
        df.update(samedict)
        df.update(diffdict)
        #print df

    return df

#输入：类别文档频率mdf，全局文档频率ndf
#功能：计算每一类文档中各个词条的改进的idf权重,idf=log{N*(m/n)*(m/(n-m+1))}
#输出：每个元素为该类别中的词条的权重列表，按权重由大到小排列，元素为元组，元组的第一个元素单词，第二个元素表示该单词在该类别中的权重
def calidf(mdf, ndf):
    idf = []
    N = 5600
    for eachinmdf in mdf:
        eachdict = {}
        for word in eachinmdf.keys():
            n = ndf[word]
            m = eachinmdf[word]
            idf = math.log10((m*N/n)*(float(m)/abs(n-m+1)))
            eachdict[word] = idf
        sortedtuplelist = sorted(eachdict.iteritems(),key=lambda d:d[1],reverse=True)
        idf.append(sortedtuplelist)

    return idf

#输入：tf（一篇文档对应一个字典）,category为类别标签，idf为每个类别的各个词条的idf权重
#功能：计算每篇文档的tf-idf权重向量
#输出：返回tf-idf权重向量字典列表
def caltfidf(tf, category, idf):
    num = len(tf)
    tfidf = []

    idfdict = []
    for eachidf in idf:
        keys = [item[0] for item in eachidf]
        value = [item[1] for item in eachidf]
        idfdict.append(dict(zip(keys, value)))

    for i,tfdict in enumerate(tf):
        cate = category[i]
        cateidf = idfdict[cate-1]
        doc = {}
        for key in list(set(tfdict.keys())&set(cateidf.keys())):
            doc[key] = tfdict[key] * cateidf[key]
        tfidf.append(doc)

    return tfidf


#输入：tf（一篇文档对应一个字典）,category(类别标签),ndf,默认文件名为tf.txt
#功能：将tf写入文件，每一行格式为 文档编号+'\t'+'\t'.join(','.join([单词 在该文档中出现的次数（按从大到小排列）]))
#输出：无
def writetf(tf, category, ndf, tfname = 'tf.txt'):
    f = open(tfname,'w')
    wordset = set(ndf.keys())

    for index,tdict in enumerate(tf):
        wstr = str(index+1)+ '\t' + str(category[index])
        samelist = list(wordset&set(tdict.keys()))
        for item in sorted(tdict.iteritems(),key=lambda d:d[1],reverse=True):
            if item[0] not in samelist:
                continue
            wstr = wstr + '\t'+ item[0] + ',' + str(item[1])
        wstr += '\n'
        f.write(wstr.encode("UTF-8"))

    f.close()
    print 'finish!'

#输入：ndf,默认文件名为ndf.txt
#功能：将全局文档频率ndf写入文件中，每行格式为 单词+'\t'+该单词的全局文档次数
#输出：无
def writendf(ndf, ndfname = 'ndf.txt'):
    f = open(ndfname, 'w')

    for item in sorted(ndf.iteritems(),key=lambda d:d[1],reverse=True):
        wstr = item[0] + '\t' + str(item[1]) + '\n'
        f.write(wstr.encode("UTF-8"))

    f.close()
    print 'finish!'

#输入：mdf,默认文件名为mdf.txt
#功能：将局部类别文档频率mdf写入文件中，每行格式为 类别+'\t'+'\t'.join(','.join([单词 该单词在该类别中的文档频率]))
#输出：无
def writemdf(mdf, mdfname = 'mdf.txt'):
    f = open(mdfname, 'w')

    for i in range(len(mdf)):
        wstr = str(i+1)
        for item in mdf[i]:
            wstr = wstr + '\t'+ item[0] + ',' + str(item[1])
        wstr += '\n'
        f.write(wstr.encode("UTF-8"))

    f.close()
    print 'finish!'

#输入：已排好序的idf
#功能：将各个类别的idf写入对应文件中
#输出：无
def writeidf(idf):
    for i in range(len(idf)):
        filename = 'idf{0}.txt'.format(i+1)
        f = open(filename, 'w')
        for item in idf[i]:
            wstr = item[0] + '\t' + str(item[1]) + '\n'
            f.write(wstr.encode('UTF-8'))
        f.close()

    print 'finish!'

#输入：tfidf
#功能：写入对应文件tfidf.txt中
#输出：无
def writetfidf(tfidf, category, tidname='tfidf.txt'):
    f = open(tidname, 'w')

    for index, tddict in enumerate(tfidf):
        cate = category[index]
        wstr = str(index+1)+'\t'+str(cate)
        for key in tddict.keys():
            wstr += '\t'+key+','+str(tddict[key])
        wstr += '\n'
        f.write(wstr)

    f.close()

##############
#IG相关
##############

#输入：默认文件tf.txt,ndf.txt,mdf.txt
#功能：加载tf,ndf,mdf,category
#输出：tf,ndf,mdf,category
def loadtfdf(tfname='tf.txt', ndfname='ndf.txt', mdfname='mdf.txt'):
    ftf = open(tfname)
    ctf = ftf.readlines()
    tf = []
    category = []
    for line in ctf:
        e = line.strip('\n').split('\t')
        cate = int(e[1])
        category.append(cate)
        tfdict = {}
        for item in e[2:]:
            etf = item.split(',')
            tfdict[etf[0]] = int(etf[1])
        tf.append(tfdict)
    ftf.close()

    fndf = open(ndfname)
    ndf = {}
    cndf = fndf.readlines()
    for line in cndf:
        e = line.strip('\n').split('\t')
        ndf[e[0]] = int(e[1])
    fndf.close()

    fmdf = open(mdfname)
    mdf = [{},{},{},{},{},{},{}]
    cmdf = fmdf.readlines()
    for line in cmdf:
        e = line.strip('\n').split('\t')
        cate = int(e[0])
        for item in e[1:]:
            etf = item.split(',')
            mdf[cate-1][etf[0]] = int(etf[1])
    fmdf.close()
    print 'finish!'
    return tf, category, ndf, mdf

#输入：词条列表，ndf,mdf,category
#功能：将计算信息增益和条件概率
#输出：已排好序的信息增益列表和条件概率
def calsimpleIG(wordlist, ndf, mdf, category):
    IG = [{},{},{},{},{},{},{}]
    Nall = len(category)
    catedict = dict(collections.Counter(category))
    pc = []
    for i in range(len(mdf)):
        pc.append(catedict[i+1]/float(Nall))

    pt10 = []
    for word in wordlist:
        pt1 = ndf[word]/float(Nall)
        pt0 = 1-pt1
        cprob = []
        for i in range(len(mdf)):
            if not (mdf[i]).has_key(word):
                m = 0
            else:
                m = mdf[i][word]

            pi1t1 = (m+1)/float(ndf[word]+2)
            pi0t1 = (ndf[word]-m+1)/float(ndf[word]+2)
            pi1t0 = (Nall-ndf[word]-catedict[i+1]+m+1)/float(Nall-ndf[word]+2)
            pi0t0 = (catedict[i+1]-m+1)/float(Nall-ndf[word]+2)
            IG[i][word] = pt1*(pi1t1*math.log(pi1t1)+pi0t1*math.log(pi0t1))+pt0*(pi1t0*math.log(pi1t0)+pi0t0*math.log(pi0t0))-pc[i]*math.log(pc[i])
            cprob.append(pi1t1)
        pt10.append(cprob)
    print 'finish!'
    return [sorted(ig.iteritems(),key=lambda d:d[1],reverse=True) for ig in IG],pt10

#输入：无
#功能：将每种类别中的每个词条的条件概率写入文件conprob.txt中
#输出：无
def writeconprob():
    tf, category, ndf, mdf = loadtfdf('tf.txt', 'ndf.txt', 'mdf.txt')
    print '加载tf,ndf,mdf完毕！'
    wordlist = ndf.keys()
    IG,pt10 = calsimpleIG(wordlist, ndf, mdf, category)
    print '计算条件概率和信息增益完毕'

    wordvect = [item[0] for ig in IG for item in ig[:15000]]
    wordset = set(wordvect)
    fi = open('conprob.txt','w')
    count = 0
    for word in list(wordset):
        if is_number(word):
            continue
        wordindex = wordlist.index(word)
        wstr = word+'\t'+'\t'.join([str(prob) for prob in pt10[wordindex]])
        wstr += '\n'
        fi.write(wstr)
        count += 1

    fi.close()
    print 'finish!'