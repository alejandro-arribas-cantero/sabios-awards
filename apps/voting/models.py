from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class VotingPeriod(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Abierta'),
        ('CLOSED', 'Cerrada'),
        ('REVEALED', 'Resultados Públicos'),
    ]

    TYPE_CHOICES = [
        ('MVP_MONTH', 'MVP del Mes'),
        ('THE_BEST_CUATRI_1', 'The Best of the Cuatri 1 (Sep-Dic)'),
        ('THE_BEST_CUATRI_2', 'The Best of the Cuatri 2 (Ene-May)'),
        ('BALON_ORO', 'Balón de Oro del Curso'),
        ('PUSKAS', 'Puskas'),
        ('BOTA_ORO_ANO', 'Bota de Oro del Año'),
    ]

    month = models.IntegerField()
    year = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    voting_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='MVP_MONTH', verbose_name="Tipo de Votación")
    winner_photo = models.ImageField(upload_to='winners/', blank=True, null=True)
    manual_winner = models.ForeignKey('Candidate', on_delete=models.SET_NULL, null=True, blank=True, related_name='won_periods', verbose_name="Ganador Manual")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('month', 'year', 'voting_type')
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.get_voting_type_display()} - {self.month}/{self.year} - {self.get_status_display()}"

    @property
    def month_name(self):
        import calendar
        # Set locale to Spanish if possible, or just use a manual mapping for simplicity and reliability
        months = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        return months.get(self.month, str(self.month))

    def get_winner_candidate(self):
        if self.manual_winner:
            return self.manual_winner
            
        from django.db.models import Count
        if not hasattr(self, '_winner_candidate'):
            self._winner_candidate = self.candidates.annotate(num_votes=Count('votes')).order_by('-num_votes').first()
        return self._winner_candidate

    @property
    def resolved_winner_photo(self):
        if self.winner_photo:
            return self.winner_photo
        winner = self.get_winner_candidate()
        if winner and winner.photo_winner:
            return winner.photo_winner
        # Fallback to standard photo if no winner photo
        if winner and winner.photo:
            return winner.photo
        return None

class Candidate(models.Model):
    period = models.ForeignKey(VotingPeriod, on_delete=models.CASCADE, related_name='candidates')
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='candidates/')
    photo_winner = models.ImageField(upload_to='candidates/winners/', blank=True, null=True, verbose_name="Foto Ganador")
    nomination_reason = models.TextField(blank=True, null=True, verbose_name="Motivo de Nominación")
    
    def __str__(self):
        return f"{self.name} ({self.period})"
    
    @property
    def vote_count(self):
        return self.votes.count()

    @property
    def percentage(self):
        total_votes = self.period.votes.count()
        if total_votes == 0:
            return 0
        return (self.votes.count() / total_votes) * 100

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    period = models.ForeignKey(VotingPeriod, on_delete=models.CASCADE, related_name='votes')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'period')

    def save(self, *args, **kwargs):
        if self.period.status != 'OPEN':
            raise ValidationError("La votación no está abierta.")
        if self.candidate.period != self.period:
            raise ValidationError("Este candidato no pertenece a la votación actual.")
        super().save(*args, **kwargs)
