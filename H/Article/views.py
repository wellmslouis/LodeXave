from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime as dt
from Article.models import *
import requests
import re
from bs4 import BeautifulSoup

def strSource(sourceInput):
    source=["LOFTER"]
    if sourceInput>0:
        return source[sourceInput-1]
    else:
        return "未知"

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()  # 如果状态不是200，引发HTMLError异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"

def spiderArticle(request):
    if request.method=='POST':
        linkInput=request.POST.get("link")
        yearInput = request.POST.get("year")

        #爬取数据
        text = getHTMLText(linkInput)
        soup = BeautifulSoup(text, "lxml")
        author = soup.find("div", class_="selfinfo")
        authorName = author.find("h1").text
        article = soup.find("div", class_="block article")
        articleDay = article.find("div", class_="day").text
        articleMonth = article.find("div", class_="month").text
        articleText = article.find("div", class_="text")
        articleTitle = articleText.find("h2").text
        articleContents = articleText.findAll("p")
        articleContentT = ""
        for i in articleContents:
            a = i.text
            articleContentT+=a
            articleContentT+="\n"

        #导入数据
        newA=Article()
        newA.link=linkInput
        newA.title=articleTitle
        newA.content=articleContentT
        newA.author=authorName
        newA.source=1
        patternA = r"post/"
        a = re.search(patternA, linkInput)
        authorUrl = ""
        for i in range(a.start()):
            authorUrl += linkInput[i]
        newA.authorLink=authorUrl
        b=yearInput+"-"+articleMonth+"-"+articleDay
        c = dt.strptime(b, '%Y-%m-%d')
        newA.publicTime=c
        newA.save()
        curA=Article.objects.get(link=linkInput)

        d = soup.find("div", class_="tag")
        tags=d.find_all("a")
        for i in tags:
            e=i.text
            f=""
            for j in e:
                if j=="●" or j==" ":
                    continue
                else:
                    f+=j
            try:
                curT=Tag.objects.get(name=f)
            except:#没有存过这个tag
                newT=Tag()
                newT.name=f
                newT.save()
                curT = Tag.objects.get(name=f)
            newAT=Article_Tag()
            newAT.AID=curA.AID
            newAT.TID=curT.TID
            newAT.save()
        result = {
            "code": 200,
            "msg": "导入成功",
            "id": curA.AID
        }
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

def displayArticle(request):
    if request.method == 'POST':
        idInput = request.POST.get("id")
        curA = Article.objects.get(AID=idInput)
        curAT=Article_Tag.objects.filter(AID=idInput)
        tags=[]
        for i in range(len(curAT)):
            curT=Tag.objects.get(TID=curAT[i].TID)
            tags.append(curT.name)

        #test
        print(idInput)

        result = {
            "code": 200,
            "msg": "请求文章详细信息成功",
            "title":curA.title,
            "link":curA.link,
            "author":curA.author,
            "authorLink":curA.authorLink,
            "importTime":curA.importTime,
            "publicTime":curA.publicTime,
            "note":curA.note,
            "source":strSource(curA.source),
            "content":curA.content,
            "tag":tags
        }
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

