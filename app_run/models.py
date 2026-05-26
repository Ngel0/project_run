from django.db import models
from django.conf import settings

class Run(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    athlete = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    STATUS_CHOICES = [
        ('init', 'Забег инициализирован'),
        ('in_progress', 'Забег начат'),
        ('finished', 'Забег закончен')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='init')

class AthleteInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goals = models.CharField(max_length=200, null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
