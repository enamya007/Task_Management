from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tache
from .forms import TacheForm


# ── INSCRIPTION ───────────────────────────────────────────────
def inscription(request):
    if request.user.is_authenticated:
        return redirect('liste_taches')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f' Bienvenue {user.username} !')
            return redirect('liste_taches')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/inscription.html', {'form': form})


# ── CONNEXION ─────────────────────────────────────────────────
def connexion(request):
    if request.user.is_authenticated:
        return redirect('liste_taches')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f' Bonjour {user.username} !')
            return redirect('liste_taches')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/connexion.html', {'form': form})


# ── DÉCONNEXION ───────────────────────────────────────────────
def deconnexion(request):
    logout(request)
    messages.info(request, ' Vous avez été déconnecté.')
    return redirect('connexion')


# ── LISTE (chaque user voit UNIQUEMENT ses tâches) ────────────
@login_required
def liste_taches(request):
    taches = Tache.objects.filter(utilisateur=request.user)  # ← FILTRE CLÉ

    statut   = request.GET.get('statut', '')
    priorite = request.GET.get('priorite', '')
    if statut:
        taches = taches.filter(statut=statut)
    if priorite:
        taches = taches.filter(priorite=priorite)

    base = Tache.objects.filter(utilisateur=request.user)
    stats = {
        'total'    : base.count(),
        'en_cours' : base.filter(statut=Tache.STATUT_EN_COURS).count(),
        'terminees': base.filter(statut=Tache.STATUT_TERMINEE).count(),
        'haute_prio': base.filter(priorite=Tache.PRIORITE_HAUTE).count(),
    }
    return render(request, 'tasks/liste.html', {
        'taches': taches, 'stats': stats,
        'statut': statut, 'priorite': priorite,
    })


# ── AJOUTER ───────────────────────────────────────────────────
@login_required
def ajouter_tache(request):
    if request.method == 'POST':
        form = TacheForm(request.POST)
        if form.is_valid():
            tache = form.save(commit=False)
            tache.utilisateur = request.user   # ← on rattache l'utilisateur
            tache.save()
            messages.success(request, f' Tâche « {tache.titre} » créée !')
            return redirect('liste_taches')
    else:
        form = TacheForm()
    return render(request, 'tasks/form.html', {'form': form, 'action': 'Ajouter'})


# ── MODIFIER ──────────────────────────────────────────────────
@login_required
def modifier_tache(request, pk):
    # get_object_or_404 avec utilisateur=request.user → sécurité totale
    tache = get_object_or_404(Tache, pk=pk, utilisateur=request.user)
    if request.method == 'POST':
        form = TacheForm(request.POST, instance=tache)
        if form.is_valid():
            form.save()
            messages.success(request, f' Tâche modifiée !')
            return redirect('liste_taches')
    else:
        form = TacheForm(instance=tache)
    return render(request, 'tasks/form.html', {'form': form, 'action': 'Modifier', 'tache': tache})


# ── SUPPRIMER ─────────────────────────────────────────────────
@login_required
def supprimer_tache(request, pk):
    tache = get_object_or_404(Tache, pk=pk, utilisateur=request.user)
    if request.method == 'POST':
        tache.delete()
        messages.warning(request, ' Tâche supprimée.')
        return redirect('liste_taches')
    return render(request, 'tasks/confirmer_suppression.html', {'tache': tache})


# ── TOGGLE STATUT ─────────────────────────────────────────────
@login_required
def toggle_statut(request, pk):
    tache = get_object_or_404(Tache, pk=pk, utilisateur=request.user)
    if tache.est_terminee():
        tache.marquer_en_cours()
    else:
        tache.marquer_terminee()
    return redirect('liste_taches')