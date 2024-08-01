from django.urls import path
from .views import SignIn, SignUp, Home, HomePage, logout_view, linked_view, public_link, track_click, DashBoardView

urlpatterns = [
    path('', Home, name="home"),
    path('signIn/', SignIn, name="signin"),
    path('signUp/', SignUp, name="signup"),
    path('home-page/', HomePage, name="home-page"),
    path('logout/', logout_view, name='logout'),
    path('linked-view/', linked_view, name="link-view"),
    path('public-link/<str:user_name>/',
         public_link, name="public-link"),
    path('click/<str:profile_id>/', track_click, name="track-click"),
    path('dashboard/', DashBoardView, name="dashboard"),
]
