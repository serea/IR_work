#coding=utf-8
import scrapy
import sys
import json
from xlutils.copy import copy 
from tutorial.items import TutorialItem
reload(sys)
sys.setdefaultencoding('utf-8')
global count
global num
num = 1;
class DmozSpider(scrapy.spiders.Spider):
    name = "IR_news"

    hurl = "http://www.bjnews.com.cn/sport/list-28-page-"
    start_urls=[]
    for nn in range(1,51):
    	aurl=hurl+str(nn)+".html"
    	start_urls.append(aurl)

    # start_urls=["http://203.192.8.57/was5/web/search?channelid=276589&searchword=extend5%3D%27%2511109449%25%27&prepage=1000&list=&page=1"]
    
	# 财经 "http://203.192.8.57/was5/web/search?channelid=214510&prepage=1000&searchword=extend5%3D%27%2511105289%25%27"
	# 科技 "http://203.192.8.57/was5/web/search?channelid=234968&searchword=extend5%3D%27%2511109303%25%27&prepage=1000&list=&page=1"
	# 汽车 "http://203.192.8.57/was5/web/search?channelid=276589&prepage=1000&searchword=extend5%3D%27%2511109357%25%27"
	# 房产 "http://www.chinanews.com/house/gd.shtml" "http://fdc.fang.com/news/more/11806/1.html"
	# 体育 "http://www.bjnews.com.cn/sport/list-28-page-1.html"
	# 娱乐 "http://www.shcaoan.com/wy/"
	# 其他 "http://203.192.8.57/was5/web/search?channelid=276589&searchword=extend5%3D%27%2511109449%25%27&prepage=1000&list=&page=1"
    def parse(self, response):
        global count
        count = 1
        global num
        num += 1 
        global title    
        titles = response.xpath('//dl/dd/a')#'//div/div/div/div/ul/li/a')#'//ul/li/div/a')#'//h2/a'#'//dl/dd/a'#".//*[@id='content_right']/div[3]/ul/li/div/a"
        #titles = response.xpath(".//*[@id='divlist1']/ul/li/a")
        
        for sel in titles:
            title= sel.xpath('text()').extract()
            link = sel.xpath('@href').extract()[0]#.decode('utf-8')
            print link
            yield scrapy.Request(link, callback=self.parse_desc)  

    def parse_desc(self,response):

        item = TutorialItem()

        tf = open('news.json','ab')
        global count
        global num

        item['tid'] = num
        item['aid'] = count
        #item['title'] = response.xpath(".//*[@id='title']/text()").extract()[0].encode('utf8').replace('\n','').replace('\r','')
        #item['title'] = response.xpath(".//*[@id='endArea_Title']/text()").extract()[0].encode('utf8').replace('\n','').replace('\r','')
        item['title'] = response.xpath(".//*[@id='main']/div[1]/h1/text()").extract()[0].encode('utf8').replace('\n','').replace('\r','')
        #item['title'] = response.xpath(".//*[@id='cont_1_1_2']/h1/text()").extract()[0].encode('utf8').replace('\n','').replace('\r','')
        #item['title'] = response.xpath(".//*[@id='container']/div[2]/div[1]/div/div[1]/h1/text()").extract()[0].encode('utf8').replace('\n','').replace('\r','')
        
        print item['title']
        item['link'] = response.url
        #descs = response.xpath(".//*[@id='article']/div[2]/p/text()").extract()
        #descs = response.xpath(".//*[@id='endArea_Detail']/p/text()").extract()
        descs = response.xpath(".//*[@id='main']/div/div/p/text()").extract()
        #descs = response.xpath(".//*[@id='cont_1_1_2']/div[6]/p/text()").extract()
        #descs = response.xpath(".//*[@id='news_body']/p/text()").extract()
        item['desc'] = ''
        for desc in descs:
            item['desc'] = item['desc'] + desc.encode('utf8').replace('\n','').replace('\r','')

        #print item['desc']
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        #print line
        tf.write(line)
        count += 1
                    
