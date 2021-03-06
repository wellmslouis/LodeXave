"""LX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Article.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('spiderArticle',spiderArticle,name='spiderArticle'),
    path('displayArticle',displayArticle,name='displayArticle'),
    path('displayAllArticles',displayAllArticles,name='displayAllArticles'),
    path('editArticle',editArticle,name='editArticle'),
    path('deleteArticle',deleteArticle,name='deleteArticle'),
    path('searchArticle',searchArticle,name='searchArticle'),
    path('displayAllTags',displayAllTags,name='displayAllTags'),
    path('displayAllArticlesInTag',displayAllArticlesInTag,name='displayAllArticlesInTag'),
    path('deleteTag',deleteTag,name='deleteTag'),
    path('createCollection',createCollection,name='createCollection'),
    path('displayAllCollections', displayAllCollections, name='displayAllCollections'),
    path('modifyCollectionName', modifyCollectionName, name='modifyCollectionName'),
    path('deleteCollection', deleteCollection, name='deleteCollection'),
    path('addArticleToCollection', addArticleToCollection, name='addArticleToCollection'),
    path('displayAllArticlesInCollection', displayAllArticlesInCollection, name='displayAllArticlesInCollection'),
    path('deleteArticleFromCollection', deleteArticleFromCollection, name='deleteArticleFromCollection'),
    path('moveUpInCollection', moveUpInCollection, name='moveUpInCollection'),
    path('moveDownInCollection', moveDownInCollection, name='moveDownInCollection'),
]
