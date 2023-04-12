from django.contrib import admin
from . import models

admin.site.register(models.Service)
admin.site.register(models.Article)
#admin.site.register(models.Course)
admin.site.register(models.Contact)
admin.site.register(models.OnlineForm)

@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display = ('title','updated')
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','publish','status')
    list_filter = ('status','created','publish','author')
    search_fields = ('title','body')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    data_hierarchy = 'publish'
    ordering = ('status','publish')
@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created','active')
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')
