from django.conf.urls import url
import MyBlog
from MyBlog import views
from django.urls import path, include

urlpatterns = [
    url(r'^$', MyBlog.views.home, name='home'),
    url(r'^users/$', MyBlog.views.show_users, name='users'),
    url(r'^articles/(?P<pk>\d+)/$', MyBlog.views.PostDetailView.as_view(), name='article'),
    url(r'^register/$', MyBlog.views.RegisterFormView.as_view(), name='registration'),
    url(r'^logout/$', MyBlog.views.logout_view, name='logout'),
    url(r'^MyBlog/login/$', MyBlog.views.LoginFormView.as_view(), name='login'),
    url(r'^add/$', MyBlog.views.AddArticle.as_view(), name='add'),
    url(r'^user/(?P<username>.+)/', MyBlog.views.show_user, name='user'),
    url(r'^tag/(?P<tag>[-\w]+)/$', MyBlog.views.home_by_tag, name='home_by_tag'),
    url(r'^search/$', MyBlog.views.home_by_keyword, name='home_by_keyword'),
    url(r'^friends/$', MyBlog.views.show_friends, name='friends'),
    url(r'^articles/(?P<article_id>[0-9]+)/delete/', views.delete),
    url(r'^articles/(?P<article_id>[0-9]+)/edit/', views.edit,name='edit'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends'),
]