from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime as dt
from Article.models import *
import requests
import time
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
            c = dt.strptime(b, '%Y-%m-%d')
            d = soup.find("div", class_="tag")
            tags = d.find_all("a")
        else:
            author = soup.find("div", class_="g-sd")
            if author!=None:
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
                c = dt.strptime(b, '%Y-%m-%d')
                d=soup.find("div", class_="info box")
                tags=d.find_all("a",class_="tag")
            else:
                author=soup.find("div", class_="g-hd box")
                authorName = author.find("h1").text
                article = soup.find("div", class_="m-postdtl")
                articleText = article.find("div", class_="ctc box")
                articleTitle = articleText.find("h2").text
                articleContents = articleText.findAll("p")
                articleContentT = ""
                for i in articleContents:
                    e=str(i).replace("<br/>","\n")
                    a=(e.replace("<p>","")).replace("</p>","")
                    articleContentT += a
                    articleContentT += "\n"
                b = article.find("a", class_="date").text
                c = dt.strptime(b, '%Y.%m.%d')
                d = soup.find("div", class_="info box")
                tags = d.find_all("a", class_="tag")


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
        getAllC = Collection.objects.filter()
        collections = []
        for i in getAllC:
            collection = {}
            collection["name"] = i.name
            collection["id"] = i.CID
            collections.append(collection)
        result = {
            "code": 200,
            "msg": "请求文章们详细信息成功",
            "articles":articles,
            "length":len(articles),
            "collections":collections,
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

def createCollection(request):
    if request.method == 'POST':
        newC=Collection()
        newC.name="新建合集"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        newC.save()
        result = {
            "code": 200,
            "msg": "创建合集成功"
        }
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

def displayAllCollections(request):
    if request.method == 'POST':
        getAllC = Collection.objects.filter()
        collections = []
        for i in getAllC:
            collection={}
            collection["name"]=i.name
            collection["id"]=i.CID
            collection["num"]=i.number
            collections.append(collection)
        result = {
            "code": 200,
            "msg": "请求合集们详细信息成功",
            "collections": collections,
            "length": len(collections)
        }
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

def modifyCollectionName(request):
    if request.method == 'POST':
        getCID = request.POST.get("id")
        getName=request.POST.get("name")
        curC=Collection.objects.get(CID=getCID)
        curC.name=getName
        curC.save()
        result = {
            "code": 200,
            "msg": "重命名合集成功"
        }
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

def deleteCollection(request):
    if request.method == 'POST':
        getCID = request.POST.get("id")
        Collection.objects.get(CID=getCID).delete()
        Collection_Article.objects.filter(CID=getCID).delete()
        result = {
            "code": 200,
            "msg": "删除合集成功"
        }
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

def addArticleToCollection(request):
    if request.method == 'POST':
        getCID = request.POST.get("cid")
        getAID=request.POST.get("aid")
        curC=Collection.objects.get(CID=getCID)
        newCA=Collection_Article()
        newCA.CID=getCID
        newCA.AID=getAID
        newCA.orderID=curC.number+1
        newCA.save()
        curC.number+=1
        curC.save()
        result = {
            "code": 200,
            "msg": "添加至合集成功"
        }
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

def displayAllArticlesInCollection(request):
    if request.method == 'POST':
        getCID = request.POST.get("id")
        curC=Collection.objects.get(CID=getCID)
        curCAs=Collection_Article.objects.filter(CID=getCID)
        articles=[]
        for i in curCAs:
            article={}
            article["AID"]=i.AID
            article["OID"]=i.orderID
            article["title"]=Article.objects.get(AID=i.AID).title
            articles.append(article)
        articles.sort(key=lambda item: item.get("OID"))
        result = {
            "code": 200,
            "msg": "请求合集内文章们全部信息成功",
            "name":curC.name,
            "articles":articles
        }
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

def deleteArticleFromCollection(request):
    if request.method == 'POST':
        getAID = request.POST.get("id")
        curCA=Collection_Article.objects.get(AID=getAID)
        a=curCA.orderID
        curCID=curCA.CID
        curC=Collection.objects.get(CID=curCID)
        curC.number-=1
        curC.save()
        curCA.delete()
        curCAs=Collection_Article.objects.filter(CID=curCID)
        for i in curCAs:
            if i.orderID>a:
                i.orderID-=1
                i.save()
        result = {
            "code": 200,
            "msg": "删除合集中文章成功"
        }
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

def moveUpInCollection(request):
    if request.method == 'POST':
        getOID = int(request.POST.get("oid"))
        getCID=request.POST.get("cid")
        if getOID==1:
            result = {
                "code": 200,
                "msg": "已在最前"
            }
            return JsonResponse(result, json_dumps_params={"ensure_ascii": False})
        else:
            curA=Collection_Article.objects.get(orderID=getOID,CID=getCID)
            curB=Collection_Article.objects.get(orderID=getOID-1,CID=getCID)
            curA.orderID-=1
            curB.orderID += 1
            curA.save()
            curB.save()
            result = {
                "code": 200,
                "msg": "上移成功"
            }
            return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

def moveDownInCollection(request):
    if request.method == 'POST':
        getOID = int(request.POST.get("oid"))
        getCID=request.POST.get("cid")
        curNum=int(Collection.objects.get(CID=getCID).number)
        if getOID==curNum:
            result = {
                "code": 200,
                "msg": "已在最后"
            }
            return JsonResponse(result, json_dumps_params={"ensure_ascii": False})
        else:
            curA=Collection_Article.objects.get(orderID=getOID,CID=getCID)
            curB=Collection_Article.objects.get(orderID=getOID+1,CID=getCID)
            curA.orderID+=1
            curB.orderID -= 1
            curA.save()
            curB.save()
            result = {
                "code": 200,
                "msg": "下移成功"
            }
            return JsonResponse(result, json_dumps_params={"ensure_ascii": False})