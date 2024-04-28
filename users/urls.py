from django.urls import path
from .views import SignIn, SignUp, Home

urlpatterns = [
    path('', Home, name="home"),
    path('signIn/', SignIn, name="signin"),
    path('signUp/', SignUp, name="signup"),
]
