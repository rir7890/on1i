from django.urls import path
from .views import SignIn, SignUp, Home, HomePage

urlpatterns = [
    path('', Home, name="home"),
    path('signIn/', SignIn, name="signin"),
    path('signUp/', SignUp, name="signup"),
    path('home-page/', HomePage, name="home-page")
]
