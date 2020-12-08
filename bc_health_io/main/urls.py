from django.urls import path

from . import views
from .views import ReceptionList, ReceptionDetail

urlpatterns = [
    path('list/', ReceptionList.as_view(), name='receptions'),
    path('<str:data_id>/', ReceptionDetail.as_view(), name="reception_detail"),
    path('<str:data_id>/mod', views.mod, name="reception_mod"),
]
