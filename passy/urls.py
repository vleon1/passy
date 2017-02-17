from django.conf.urls import url

from . import views

app_name = 'passy'

urlpatterns = [
    url(r'^register', views.register, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^passwords/(?P<site>\w+)', views.password, name='password'),
    url(r'^passwords', views.passwords, name='passwords'),
    url(r'^$', views.index, name='index'),
]
