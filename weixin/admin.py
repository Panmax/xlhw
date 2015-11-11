# -*- coding: utf-8 -*-
from models import News, Commander, Text

__author__ = 'JiaPan'
from django.contrib import admin


class NewsAdmin(admin.ModelAdmin):
    list_display = ('shorttitle', 'shortdescription', 'commander', 'priority', 'is_valid')

    def shorttitle(self, obj):
        return obj.title[:20]

    shorttitle.short_description = u'标题'

    def shortdescription(self, obj):
        return obj.description[:20]

    shortdescription.short_description = u'描述'

    list_filter = ['commander']

class TextAdmin(admin.ModelAdmin):
    list_display = ('shortcontent', 'commander', 'is_valid')

    def shortcontent(self, obj):
        return obj.content[:20]
    shortcontent.short_description = u'内容'

    list_filter = ['commander']


admin.site.register(News, NewsAdmin)
admin.site.register(Commander)
admin.site.register(Text, TextAdmin)