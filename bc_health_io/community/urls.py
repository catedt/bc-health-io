from django.urls import path
from community import views

urlpatterns = [
    path('list', views.index, name='community'),
]