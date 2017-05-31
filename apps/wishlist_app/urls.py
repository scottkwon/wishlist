from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^process/$', views.process, name='process'),
    url(r'^login/$', views.login, name='login'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^wish_items/add/$', views.add_wishitem, name='add'),
    url(r'^wish_items/create/$', views.create_item, name='create'),
    url(r'^wish_items/(?P<id>\d+)/$', views.item_users, name='items'),
    url(r'^logout/$', views.logout)
]
