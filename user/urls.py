from django.urls import path,re_path
from user.views import IndexView,LoginView,RegisterView,LogoutView,ActiveView

app_name='[user]'
urlpatterns = [
    re_path(r'^index/(?P<page>\d+)*$',IndexView.as_view(),name='index'),
    re_path(r'^login$',LoginView.as_view(),name='login'),
    re_path(r'^register$',RegisterView.as_view(),name='register'),
    re_path(r'^logout$',LogoutView.as_view(),name='logout'),
    re_path(r'active/(?P<token>.*)',ActiveView.as_view(),name='active')
]
