from django.contrib import admin
from Article.models import *

class articleAdmin(admin.ModelAdmin):
    list_display =["AID","link","title","importTime","publicTime","author","authorLink","source","note"]

admin.site.register(Article,articleAdmin)

class tagAdmin(admin.ModelAdmin):
    list_display =["TID","name"]

admin.site.register(Tag,tagAdmin)

class a_tAdmin(admin.ModelAdmin):
    list_display =["AID","TID"]

admin.site.register(Article_Tag,a_tAdmin)

class collectionAdmin(admin.ModelAdmin):
    list_display =["CID","name","number"]

admin.site.register(Collection,collectionAdmin)

class c_aAdmin(admin.ModelAdmin):
    list_display =["CID","AID","orderID"]

admin.site.register(Collection_Article,c_aAdmin)

