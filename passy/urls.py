from django.conf.urls import url

from passy import views


app_name = 'passy'


urlpatterns = [
    url(r'^register', views.RegisterView.as_view(), name='register'),
    url(r'^login', views.LoginView.as_view(), name='login'),
    url(r'^logout', views.LogoutView.as_view(), name='logout'),
    url(r'^passwords/(?P<pk>[0-9]+)', views.PasswordView.as_view(), name='password'),
    url(r'^passwords/get_random', views.GetRandomPasswordView.as_view(), name='get_random_password'),
    url(r'^passwords', views.PasswordListView.as_view(), name='password_list'),
    url(r'^$', views.IndexView.as_view(), name='index'),
]
