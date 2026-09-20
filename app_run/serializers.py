from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Run, Position

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

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

    def validate(self, data):
        run = Run.objects.filter(id=data.get('run')).first()
        latitude = data.get('latitude')
        longtitude = data.get('longtitude')
        if run is None:
            raise serializers.ValidationError({'run':'run does not exist'})
        if run.status != 'in_progress':
            raise serializers.ValidationError({'run':'the run is not in progress'})
        if latitude is None or latitude < -90.0 or latitude > 90.0:
            return serializers.ValidationError({'latitude':'invalid number'})
        if longtitude is None or longtitude < -180.0 or longtitude > 180.0:
            return serializers.ValidationError({'longtitude':'invalid number'})
        return data
