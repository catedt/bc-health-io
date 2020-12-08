from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.index, name='reputation'),
    path('<str:data_id>/', views.detail, name="reputation_detail"),
    path('<str:data_id>/mod', views.mod, name="reputation_mod"),
]
