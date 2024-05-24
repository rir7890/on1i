from django.urls import path
from .views import SignIn, SignUp, Home, HomePage, logout_view

urlpatterns = [
    path('', Home, name="home"),
    path('signIn/', SignIn, name="signin"),
    path('signUp/', SignUp, name="signup"),
    path('home-page/', HomePage, name="home-page"),
    path('logout/', logout_view, name='logout'),
]
