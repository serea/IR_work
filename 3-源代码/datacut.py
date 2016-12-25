# -*- coding: utf-8 -*-
import xlrd

#功能：切割训练集或者收集所有数据，视情况修改代码即可
def cuttrainandall():
    xlsdata = xlrd.open_workbook(u'爬虫数据V2.0.xlsx','r')

    category = []
    caijingdt = xlsdata.sheet_by_index(0)
    caijing = []
    ncount = 1
    for i in range(1,caijingdt.nrows-1):
        news = caijingdt.row_values(i)
        if news[3] == '':
            continue
        caijing.append([news[2], news[3]])
        category.append(1)
        ncount = ncount+1
        if ncount>800:
            break
    print len(caijing)

    kejidt = xlsdata.sheet_by_index(1)
    keji = []
    ncount = 1
    for i in range(1,kejidt.nrows-1):
        news = kejidt.row_values(i)
        if news[3] == '':
            continue
        keji.append([news[2], news[3]])
        category.append(2)
        ncount = ncount+1
        if ncount>800:
            break
    print len(keji)

    qichedt = xlsdata.sheet_by_index(2)
    qiche = []
    ncount = 1
    for i in range(1,qichedt.nrows-1):
        news = qichedt.row_values(i)
        if news[3] == '':
            continue
        qiche.append([news[2], news[3]])
        category.append(3)
        ncount = ncount+1
        if ncount>800:
            break
    print len(qiche)

    fangchandt = xlsdata.sheet_by_index(5)
    fangchan = []
    ncount = 1
    for i in range(1,fangchandt.nrows-1):
        news = fangchandt.row_values(i)
        if news[3] == '':
            continue
        fangchan.append([news[2], news[3]])
        category.append(4)
        ncount = ncount+1
        if ncount>800:
            break
    print len(fangchan)

    tiyudt = xlsdata.sheet_by_index(6)
    tiyu = []
    ncount = 1
    for i in range(1,tiyudt.nrows-1):
        news = tiyudt.row_values(i)
        if news[3] == '':
            continue
        tiyu.append([news[2], news[3]])
        category.append(5)
        ncount = ncount+1
        if ncount>800:
            break
    print len(tiyu)

    yuledt = xlsdata.sheet_by_index(3)
    yule = []
    ncount = 1
    for i in range(1,yuledt.nrows-1):
        news = yuledt.row_values(i)
        if news[3] == '':
            continue
        yule.append([news[2], news[3]])
        category.append(6)
        ncount = ncount+1
        if ncount>800:
            break
    print len(yule)

    qitadt = xlsdata.sheet_by_index(4)
    qita = []
    ncount = 1
    for i in range(1,qitadt.nrows-1):
        news = qitadt.row_values(i)
        if news[3] == '':
            continue
        qita.append([news[2], news[3]])
        category.append(7)
        ncount = ncount+1
        if ncount>800:
            break
    print len(qita)

    full = caijing
    full.extend(keji)
    full.extend(qiche)
    full.extend(fangchan)
    full.extend(tiyu)
    full.extend(yule)
    full.extend(qita)

    print len(full)
    wf = open('alldata.txt','w')
    count = 0
    for index,enews in enumerate(full):
        count = count+1
        wstr = str(count)+'\t'+str(category[index])+'\t'+enews[0]+'\t'+enews[1]+'\n'
        wf.write(wstr.encode("UTF-8"))

    wf.close()
    print 'finish!'

#功能：从所有数据alldata.txt中切割测试集
def cuttest():
    f = open('alldata.txt')
    newslist = f.readlines()

    newstext=[[],[],[],[],[],[],[]]
    for news in newslist:
        textlist = news.strip(' ').split('\t')
        (newstext[int(textlist[1])-1]).append([textlist[2],textlist[3]])

    f.close()

    testdata=[]
    category=[]
    testdata.extend(newstext[0][800:])
    category.extend([1 for i in range(800, len(newstext[0]))])
    print len(newstext[0])
    testdata.extend(newstext[1][800:])
    category.extend([2 for i in range(800, len(newstext[1]))])
    print len(newstext[1])
    testdata.extend(newstext[2][800:])
    category.extend([3 for i in range(800, len(newstext[2]))])
    print len(newstext[2])
    testdata.extend(newstext[3][800:])
    category.extend([4 for i in range(800, len(newstext[3]))])
    print len(newstext[3])
    testdata.extend(newstext[4][800:])
    category.extend([5 for i in range(800, len(newstext[4]))])
    print len(newstext[4])
    testdata.extend(newstext[5][800:])
    category.extend([6 for i in range(800, len(newstext[5]))])
    print len(newstext[5])
    testdata.extend(newstext[6][800:])
    category.extend([7 for i in range(800, len(newstext[6]))])
    print len(newstext[6])
    print len(testdata)
    print len(category)

    count = 0
    wf = open('testdata.txt','w')
    for index,enews in enumerate(testdata):
        count = count+1
        wstr = str(count)+'\t'+str(category[index])+'\t'+enews[0]+'\t'+enews[1]
        wf.write(wstr)
    wf.close()
    print 'finish!'