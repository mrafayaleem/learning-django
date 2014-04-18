from django.conf.urls import patterns, url

from accounts import views

urlpatterns = patterns('',
                       url(r'^register/$',  views.register, name='register'),
                       url(r'^profile/$', views.profile, name='profile'),
                       url(r'^login/$', views.LoginView.as_view(), name='login'),
                       url(r'^logout/$', views.logout, name='logout'),
)