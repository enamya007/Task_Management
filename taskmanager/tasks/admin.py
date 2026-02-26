from django.contrib import admin
from .models import Tache


@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display  = ('titre', 'priorite', 'statut', 'date_creation')
    list_filter   = ('statut', 'priorite')
    search_fields = ('titre', 'description')
    ordering      = ('-date_creation',)