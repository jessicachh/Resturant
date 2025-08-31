from django.contrib import admin
from django.utils.html import format_html
from .models import *
admin.site.site_header="Myshop Project"
admin.site.site_title="django project"
admin.site.index_title="h13 project"


# Register your models here.
admin.site.register(Category)
@admin.register(Momo)
class MomoAdmin(admin.ModelAdmin):
    list_display=['id','name','category','desc','price','display_img']
    list_display_links=['name']
    list_editable=['category']
    list_filter=['price','category']
    list_per_page=2
    ordering=['name']

    def display_img(self,obj):
        if obj.image:
             return format_html('<img src="{}" width="100px" height="100px"; >',obj.image.url)
    