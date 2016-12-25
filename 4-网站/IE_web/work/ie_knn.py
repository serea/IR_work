#coding:utf-8
import textclassify
def answer(d_context):

    answer_list={1:'财经',2:'科技',3:'汽车',4:'房产',5:'体育',6:'娱乐',7:'其他'}
    true = []
    predict = []
    # tfidf,category = textclassify.initial()
    prekind = textclassify.kNN(d_context, tfidf, category, 25)
    return prekind
    #return answer_list[prekind[0][0]]
    # predict.append(prekind[0][0])
    #
    # count = 0
    # res = []
    # for i in range(len(true)):
    #     if true[i]==predict[i]:
    #         count+=1
    #         res.append(true[i])
    #
    # P = float(count)/len(true)
    # print "总准确率："+str(P)
    # truedict = dict(collections.Counter(true))
    # resdict = {1:0,2:0,3:0,4:0,5:0,6:0,7:0}
    # resdict.update(dict(collections.Counter(res)))
    # print "财经："+str(float(resdict[1])/truedict[1])
    # print "科技："+str(float(resdict[2])/truedict[2])
    # print "汽车："+str(float(resdict[3])/truedict[3])
    # print "房产："+str(float(resdict[4])/truedict[4])
    # print "体育："+str(float(resdict[5])/truedict[5])
    # print "娱乐："+str(float(resdict[6])/truedict[6])
    # print "其他："+str(float(resdict[7])/truedict[7])
    #
    #
    # return '财经'