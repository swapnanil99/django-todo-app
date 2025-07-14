from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
   # path('', views.signup, name='signup'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('update-icon/', views.update_icon, name='update_icon'),
    path('logout/', views.logout_view, name='logout'),
    path('todo/', views.todo_view, name='todo'),
    path('add-task/', views.add_task, name='add_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('toggle-complete/<int:task_id>/', views.toggle_complete, name='toggle_complete'),

]
