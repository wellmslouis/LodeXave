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
        if author!=None:
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
            b = yearInput + "-" + articleMonth + "-" + articleDay
            d = soup.find("div", class_="tag")
            tags = d.find_all("a")
        else:
            author = soup.find("div", class_="g-sd")
            authorName = author.find("h1").text

            article = soup.find("div", class_="dtinner")
            articleText = article.find("div", class_="ctc box")
            articleTitle = articleText.find("h2").text
            articleContents = articleText.findAll("p")
            articleContentT = ""
            for i in articleContents:
                a = i.text
                articleContentT += a
                articleContentT += "\n"
            b=article.find("a",class_="date").text
            d=soup.find("div", class_="info box")
            tags=d.find_all("a",class_="tag")


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
        c = dt.strptime(b, '%Y-%m-%d')
        newA.publicTime=c
        newA.save()
        curA=Article.objects.get(link=linkInput)


        for i in tags:
            e=i.text
            f=""
            for j in e:
                if j=="●" or j==" " or j=="#":
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
        strTags=""
        for i in range(len(curAT)):
            curT=Tag.objects.get(TID=curAT[i].TID)
            tags.append(curT.name)
            strTags+=curT.name+";"
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
            "tag":tags,
            "strT":strTags
        }
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d")

def displayAllArticles(request):
    if request.method == 'POST':
        articlesInput=Article.objects.filter()
        articles=[]
        for i in articlesInput:
            article={}
            article["id"]=i.AID
            article["title"]=i.title
            article["author"]=i.author
            article["publicTime"]=datetime_toString(i.publicTime)
            try:
                getCID=Collection_Article.objects.get(AID=i.AID).CID
                getCName=Collection.objects.get(CID=getCID).name
            except:
                getCName=""
            article["collectionName"]=getCName
            articles.append(article)
        result = {
            "code": 200,
            "msg": "请求文章们详细信息成功",
            "articles":articles,
            "length":len(articles)
        }
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

def editArticle(request):
    if request.method == 'POST':
        getAID=request.POST.get("id")
        curA=Article.objects.get(AID=getAID)
        getTitle=request.POST.get("title")
        getAuthor=request.POST.get("author")
        getContent=request.POST.get("content")
        getStrT=request.POST.get("strT")
        curA.title=getTitle
        curA.author=getAuthor
        curA.content=getContent
        curA.save()
        getTags=getStrT.split(";")
        Article_Tag.objects.filter(AID=getAID).delete()
        for i in getTags:
            if i=="":
                continue
            try:
                curT=Tag.objects.get(name=i)
            except:#没有存过这个tag
                newT=Tag()
                newT.name=i
                newT.save()
                curT = Tag.objects.get(name=i)
            newAT=Article_Tag()
            newAT.AID=curA.AID
            newAT.TID=curT.TID
            newAT.save()
        result = {
            "code": 200,
            "msg": "修改文章成功",
        }
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

def deleteArticle(request):
    if request.method == 'POST':
        getAID=request.POST.get("id")
        Article.objects.filter(AID=getAID).delete()
        Article_Tag.objects.filter(AID=getAID).delete()
        Collection_Article.objects.filter(AID=getAID).delete()
        result = {
            "code": 200,
            "msg": "删除文章成功",
        }
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

def searchArticle(request):
    if request.method == 'POST':
        getT=request.POST.get("search")
        getAllA=Article.objects.filter()
        articles=[]
        for i in getAllA:
            if getT in i.title:
                article = {}
                article["id"] = i.AID
                article["title"] = i.title
                article["author"] = i.author
                article["publicTime"] = datetime_toString(i.publicTime)
                try:
                    getCID = Collection_Article.objects.get(AID=i.AID).CID
                    getCName = Collection.objects.get(CID=getCID).name
                except:
                    getCName = ""
                article["collectionName"] = getCName
                articles.append(article)
        result = {
            "code": 200,
            "msg": "请求文章们详细信息成功",
            "articles": articles,
            "length": len(articles)
        }
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

def displayAllTags(request):
    if request.method == 'POST':
        getAllT=Tag.objects.filter()
        tags=[]
        for i in getAllT:
            getAT=Article_Tag.objects.filter(TID=i.TID)
            if len(getAT)==0:
                Tag.objects.get(TID=i.TID).delete()
                continue
            tag={}
            tag["number"]=len(getAT)
            tag["name"]=i.name
            tag["id"]=i.TID
            tags.append(tag)
        #待排序
        result = {
            "code": 200,
            "msg": "请求标签们详细信息成功",
            "tags": tags,
            "length": len(tags)
        }
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

def displayAllArticlesInTag(request):
    if request.method == 'POST':
        getTID = request.POST.get("id")
        print(getTID)
        name=Tag.objects.get(TID=getTID).name
        a=Article_Tag.objects.filter(TID=getTID)
        articles = []
        for i in a:
            b=Article.objects.get(AID=i.AID)
            article = {}
            article["id"] = b.AID
            article["title"] = b.title
            article["author"] = b.author
            article["publicTime"] = datetime_toString(b.publicTime)
            try:
                getCID = Collection_Article.objects.get(AID=b.AID).CID
                getCName = Collection.objects.get(CID=getCID).name
            except:
                getCName = ""
            article["collectionName"] = getCName
            articles.append(article)
        result = {
            "code": 200,
            "msg": "请求标签内文章们详细信息成功",
            "articles": articles,
            "length": len(articles),
            "name":name
        }
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

def deleteTag(request):
    if request.method == 'POST':
        getTID = request.POST.get("id")
        Tag.objects.get(TID=getTID).delete()
        Article_Tag.objects.filter(TID=getTID).delete()
        result = {
            "code": 200,
            "msg": "删除标签成功"
        }
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False})