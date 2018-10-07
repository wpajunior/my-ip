from django.urls import path
from . import views

app_name='myip'

urlpatterns = [
    path('', views.index, name='index')
]