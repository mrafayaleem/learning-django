from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from marketplace import views

urlpatterns = patterns('',
                       url(r'^$', views.dubai_home, name='dubai-home'),

                       url(r'^motors/(?P<category>[-\w]+)/$', views.ad_listing, name='ad-listing'),

                       url(r'^place-an-ad/taxonomy/motors/$', login_required(views.MotorCategoryDisplayView.as_view()),
                           name='motor-category'),

                       url(r'^place-an-ad/taxonomy/motors/(?P<sub_category>[-\w]+)/$',
                           login_required(views.MotorMakeDisplayView.as_view()),
                           name='motor-make'),

                       url(r'^place-an-ad/taxonomy/motors/(?P<sub_category>[-\w]+)/(?P<make>[-\w]+)/$',
                           login_required(views.MotorModelDisplayView.as_view()),
                           name='motor-model'),

                       url(
                           r'^place-an-ad/taxonomy/motors/(?P<sub_category>[-\w]+)/(?P<make>[-\w]+)/(?P<model>[-\w]+)/$',
                           login_required(views.MotorAdRedirectView.as_view()),
                           name='motor-ad-redirect'),

                       url(r'^place-an-ad/motors/(?P<sub_category>[-\w]+)/(?P<make>[-\w]+)/(?P<model>[-\w]+)/new/$',
                           login_required(views.MotorAdFormView.as_view()),
                           name='motor-ad-form'),


                       # url(r'^place-an-ad/taxonomy/(?P<ad_category>[-\w]+)/(?P<sub_category>[-\w]+)/$',
                       #     views.place_an_ad_select_sub_category, name='place-an-ad-select-sub-category'),
                       # url(r'^place-an-ad/taxonomy/(?P<ad_category>[-\w]+)/(?P<sub_category>[-\w]+)/new/$', views.submit_ad,
                       #     name='place-an-ad-new'),
)



