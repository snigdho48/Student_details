from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from Main_app import views

urlpatterns = [
    path('accounts/login/',views.login,name='login'),
    path('accounts/register/',views.register,name='register'),
    path('student/list/', views.show_list, name='show_list'),
    path('logout/', views.logout, name='logout'),
    path('list/',views.show,name='show'),
    path("delete/<int:id>/", views.delete, name='delete'),
    path("update/<int:id>/", views.update, name='update'),

    path('password_reset_form/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset_form'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),


]