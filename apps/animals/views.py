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
