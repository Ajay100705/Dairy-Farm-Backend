from django.urls import path
from . import views

urlspatterns = [
    # Animal CRUD
    path('', views.AnimalListView.as_view(), name='animal-list'),
    path('create/', views.AnimalCreateView.as_view(), name='animal-create'),
    path('<int:pk>/', views.AnimalDetailView.as_view(), name='animal-detail'),
    path('<int:pk>/update/', views.AnimalUpdateView.as_view(), name='animal-update'),
    path('<int:pk>/delete/', views.AnimalDeleteView.as_view(), name='animal-delete'),
    
    # Animal Details
    path('<int:pk>/pedigree/', views.animal_pedigree, name='animal-pedigree'),
    path('<int:pk>/weight-history/', views.animal_weight_history, name='animal-weight-history'),
    path('<int:pk>/mark-sold/', views.mark_animal_sold, name='animal-mark-sold'),
    path('<int:pk>/mark-deceased/', views.mark_animal_deceased, name='animal-mark-deceased'),
    
    # Health Records
    path('<int:animal_pk>/health-records/', views.AnimalHealthRecordListView.as_view(), name='health-record-list'),
    path('<int:animal_pk>/health-records/<int:pk>/', views.AnimalHealthRecordDetailView.as_view(), name='health-record-detail'),
    
    # Weight Logs
    path('<int:animal_pk>/weight-logs/', views.AnimalWeightLogListView.as_view(), name='weight-log-list'),
    path('<int:animal_pk>/weight-logs/<int:pk>/', views.AnimalWeightLogDetailView.as_view(), name='weight-log-detail'),
    
    # Notes
    path('<int:animal_pk>/notes/', views.AnimalNoteListView.as_view(), name='animal-note-list'),
    path('<int:animal_pk>/notes/<int:pk>/', views.AnimalNoteDetailView.as_view(), name='animal-note-detail'),
    
    # Breeding Records
    path('<int:farm_pk>/breeding/', views.BreedingRecordListView.as_view(), name='breeding-record-list'),
    path('<int:farm_pk>/breeding/<int:pk>/', views.BreedingRecordDetailView.as_view(), name='breeding-record-detail'),
    
    # Calving Records
    path('<int:farm_pk>/calving/', views.CalvingRecordListView.as_view(), name='calving-record-list'),
    path('<int:farm_pk>/calving/<int:pk>/', views.CalvingRecordDetailView.as_view(), name='calving-record-detail'),
    
    # Stats & Choices
    path('stats/', views.animal_stats, name='animal-stats'),
    path('breeds/', views.get_breed_choices, name='breed-choices'),
]