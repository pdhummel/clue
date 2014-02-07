import clue.settings
from django.conf.urls.defaults import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

from views.player_api_view import PlayerList, PlayerDetail
from views.game_api_view import GameList, GameDetail, GameSecretDetail
from views.game_piece_api_view import GamePieceList, GamePieceDetail, piece_list
from views.game_player_api_view import GamePlayerList, GamePlayerDetail

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
    url(r'^clue/game_list/$', 'clue.views.game_list'),
    url(r'^clue/enter_game/$', 'clue.views.enter_game'),
    url(r'^clue/join_game/$', 'clue.views.join_game'),
    
    url(r'^clue/games/$', GameList.as_view()),
    url(r'^clue/games/(?P<pk>[0-9]+)/$', GameDetail.as_view()),
    url(r'^clue/games/secret/(?P<pk>[0-9]+)/$', GameSecretDetail.as_view()),
    
    url(r'^clue/games/(?P<game_pk>.+)/pieces/$', GamePieceList.as_view(), name='game_pieces_list'),    
    url(r'^clue/games/(?P<game_pk>[0-9]+)/pieces/(?P<pk>[0-9]+)/$', GamePieceDetail.as_view()),
    url(r'^clue/pieces/$', piece_list),
    
    url(r'^clue/games/(?P<game_pk>.+)/players/$', GamePlayerList.as_view(), name='game_players_list'),    
    url(r'^clue/games/(?P<game_pk>[0-9]+)/players/(?P<pk>[0-9]+)/$', GamePlayerDetail.as_view()),    
)

urlpatterns = format_suffix_patterns(urlpatterns)

