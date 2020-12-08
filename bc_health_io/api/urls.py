from django.urls import include, path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'hbblock', views.HbBlockDataSet)
router.register(r'doctors', views.DoctorDataSet)
router.register(r'clients', views.ClientDataSet)
router.register(r'mediator', views.MediatorDataSet)
router.register(r'contract', views.SmartContractDataSet)
router.register(r'reputations', views.ReputationViewSet)
router.register(r'receptions', views.ReceptionViewSet)


urlpatterns = [
    path('deploy/reception', views.DeployReception.as_view(), name='deploy_reception'),
    path('deploy/reputation', views.DeployReputation.as_view(), name='deploy_reputation'),
    path('transact/reputation_init', views.TransactReputationInit.as_view(), name='reputation_init'),
    path('transact/reputation_scoring', views.TransactReputationAdd.as_view(), name='reputation_scoring'),
    path('transact/reception', views.TransactReception.as_view(), name='transact_reception'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
