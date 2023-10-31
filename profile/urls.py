from django.urls import path, re_path

from profile import views

urlpatterns = [
    re_path(r'^(?P<username>[\w.@+-]+)/$', views.profile, name='profile'),
    path('profile/<str:username>/upvote/', views.upvote, name='upvote'),
    path('profile/<str:username>/downvote/', views.downvote, name='downvote'),
]