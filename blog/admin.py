from django.contrib import admin
from .models import Category,Page,UserProfile

class ChoiceInline(admin.TabularInline):
    '''设置Page在别的模型内编辑'''
    model = Page
    extra = 3

class CategoryAdmin(admin.ModelAdmin):
    #定制在category详情页显示的项目
    # fields = ['name','views','likes']
    #把category详情页歌字段进行分类,不能与fields同时设置
    fieldsets = [
        (None,{'fields':['name','slug']}),
        ('Views&Likes',{'fields':['views','likes']}),
    ]
    #定制在category列表页显示的项目
    list_display = ('name','views','likes')

    inlines = [ChoiceInline]

class PageAdmin(admin.ModelAdmin):
    list_display = ('title','views','category','url')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(UserProfile)

