from django.urls import path

from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index_d, name='index_d'),
    path('add_user/', views.add_user, name='add_user'),
    path('<int:user_id>/delete_user/', views.delete_user, name='delete_user'),
    path('<int:user_id>/edit_user/', views.edit_user, name='edit_user'),
    ]