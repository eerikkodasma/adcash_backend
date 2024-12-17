from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Influencer, Employee
from .serializers import InfluencerSerializer, EmployeeSerializer

class InfluencerViewSet(viewsets.ModelViewSet):
    queryset = Influencer.objects.prefetch_related('social_media_accounts', 'manager')
    serializer_class = InfluencerSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['manager__id']
    search_fields = ['first_name', 'last_name', 'manager__first_name', 'manager__last_name']

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer