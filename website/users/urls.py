from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.list_all_users, name='list_all_users'),
    url(r'sign_up/', views.sign_up, name='sign_up'),
    url(r'sign_in/', views.sign_in, name='sign_in'),
    url(r'update/(?P<data>\w+)', views.update, name='update'),
    url(r'delete/(?P<data>\w+)', views.delete, name='delete'),
]
