from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from accounts import views

urlpatterns = patterns('',
                       url(r'^register/$', views.RegisterView.as_view(), name='register'),
                       url(r'^profile/$', login_required(views.ProfileMainView.as_view()), name='profile'),
                       url(r'^login/$', views.LoginView.as_view(), name='login'),
                       url(r'^logout/$', views.logout, name='logout'),
)