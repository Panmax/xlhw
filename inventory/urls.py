from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'inventory.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'kucun.views.all_phone'),
                       url(r'kucun/', include('kucun.urls')),
                       url(r'sell/', include('sell.urls')),
                       url(r'weixin/', include('weixin.urls')),
                       url(r'meizu/', include('meizu.urls')),
)
