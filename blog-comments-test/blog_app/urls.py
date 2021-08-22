from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('blog_detail/<str:pk>/',views.blog_detail,name="blog_detail"),
    path('add_blog', views.add_blog, name="add_blog"),
    path('blog_detail/<str:pid>/add_reply/<str:cid>', views.add_reply, name="add_reply")
]