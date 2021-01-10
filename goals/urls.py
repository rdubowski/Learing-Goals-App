from django.urls import path
from . import views
urlpatterns = [
    path('', views.welcome_screen, name='welcome_screen'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dasboard/', views.dasboard, name='dasboard'),
    
    # path('todo/<int:pk>', views.singleTodo, name='single-todo'),
    # path('add/', views.addTodo, name='add'),
    # path('complete/<int:pk>/', views.completeTodo, name='complete'),
    # path('uncomplete/<int:pk>/', views.uncompleteTodo, name='uncomplete'),
    # path('delete_complete/', views.deleteTodo, name='delete_complete'),
    # path('delete_all/', views.deleteAll, name='delete_all'),
]
