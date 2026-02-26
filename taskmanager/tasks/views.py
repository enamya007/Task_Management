from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Tache
from .forms import TacheForm


# ── 1. Liste des tâches ───────────────────────────────────────────────────────
def liste_taches(request):
    """Affiche toutes les tâches avec filtrage optionnel par statut / priorité."""
    taches = Tache.objects.all()

    # Filtres GET
    statut   = request.GET.get('statut', '')
    priorite = request.GET.get('priorite', '')

    if statut:
        taches = taches.filter(statut=statut)
    if priorite:
        taches = taches.filter(priorite=priorite)

    # Statistiques pour le tableau de bord
    stats = {
        'total'    : Tache.objects.count(),
        'en_cours' : Tache.objects.filter(statut=Tache.STATUT_EN_COURS).count(),
        'terminees': Tache.objects.filter(statut=Tache.STATUT_TERMINEE).count(),
        'haute_prio': Tache.objects.filter(priorite=Tache.PRIORITE_HAUTE).count(),
    }

    context = {
        'taches'  : taches,
        'stats'   : stats,
        'statut'  : statut,
        'priorite': priorite,
    }
    return render(request, 'tasks/liste.html', context)


# ── 2. Ajouter une tâche ──────────────────────────────────────────────────────
def ajouter_tache(request):
    """Crée une nouvelle tâche."""
    if request.method == 'POST':
        form = TacheForm(request.POST)
        if form.is_valid():
            tache = form.save()
            messages.success(request, f'✅ Tâche « {tache.titre} » créée avec succès !')
            return redirect('liste_taches')
    else:
        form = TacheForm()

    return render(request, 'tasks/form.html', {'form': form, 'action': 'Ajouter'})


# ── 3. Modifier une tâche ─────────────────────────────────────────────────────
def modifier_tache(request, pk):
    """Modifie une tâche existante."""
    tache = get_object_or_404(Tache, pk=pk)

    if request.method == 'POST':
        form = TacheForm(request.POST, instance=tache)
        if form.is_valid():
            form.save()
            messages.success(request, f'✏️ Tâche « {tache.titre} » modifiée !')
            return redirect('liste_taches')
    else:
        form = TacheForm(instance=tache)

    return render(request, 'tasks/form.html', {
        'form'  : form,
        'action': 'Modifier',
        'tache' : tache,
    })


# ── 4. Supprimer une tâche ────────────────────────────────────────────────────
def supprimer_tache(request, pk):
    """Supprime une tâche après confirmation."""
    tache = get_object_or_404(Tache, pk=pk)

    if request.method == 'POST':
        titre = tache.titre
        tache.delete()
        messages.warning(request, f'🗑️ Tâche « {titre} » supprimée.')
        return redirect('liste_taches')

    return render(request, 'tasks/confirmer_suppression.html', {'tache': tache})


# ── 5. Marquer terminée / en cours ────────────────────────────────────────────
def toggle_statut(request, pk):
    """Bascule le statut d'une tâche via méthode métier."""
    tache = get_object_or_404(Tache, pk=pk)

    if tache.est_terminee():
        tache.marquer_en_cours()
        messages.info(request, f'🔄 Tâche remise en cours.')
    else:
        tache.marquer_terminee()
        messages.success(request, f'🎉 Tâche marquée comme terminée !')

    return redirect('liste_taches')