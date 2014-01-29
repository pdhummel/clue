import clue.settings
from django.conf.urls.defaults import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

from views.player_api_view import PlayerList, PlayerDetail
from views.game_api_view import GameList, GameDetail, GameSecretDetail

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    #url(r'^clue/$', 'clue.views.clue', name='clue')  
    # Examples:
    # url(r'^$', 'clue.views.home', name='home'),
    # url(r'^clue/', include('clue.foo.urls')),


    #url(r'^clue/test_json/$', 'clue.views.rest_apis.test_json', name='test_json'),        
    #url(r'^players/$', 'clue.views.rest_apis.player_list'),
    #url(r'^players/(?P<pk>[0-9]+)/$', 'clue.views.rest_apis.player_detail'),
    #url(r'^players/$', PlayerList.as_view()),
    #url(r'^players/(?P<pk>[0-9]+)/$', PlayerDetail.as_view()),    


    url(r'^clue/static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': clue.settings.STATIC_ROOT}),    

    #url(r'^index$', 'clue.views.index', name='index'),
    url(r'^clue/$', 'clue.views.clue', name='clue'),
    url(r'^clue/login/$', 'clue.views.login_user'),  
    
    url(r'^clue/games/$', GameList.as_view()),
    url(r'^clue/games/(?P<pk>[0-9]+)/$', GameDetail.as_view()),
    #url(r'^clue/games/(?P<pk>[0-9]+)/$', GameSecretDetail.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)

