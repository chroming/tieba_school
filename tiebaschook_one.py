# -*- coding:utf-8 -*-
import requests
import re
import xlwt

#本程序用于抓去贴吧校园分类下所有贴吧会员数、主题数、帖子数。单进程抓取。

jsurl = 'http://tieba.baidu.com/f/fdir?fd=%B8%DF%B5%C8%D4%BA%D0%A3&sd=%BD%AD%CB%D5%D4%BA%D0%A3'
i=0

file = xlwt.Workbook()
tables = file.add_sheet('all',cell_overwrite_ok=True)

def reget(url):
    try:
        page=requests.get(url,timeout=30)
        return page
    except:
        return None

#根据贴吧页面抓取数据
def getdata(surl,i):
    tbpage = reget(surl)
    #print tbpage.text
    zt=u"主题数"
    tz=u"贴子数"

    try:
        gettbzt = re.findall(r'%s.*?(\d{1,20})'%zt,tbpage.text,re.S)[0]
        gettbtz = re.findall(r'%s.*?(\d{1,50})'%tz,tbpage.text,re.S)[0]
        gettbmem = re.findall(r'member_num\"\:(\d*)',tbpage.text,re.S)[0]
        gettbnm = re.findall(r'forum_id.*?name\:\ \'(.*?)\'',tbpage.text,re.S)[0]

        tables.write(i,0,gettbnm)
        tables.write(i,1,gettbmem)
        tables.write(i,2,gettbzt)
        tables.write(i,3,gettbtz)
        file.save('all.xls')
        print gettbnm,gettbmem,gettbzt,gettbtz

    except:
        pass

#获取该地区学校链接
def getschool(areaurl,listnum,i):
    print listnum
    for num in range(1,listnum+1):
        url = areaurl+'&pn='+str(num)
        areapage = reget(url)
        #print areapage.text
        schoollist=re.findall(r'(http\:\/\/tieba\.baidu\.com\/f\?kw\=(?!\').*?)\'',areapage.text,re.S)
        for surl in schoollist:
            #print surl
            getdata(surl,i)
            i=i+1

#定义获取页数函数
def getnum(areaurl):
    st = u"尾页"
    try:
        page = requests.get(areaurl,timeout=30)
        getpagenum = re.findall(r'pn=(\d{1,3})\"\>%s\<'%st,page.text,re.S)
        listnum = int(getpagenum[0])
        return listnum
    except:
        print "获取页数出错！重试中"
        getnum(areaurl)

#获取地区链接
def getedulist(page,i):
    getarealist = re.findall(r'\<li\>.*?href\=\"(.{50,80}?)\"',page,re.S)
    getarealist.append(u'/f/fdir?fd=%B8%DF%B5%C8%D4%BA%D0%A3&sd=%BD%AD%CB%D5%D4%BA%D0%A3')
    for arealist in getarealist:
        areaurl =  'http://tieba.baidu.com'+arealist
        #print areaurl
        listnum = getnum(areaurl)
        getschool(areaurl,listnum,i)

getjs = requests.get(jsurl,timeout=30)
#jslistnum = getnum(jsurl)
#getschool(jsurl,jslistnum,i)

getedulist(getjs.text,i)

