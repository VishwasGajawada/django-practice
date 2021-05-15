from django.urls import path
from tasks import views
urlpatterns = [

    path('',views.index,name="list"),
    path('update_task/<str:pk>/',views.updateTask,name="update_task"),
    path('delete/<str:pk>/',views.deleteTask,name="delete_task"),
    path('save_changes/<str:pk>/',views.saveChanges,name="save_changes"),
]