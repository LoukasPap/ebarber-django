from django.urls import path
from . import views
from ebarber.views import *

app_name = 'ebarber'
urlpatterns = [
    # ex: /ebarber/
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('bprof/', views.bprof, name='bprof'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]
