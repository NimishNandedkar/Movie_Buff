from django.contrib import admin
from django.urls import path, include 
from . import views




urlpatterns = [
    
    path('', views.index , name="index"),
    # path('movie/<int:movie_id>/', views.movie_view, name='movie_view'),
    path('movie/<int:movie_id>/', views.movie_view, name='movie_view'),
    path('search/',views.search,name='search'),
    path('signup/',views.handleSignup,name='handleSignup'),
    path('login/',views.handleLogin,name='handleLogin'),
    path('logout/',views.handleLogout,name='handleLogout'),
    path('loginError/',views.loginError,name='loginError'),
    
    path('watchLater/', views.watch_later_list, name='watch_later_list' ), 
    # path('add_to_watch_later/<int:movie_id>/', views.add_to_watch_later, name='add_to_watch_later'),
    path('add_to_watch_later/<str:movie_id>/', views.add_to_watch_later, name='add_to_watch_later'),
    path('remove_from_watch_later/<int:movie_id>/', views.remove_from_watch_later, name='remove_from_watch_later'),

    #below url is created on 20/10/23 yesterday

    path('profile/', views.view_profile, name='view_profile'),
    path('password_change/', views.change_password , name='change_password'),

    

    path('toggle-like/<int:movie_id>/', views.toggle_like, name='toggle_like'),
    path('most_popular/', views.most_popular, name='most_popular'),
    path('genre/<str:genre>/', views.genre_view, name='genre_view'),
    
]