from django.urls import include, path
from rest_framework import routers
from .views import InfluencerViewSet, EmployeeViewSet

router = routers.DefaultRouter()
router.register(r'influencers', InfluencerViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
