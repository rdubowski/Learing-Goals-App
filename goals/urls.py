from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.welcome_screen, name='welcome_screen'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard-table/', views.dashboard_table, name='dashboard_table'),
    path('create_goal/', views.create_goal, name='create_goal'),
    path('<int:pk>/delete_goal/', views.deleteGoal, name='delete_goal'),
    path('<int:pk>/change_goal_name/', views.changeGoalName, 
         name='change_goal_name'),
    path('<int:pk>/tasks/', views.learningGoalTasks, name='task_list_url'),
    path('tasks/<int:id>/completed/', views.TaskComplete,
         name='task_complete_url'),
    path('tasks/<int:id>/delete/', views.TaskDelete, name='task_delete_url'),
    # path('todo/<int:pk>', views.singleTodo, name='single-todo'),
    # path('add/', views.addTodo, name='add'),
    # path('complete/<int:pk>/', views.completeTodo, name='complete'),
    # path('uncomplete/<int:pk>/', views.uncompleteTodo, name='uncomplete'),
    # path('delete_complete/', views.deleteTodo, name='delete_complete'),
    # path('delete_all/', views.deleteAll, name='delete_all'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
         template_name="registration/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
         template_name="registration/password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(
         template_name="registration/password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(
         template_name="registration/password_reset_done.html"),
         name="password_reset_complete"),
]
