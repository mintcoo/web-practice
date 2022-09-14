from django.contrib import admin
from .models import Article, Usericon, Profile, Itembox

# Register your models here.
class Admin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content')

class IconAdmin(admin.ModelAdmin):
    list_display = ('icon_id', 'iconname', 'url')


class ItemAdmin(admin.ModelAdmin):
    list_display = ('username', 'icon_id')


admin.site.register(Article, Admin)
admin.site.register(Usericon, IconAdmin)
admin.site.register(Profile)
admin.site.register(Itembox, ItemAdmin)

