from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Run

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type']

    def get_type(self, obj):
        if obj.is_superuser:
            return 'admin'
        if obj.is_staff:
            return 'coach'
        return 'athlete'

class RunSerializer(serializers.ModelSerializer):
    athlete_data = UserSerializer(source='athlete', read_only=True)

    class Meta:
        model = Run
        fields = '__all__'
