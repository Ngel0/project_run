from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Run

User = get_user_model()

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']

class UserSerializer(BaseUserSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type', 'runs_finished']

    def get_type(self, obj):
        if obj.is_superuser:
            return 'admin'
        if obj.is_staff:
            return 'coach'
        return 'athlete'
    
    def get_runs_finished(self, obj):
        return len(obj.run_set.filter(status='finished'))

class RunSerializer(serializers.ModelSerializer):
    athlete_data = BaseUserSerializer(source='athlete', read_only=True)

    class Meta:
        model = Run
        fields = '__all__'
