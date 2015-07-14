# -*- coding:utf-8 -*-
import requests
import re
#import xlwt
import os

#本程序用于多进程抓取贴吧校园分类下所有贴吧会员数、主题数、帖子数。抓取的数据直接输出。

jsurl = 'http://tieba.baidu.com/f/fdir?fd=%B8%DF%B5%C8%D4%BA%D0%A3&sd=%BD%AD%CB%D5%D4%BA%D0%A3'
i=0


#file = xlwt.Workbook()
#tables = file.add_sheet('all',cell_overwrite_ok=True)


#c为创建进程数
c=35

#定义请求函数
def reget(url):
    try:
        page=requests.get(url,timeout=30).text
        return page
    except:
        return None

#定义获取贴吧数据函数
def getdata(surl,i):
    tbpage = reget(surl)
    #print tbpage.text
    zt=u"主题数"
    tz=u"贴子数"

    try:
        gettbzt = re.findall(r'%s.*?(\d{1,20})'%zt,tbpage,re.S)[0]
        gettbtz = re.findall(r'%s.*?(\d{1,50})'%tz,tbpage,re.S)[0]
        gettbmem = re.findall(r'member_num\"\:(\d*)',tbpage,re.S)[0]
        gettbnm = re.findall(r'forum_id.*?name\:\ \'(.*?)\'',tbpage,re.S)[0]

        # tables.write(i,0,gettbnm)
        # tables.write(i,1,gettbmem)
        # tables.write(i,2,gettbzt)
        # tables.write(i,3,gettbtz)
        #file.save('111.xls')
        print gettbnm,gettbmem,gettbzt,gettbtz

    except:
        pass

#定义获取该区域学校链接函数
def getschool(areaurl,listnum,i):
    #print listnum
    for num in range(1,listnum+1):
        url = areaurl+'&pn='+str(num)
        #print url
        areapage = reget(url)
        #print areapage.text
        schoollist=re.findall(r'(http\:\/\/tieba\.baidu\.com\/f\?kw\=(?!\').*?)\'',areapage,re.S)
        if schoollist==[]:
            break
        else:
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
        listnum = 27
        return listnum

#定义多进程创建函数。其中主进程用于创建下一个子进程，子进程用于执行任务。
def osfork(leng,c,k,getarealist):
    if c==0:
        print "程序运行结束！"
    else:
        pid = os.fork()
        if pid==0:
            for nuu in range(c-1,leng,k):
                areaurl = 'http://tieba.baidu.com'+getarealist[nuu]
                listnum = getnum(areaurl)
                getschool(areaurl,listnum,i)
        else:
            c=c-1
            osfork(leng,c,k,getarealist)


#定义获取区域链接函数
def getedulist(page,i):
    getarealist = re.findall(r'\<li\>.*?href\=\"(.{50,80}?)\"',page,re.S)
    getarealist.append(u'/f/fdir?fd=%B8%DF%B5%C8%D4%BA%D0%A3&sd=%BD%AD%CB%D5%D4%BA%D0%A3')
    #print getarealist
    leng = len(getarealist)
    k=c
    osfork(leng,c,k,getarealist)

try:
    getjs = requests.get(jsurl)
except:
    print "首页数据获取失败！请检查网络！"

getedulist(getjs.text,i)


# def osfork(c):
#     if c==0:
#         break
#     else:
#         k=2^c
#         pid == os.fork()
#         if pid==0:
#             c=c-1
#             osfork(c)
#             for nuu in range(k-1,leng+k,k):
#                 areaurl = 'http://tieba.baidu.com'+getarealist[nuu]
#                 listnum = getnum(areaurl)
#                 getschool(areaurl,listnum,i)

            
#         else :
#             c=c-1
#             osfork(c)
#             for nuu in range(k-2,leng+k-1,k):
#                 areaurl = 'http://tieba.baidu.com'+getarealist[nuu]
#                 listnum = getnum(areaurl)
#                 getschool(areaurl,listnum,i)




#传统多进程创建方式
# #定义多进程
#     pid = os.fork()
#     if pid==0:
#         #file = xlwt.Workbook()
#         #tables = file.add_sheet('sheet',cell_overwrite_ok=False)
#         #file.save('sheet.xls')
#         pidd = os.fork()
#         if pidd==0:
#             piddd = os.fork()
#             if piddd==0:
#                 for nu in range(0,leng+1,8):
#                     areaurl = 'http://tieba.baidu.com'+getarealist[nu]
#                     listnum = getnum(areaurl)
#                     getschool(areaurl,listnum,i)
#             else :
#                 for nu in range(1,leng+2,8):
#                     areaurl = 'http://tieba.baidu.com'+getarealist[nu]
#                     listnum = getnum(areaurl)
#                     getschool(areaurl,listnum,i)
#         else :
#             piddd = os.fork()
#             if piddd==0:
#                 for nu in range(2,leng+3,8):
#                     areaurl = 'http://tieba.baidu.com'+getarealist[nu]
#                     listnum = getnum(areaurl)
#                     getschool(areaurl,listnum,i)
#             else :
#                 for nu in range(3,leng+4,8):
#                     areaurl = 'http://tieba.baidu.com'+getarealist[nu]
#                     listnum = getnum(areaurl)
#                     getschool(areaurl,listnum,i)

#     else:
#         #file = xlwt.Workbook()
#         #tables = file.add_sheet('sheet1',cell_overwrite_ok=False)
#         #file.save('sheet1.xls')
#         pidd = os.fork()
#         if pidd==0:
#             piddd = os.fork()
#             if piddd==0:
#                 for nu in range(4,leng+5,8):
#                     areaurl = 'http://tieba.baidu.com'+getarealist[nu]
#                     listnum = getnum(areaurl)
#                     getschool(areaurl,listnum,i)
#             else :
#                 for nu in range(5,leng+6,8):
#                     areaurl = 'http://tieba.baidu.com'+getarealist[nu]
#                     listnum = getnum(areaurl)
#                     getschool(areaurl,listnum,i)
#         else:
#             piddd = os.fork()
#             if piddd==0:
#                 for nu in range(6,leng+7,8):
#                     areaurl = 'http://tieba.baidu.com'+getarealist[nu]
#                     listnum = getnum(areaurl)
#                     getschool(areaurl,listnum,i)
#             else :
#                 for nu in range(7,leng+8,8):
#                     areaurl = 'http://tieba.baidu.com'+getarealist[nu]
#                     listnum = getnum(areaurl)
#                     getschool(areaurl,listnum,i)




    # for arealist in getarealist:
    #     areaurl =  'http://tieba.baidu.com'+arealist
    #     #print areaurl
    #     listnum = getnum(areaurl)
    #     raw_input()
    #     getschool(areaurl,listnum,i)



#jslistnum = getnum(jsurl)
#getschool(jsurl,jslistnum,i)



