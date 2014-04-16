from django.conf.urls import patterns, url

from marketplace import views

urlpatterns = patterns('',
    url(r'^$', views.dubai_home, name='dubai-home'),
    url(r'^motors/(?P<category>[-\w]+)/$', views.ad_listing, name='ad-listing'),
    url(r'^place-an-ad/taxonomy/(?P<ad_category>[-\w]+)/$', views.place_an_ad_select_category,
        name='place-an-ad-select-category'),
    url(r'^place-an-ad/taxonomy/(?P<ad_category>[-\w]+)/(?P<sub_category>[-\w]+)/$',
        views.place_an_ad_select_sub_category, name='place-an-ad-select-sub-category'),
    url(r'^place-an-ad/taxonomy/(?P<ad_category>[-\w]+)/(?P<sub_category>[-\w]+)/new/$', views.submit_ad,
        name='place-an-ad-new'),
)



