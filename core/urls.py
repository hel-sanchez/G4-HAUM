from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views
from .forms import LoginForm
from .views import request_new_activation_link, login_required_redirect, send_email

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('login/', login_required_redirect(auth_views.LoginView.as_view(template_name='core/login.html',authentication_form=LoginForm)), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('request-activation-link/', request_new_activation_link, name='request_new_activation_link'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="core/password_reset.html"), name='password_reset'),
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name="core/password_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="core/password_rest_form.html"), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="core/password_reset_done.html"), name='password_reset_complete'),
    path('send_email/<str:subject>/<str:email>/<str:name>/', send_email, name='send_email'),
]