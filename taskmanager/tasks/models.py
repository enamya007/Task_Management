from django.db import models
from django.utils import timezone


class Tache(models.Model):
    """
    Classe représentant une Tâche — Principes POO appliqués :
    - Encapsulation : attributs définis avec types précis
    - Méthodes métier : marquer_terminee(), est_haute_priorite()
    - __str__ redéfini
    """

    # ── Choix (constantes de classe) ──────────────────────────────────────────
    STATUT_EN_COURS  = 'en_cours'
    STATUT_TERMINEE  = 'terminee'
    STATUT_CHOICES = [
        (STATUT_EN_COURS, 'En cours'),
        (STATUT_TERMINEE, 'Terminée'),
    ]

    PRIORITE_FAIBLE  = 'faible'
    PRIORITE_MOYENNE = 'moyenne'
    PRIORITE_HAUTE   = 'haute'
    PRIORITE_CHOICES = [
        (PRIORITE_FAIBLE,  'Faible'),
        (PRIORITE_MOYENNE, 'Moyenne'),
        (PRIORITE_HAUTE,   'Haute'),
    ]

    # ── Champs ────────────────────────────────────────────────────────────────
    titre        = models.CharField(max_length=200, verbose_name="Titre")
    description  = models.TextField(blank=True, verbose_name="Description")
    date_creation = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    statut       = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default=STATUT_EN_COURS,
        verbose_name="Statut"
    )
    priorite     = models.CharField(
        max_length=20,
        choices=PRIORITE_CHOICES,
        default=PRIORITE_MOYENNE,
        verbose_name="Priorité"
    )

    # ── Méta ──────────────────────────────────────────────────────────────────
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Tâche"
        verbose_name_plural = "Tâches"

    # ── Méthodes spéciales ────────────────────────────────────────────────────
    def __str__(self):
        return f"[{self.get_priorite_display()}] {self.titre} — {self.get_statut_display()}"

    # ── Méthodes métier ───────────────────────────────────────────────────────
    def marquer_terminee(self):
        """Marque la tâche comme terminée et sauvegarde."""
        self.statut = self.STATUT_TERMINEE
        self.save()

    def marquer_en_cours(self):
        """Remet la tâche en cours."""
        self.statut = self.STATUT_EN_COURS
        self.save()

    def est_terminee(self):
        """Retourne True si la tâche est terminée."""
        return self.statut == self.STATUT_TERMINEE

    def est_haute_priorite(self):
        """Retourne True si priorité haute."""
        return self.priorite == self.PRIORITE_HAUTE

    def couleur_priorite(self):
        """Retourne une classe CSS selon la priorité."""
        mapping = {
            self.PRIORITE_FAIBLE:  'priorite-faible',
            self.PRIORITE_MOYENNE: 'priorite-moyenne',
            self.PRIORITE_HAUTE:   'priorite-haute',
        }
        return mapping.get(self.priorite, '')