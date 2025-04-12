import requests
import os
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout as django_logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import FavoriteCity
from .serializers import RegisterSerializer, FavoriteCitySerializer
from .utils import get_weather_data


# Register a new user
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key}, status=201)
    return Response(serializer.errors, status=400)


# Log in a user
@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
    return Response({"error": "Invalid credentials"}, status=401)


# Log out (only works with SessionAuthentication in browser)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    django_logout(request)
    return Response({"message": "Logged out successfully."})


# Get weather for a city
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_weather(request, city):
    data = get_weather_data(city)
    if data:
        return Response({
            "city": data["name"],
            "country": data["sys"].get("country", "Unknown"),
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        })
    return Response({"error": "City not found"}, status=404)


# Save or list favorite cities
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def favorite_cities(request):
    if request.method == 'POST':
        serializer = FavoriteCitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    if request.method == 'GET':
        cities = FavoriteCity.objects.filter(user=request.user)
        data = []
        for fav in cities:
            weather = get_weather_data(fav.city)
            if weather:
                data.append({
                    "city": fav.city,
                    "country": weather["sys"].get("country"),
                    "temperature": weather["main"]["temp"],
                    "description": weather["weather"][0]["description"]
                })
            else:
                data.append({
                    "city": fav.city,
                    "error": "Weather data unavailable"
                })
        return Response(data)
