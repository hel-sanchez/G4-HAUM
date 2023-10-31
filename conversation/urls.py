from django.urls import path

from conversation import views

app_name= 'conversation'

urlpatterns = [
    path('new/<int:item_pk>/', views.new_conversation, name='new_conversation'),
    path('', views.inbox, name='inbox'),
    path('<int:pk>/', views.detail_conversation, name='detail_conversation'),
    path('delete/<int:pk>/', views.delete_conversation, name='delete_conversation'),
]