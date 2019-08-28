from django.urls import path,re_path
from blogs.views import UserView,Personal_Blogs_list,DetailView,BlogTypeView,ProxyView,StaticIndex

app_name='[blogs]'



urlpatterns = [
    re_path(r'^personal_center$',UserView.as_view(),name='personal_center'),
    re_path(r'^personal_blogs_list/(?P<page>\d+)*$',Personal_Blogs_list.as_view(),name='pblogs'),
    re_path(r'^detail/(?P<blog_id>\d+)$',DetailView.as_view(),name='detail'),
    re_path(r'^blogtype/(?P<page>.*)$',BlogTypeView.as_view(),name='blogtype'),
    re_path(r'^proxy/(?P<page>\d+)*$',ProxyView.as_view(),name='proxy'),
    re_path(r'^$',StaticIndex.as_view(),name='index')

]
