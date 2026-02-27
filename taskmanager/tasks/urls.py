from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('', views.liste_taches, name='liste_taches'),
    path('ajouter/', views.ajouter_tache, name='ajouter_tache'),
    path('modifier/<int:pk>/', views.modifier_tache, name='modifier_tache'),
    path('supprimer/<int:pk>/', views.supprimer_tache, name='supprimer_tache'),
    path('toggle/<int:pk>/', views.toggle_statut, name='toggle_statut'),
]