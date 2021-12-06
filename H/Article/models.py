from django.db import models


class Article(models.Model):
    AID = models.AutoField(primary_key=True)
    link=models.CharField(max_length=500)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=100000)
    importTime=models.DateTimeField(auto_now_add=True)
    publicTime=models.DateTimeField(default="1900-01-01")
    author=models.CharField(max_length=100)
    authorLink=models.CharField(max_length=500)
    note=models.CharField(max_length=10000,default="暂无")
    source=models.IntegerField(default=0)#来源：手动导入为0，lofter为1

class Article_Tag(models.Model):
    AID=models.IntegerField()
    TID=models.IntegerField()

class Tag(models.Model):
    TID = models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)

class Collection(models.Model):
    CID = models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)

class Collection_Article(models.Model):
    CID = models.IntegerField()
    AID = models.IntegerField()
    orderID=models.IntegerField(default=0)