from django.urls import path, re_path
from . import views
from . import api

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('docs/', views.docs, name='docs'),
    path('downloads', views.downloads, name='downloads'),
    path('model/<int:model_id>', views.model, name='model'),
    path('model/<int:model_id>/<int:revision>', views.model, name='model'),
    path('search', views.search, name='search'),
    path('upload', views.upload, name='upload'),
    path('revise/<int:model_id>', views.revise, name='revise'),
    path('edit/<int:model_id>/<int:revision>', views.edit, name='edit'),
    path('user', views.user, name='user'),
    path('user/<str:username>/', views.user, name='user'),
    path('map', views.modelmap, name='map'),
    path('action/editprofile', views.editprofile, name='editprofile'),
    path('action/addcomment', views.addcomment, name='addcomment'),
    path('action/ban', views.ban, name='ban'),
    path('action/hide_model', views.hide_model, name='hide_model'),
    path('action/hide_comment', views.hide_comment, name='hide_comment'),

    path('api/info/<int:model_id>', api.get_info, name='get_info'),
    path('api/model/<int:model_id>/<int:revision>', api.get_model, name='get_model'),
    path('api/model/<int:model_id>', api.get_model, name='get_model'),
    path('api/filelist/<int:model_id>/<int:revision>', api.get_filelist, name='get_list'),
    path('api/filelist/<int:model_id>', api.get_filelist, name='get_list'),
    path('api/file/<int:model_id>/<int:revision>/<path:filename>', api.get_file, name='get_file'),
    path('api/filelatest/<int:model_id>/<path:filename>', api.get_file, name='get_file'),

    path('api/tag/<str:tag>/<int:page_id>', api.lookup_tag, name='lookup_tag'),
    path('api/tag/<str:tag>', api.lookup_tag, name='lookup_tag'),
    path('api/category/<str:category>/<int:page_id>', api.lookup_category, name='lookup_category'),
    path('api/category/<str:category>', api.lookup_category, name='lookup_category'),
    path('api/author/<str:username>/<int:page_id>', api.lookup_author, name='lookup_author'),
    path('api/author/<str:username>', api.lookup_author, name='lookup_author'),

    re_path(r'^api/search/(?P<latitude>-?\d+(\.\d+)?)/(?P<longitude>-?\d+(\.\d+)?)/(?P<distance>\d+(\.\d+)?)/(?P<page_id>\d+)$', api.search_range, name='lookup_range'),
    re_path(r'^api/search/(?P<latitude>-?\d+(\.\d+)?)/(?P<longitude>-?\d+(\.\d+)?)/(?P<distance>\d+(\.\d+)?)$', api.search_range, name='lookup_range'),
    re_path(r'^api/search/title/(?P<title>.+)/(?P<page_id>\d+)$', api.search_title, name='search_title'),
    re_path(r'^api/search/title/(?P<title>.+)$', api.search_title, name='search_title'),
    path('api/search/full', api.search_full, name='search_full'),
]
