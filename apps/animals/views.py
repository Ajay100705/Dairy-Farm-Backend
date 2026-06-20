from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Count, Avg
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta

from .models import (
    Animal, AnimalHealthRecord, AnimalWeightLog,
    BreedingRecord, CalvingRecord, AnimalNote 
)

from .serializers import (
    AnimalListSerializer,
    AnimalDetailSerializer,
    AnimalCreateSerializer,
    AnimalUpdateSerializer,
    AnimalHealthRecordSerializer,
    AnimalWeightLogSerializer,
    BreedingRecordSerializer,
    CalvingRecordSerializer,
    AnimalNoteSerializer,
    AnimalStatsSerializer,
    AnimalPedigreeSerializer,
)

from apps.accounts.permissions import (
    IsFarmMember, CanManageAnimals, IsOwner
)



class AnimalListView(generics.ListCreateAPIView):
    """
    Listing animals.
    """
    serializer_class = AnimalListSerializer
    permission_classes = [permissions.IsAuthenticated, IsFarmMember]
    
    def get_queryset(self):
        user = self.request.user
        
        # Get farms the user has access to
        if user.is_owner:
            farm_ids = user.owned_farms.filter(is_active=True).values_list('id', flat=True)
        else:
            farm_ids = user.farm_memberships.filter(
                is_active=True, status='active'
                ).values_list('farm_id', flat=True)
            
        queryset = Animal.objects.filter(farm_id__in=farm_ids)
        
        # Filter by farm
        farm_id = self.request.query_params.get('farm')
        if farm_id:
            queryset = queryset.filter(farm_id=farm_id)
        
        # Filter by species
        species = self.request.query_params.get('species')
        if species:
            queryset = queryset.filter(species=species)
        
        # Filter by breed
        breed = self.request.query_params.get('breed')
        if breed:
            queryset = queryset.filter(breed=breed)
        
        # Filter by status
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # Filter by gender
        gender = self.request.query_params.get('gender')
        if gender:
            queryset = queryset.filter(gender=gender)
        
        # Filter by pregnancy
        pregnant = self.request.query_params.get('pregnant')
        if pregnant is not None:
            queryset = queryset.filter(is_pregnant=pregnant.lower() == 'true')
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(tag_number__icontains=search) |
                Q(name__icontains=search)
            )
        
        return queryset.select_related('farm', 'mother', 'father').order_by('-created_at')
