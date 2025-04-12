
from django.urls import path
from . import views  #allows to import all the functions


urlpatterns = [
    path('weather/<str:city>/',views.get_weather),   # GET weather for a city
    path('register/',views.register),                # POST to register user
    path('login/', views.login),                     #POST to login                                           
    path('logout/', views.logout_view),                  #POST to logout
    path('favorites/', views.favorite_cities),      #GET/POST favorite cities
]
