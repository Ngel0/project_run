from django.contrib import admin
from .models import Run, AthleteInfo, Challenge, Position, CollectibleItem

admin.site.register(Run)
admin.site.register(AthleteInfo)
admin.site.register(Challenge)
admin.site.register(Position)
admin.site.register(CollectibleItem)
