from django.urls import path

from item import views
from item.views import CategoryUpdateView, LocationUpdateView

app_name = 'item'

urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
    path('new/', views.NewItem, name='new_item'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.EditItem, name='edit_item'),
    path('', views.items, name='items'),
    path('add_category/', views.add_categories, name='add_category'),
    path('category/<int:pk>/edit/', CategoryUpdateView.as_view(), name='edit_category'),
    path('<int:cat_id>/deleteCategory/', views.deleteCategory, name='deleteCategory'),
    path('add_location/', views.add_location, name='add_location'),
    path('location/<int:pk>/edit/', LocationUpdateView.as_view(), name='edit_location'),
    path('<int:loc_id>/deleteLocation/', views.deleteLocation, name='deleteLocation'),
    ]