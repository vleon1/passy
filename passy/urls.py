from django.conf.urls import url

from . import views

app_name = 'passy'

urlpatterns = [
    url(r'^register', views.register, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^passwords/(?P<pk>[0-9]+)', views.PasswordView.as_view(), name='password'),
    url(r'^passwords', views.PasswordsView.as_view(), name='passwords'),
    url(r'^$', views.index, name='index'),
]
