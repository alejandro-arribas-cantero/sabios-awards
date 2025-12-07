from django.db import models
from django.contrib.auth.models import User

class ActivityLog(models.Model):
    ACTION_TYPES = [
        ('VOTE', 'Voto Emitido'),
        ('ADMIN', 'Acción de Admin'),
        ('SYSTEM', 'Sistema'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.action_type}: {self.description}"

def log_activity(user, action_type, description):
    ActivityLog.objects.create(user=user, action_type=action_type, description=description)
