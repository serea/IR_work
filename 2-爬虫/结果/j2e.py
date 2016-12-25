#coding=utf-8
import xlrd
import xlwt
import json
from xlutils.copy import copy 

sheetn = ["其他","科技","财经","汽车","娱乐","体育","房产"]
filen = ["qt1000.json","kj999.json","cj992.json","qc330.json","yl485.json","ty991.json","fc584.json"]

for xh in range(0,len(filen)):
	wf =  xlwt.Workbook()  
	book=xlrd.open_workbook(r'news.xlsx')
	wf = copy(book) 
	rf = open(filen[xh],'r')
	ss = rf.read()
	s = ss.split("\n")
	d = []
	for line in s:
	   d.append(line)

	key = json.loads(d[0]).keys()
	lenth = len(d)
	print lenth

	sheet1 = wf.add_sheet(sheetn[xh],cell_overwrite_ok=True) 

	fnt =xlwt.Font()
	style =xlwt.XFStyle()
	style.font=fnt 

	for i in range(0,len(key)-1):
		sheet1.write(0,i,key[i+1])
	for j in range(0,lenth):
		k = key[0]
		d1 = json.loads(d[j])
			#print d1['link']
		content = []
		for k1 in key:
			content.append(d1[k1])
		for t in range(1,len(content)):
			sheet1.write_merge(j+1,j+1,t-1,t-1,content[t])  
	wf.save('news.xlsx')
	

