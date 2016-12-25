#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
import urllib2
import ie_knn
import textclassify
# Create your views here.


def index(request):
    # return HttpResponse(u"信息检索作业!")
    return render(request, 'index.html')


def result(request):
    # return HttpResponse(u"信息检索作业!")
    return render(request, 'result.html')


def answer(request):

    d_url=request.GET['url']
    d_content = urllib2.urlopen(d_url).read()
    soup = BeautifulSoup(d_content)
    d_text=soup.get_text()
    answer_list={1:'财经',2:'科技',3:'汽车',4:'房产',5:'体育',6:'娱乐',7:'其他'}
    # prekind=ie_knn.answer(d_text)
    prekind_knn=textclassify.d_kNNtestonefile(d_text)
    prekind_bayes=textclassify.d_bayestestonefile(d_text)
    d_result_knn=answer_list[prekind_knn[0][0]]
    d_result_bayes = answer_list[prekind_bayes[0][0]]

    d_dict = {}
    for i in xrange(0,7):
        d_dict[prekind_knn[i][0]] = prekind_knn[i][1]
    d_list_knn = d_dict.values()[::-1]

    d_dict = {}
    for i in xrange(0, 7):
        d_dict[prekind_bayes[i][0]] = prekind_bayes[i][1]
    d_list_bayes = d_dict.values()[::-1]
    # return HttpResponse(rep)
    return render(request, 'result.html', {'d_result_knn': d_result_knn,'d_result_bayes': d_result_bayes,'d_list_knn':d_list_knn,'d_list_bayes':d_list_bayes})
