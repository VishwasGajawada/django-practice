from django.conf.urls import url
from django.urls import path
from rango import views
# https://consideratecode.com/2018/05/02/django-2-0-url-to-path-cheatsheet/#:~:text=In%20Django%202.0%2C%20you%20use,converters%20to%20capture%20URL%20parameters.&text=path()%20always%20matches%20the,is%20passed%20to%20a%20view.

app_name = 'rango'
urlpatterns = [
    # url(r'^$',views.index,name="index"),
    path('',views.index,name="index"),
    url(r'^about',views.about,name="about",),
    path('category/<slug:category_name_slug>/',views.show_category,name="show_category"),
    path('add_category/',views.add_category,name="add_category"),
    path('category/<slug:category_name_slug>/add_page/',views.add_page,name="add_page"),
    

]
