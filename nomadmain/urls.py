from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.article_list, name="article_list"),
    re_path(r'^blog/(?P<slug>[-\w]+)/$', views.article, name='article'),
    path('team/', views.team_list, name="team_list")
    #path('blog/<int:article_id>/', views.article, name='article')
]

