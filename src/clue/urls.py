import clue.settings
from django.conf.urls.defaults import patterns, include, url


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',                   
    #url(r'^index$', 'clue.views.index', name='index'),
    url(r'^clue/$', 'clue.views.clue', name='clue'),
    url(r'^clue/test_json/$', 'clue.views.test_json', name='test_json'),        
    url(r'^clue/login/$', 'clue.views.login_user'),    
        
    url(r'^clue/static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': clue.settings.STATIC_ROOT}),    
    
    #url(r'^clue/$', 'clue.views.clue', name='clue')  
    # Examples:
    # url(r'^$', 'clue.views.home', name='home'),
    # url(r'^clue/', include('clue.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


