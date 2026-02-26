from django import forms
from .models import Tache


class TacheForm(forms.ModelForm):
    """Formulaire Django pour créer / modifier une Tâche."""

    class Meta:
        model  = Tache
        fields = ['titre', 'description', 'statut', 'priorite']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Titre de la tâche…',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Description détaillée…',
            }),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'priorite': forms.Select(attrs={'class': 'form-select'}),
        }