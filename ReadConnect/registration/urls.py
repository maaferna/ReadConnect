from django.urls import path
from .views import *
from allauth.account.views import LoginView, LogoutView, SignupView, PasswordResetView

urlpatterns = [
    path('login/', view_login, name='login'),
    path('logout/', view_logout, name="logout"),
    path('register/', view_register, name="register"),
    path('contact/', contact_view, name='contact_me'),
    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'),
    path('accounts/signup/', SignupView.as_view(), name='account_signup'),
    path('accounts/password/reset/', PasswordResetView.as_view(), name='account_reset_password'),
    path('accounts/profile/', profile_view, name='profile_view'),
    path('accounts/google/login/', CustomGoogleOAuth2LoginView, name='custom_google_login'),

]