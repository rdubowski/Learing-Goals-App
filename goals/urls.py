from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.welcome_screen, name='welcome_screen'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update_profile/<int:pk>/', views.UpdateUser.as_view(),
         name='update_profile'),
    path('dashboard-table/', views.dashboard_table, name='dashboard_table'),
    path('create_goal/', views.create_goal, name='create_goal'),
    path('<int:pk>/delete_goal/', views.delete_goal, name='delete_goal'),
    path('<int:pk>/change_goal_name/', views.change_goal_name,
         name='change_goal_name'),
    path('<int:pk>/tasks/', views.learning_goal_tasks, name='task_list_url'),
    path('tasks/<int:id>/completed/', views.task_complete,
         name='task_complete_url'),
    path('tasks/<int:id>/delete/', views.task_delete, name='task_delete_url'),
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
