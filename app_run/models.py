from django.db import models
from django.conf import settings

class Run(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    athlete = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
