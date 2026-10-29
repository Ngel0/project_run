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
    distance = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)

class AthleteInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goals = models.CharField(max_length=200, null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)

class Challenge(models.Model):
    full_name = models.CharField(max_length=50)
    athlete = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Position(models.Model):
    run = models.IntegerField()
    latitude = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)

class CollectibleItem(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=50, unique=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    picture = models.URLField(null=True, blank=True)
    value = models.IntegerField(null=True, blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='items')
