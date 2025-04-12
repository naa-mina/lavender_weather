Weather Dashboard API
A Django Rest Framework based API that lets users register, login and get real time weather for cities using OpenWeatherMap

Features
- User registeration   POST  /api/register/
- login user  POST  /api/login/
- Get current weather for any city  GET  /api/weather/<city>/
- Save favorite cities per user  POST  /api/favorities/
- Get weather for all saved cities  GET  /api/favorities/
- logout user   POST  /api/logout

  Authentication
  SessionAuthentication for browser testing

Models
FavoriteCity
- user : links to the Django user
- city : CharField for city name
