from rest_framework import serializers
from django.db.models.aggregates import Avg
from django.contrib.auth import get_user_model
from .models import Run, Position, CollectibleItem, Subscribe

User = get_user_model()

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']

class UserSerializer(BaseUserSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type', 'runs_finished', 'rating']

    def get_type(self, obj):
        if obj.is_superuser:
            return 'admin'
        if obj.is_staff:
            return 'coach'
        return 'athlete'
    
    def get_runs_finished(self, obj):
        try:
            return obj.runs_finished
        except AttributeError:
            return 0

    def get_rating(self, obj):
        return obj.subscribers.aggregate(Avg('rating'))['rating__avg'] or None

class UserAthleteDetailSerializer(UserSerializer):
    items = serializers.SerializerMethodField()
    coach = serializers.SerializerMethodField()
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['items', 'coach']

    def get_items(self, obj):
        return CollectibleItemSerializer(obj.items.all(), many=True).data

    def get_coach(self, obj):
        return obj.subscribtions.values_list('coach_id', flat=True).first()

class UserCoachDetailSerializer(UserSerializer):
    items = serializers.SerializerMethodField()
    athletes = serializers.SerializerMethodField()
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['items', 'athletes']

    def get_items(self, obj):
        return CollectibleItemSerializer(obj.items.all(), many=True).data

    def get_athletes(self, obj):
        return obj.subscribers.values_list('athlete_id', flat=True)

class RunSerializer(serializers.ModelSerializer):
    athlete_data = BaseUserSerializer(source='athlete', read_only=True)

    class Meta:
        model = Run
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    date_time = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f')

    class Meta:
        model = Position
        fields = '__all__'

    def validate(self, data):
        run = Run.objects.filter(id=data.get('run')).first()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        if run is None:
            raise serializers.ValidationError({'run':'run does not exist'})
        if run.status != 'in_progress':
            raise serializers.ValidationError({'run':'the run is not in progress'})
        if latitude is None or latitude < -90.0 or latitude > 90.0:
            raise serializers.ValidationError({'latitude':'invalid number'})
        if longitude is None or longitude < -180.0 or longitude > 180.0:
            raise serializers.ValidationError({'longitude':'invalid number'})
        return data

class CollectibleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectibleItem
        fields = ['name', 'uid', 'latitude', 'longitude', 'picture', 'value']

    def validate(self, data):
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        if latitude is None or latitude < -90.0 or latitude > 90.0:
            raise serializers.ValidationError({'latitude':'invalid number'})
        if longitude is None or longitude < -180.0 or longitude > 180.0:
            raise serializers.ValidationError({'longitude':'invalid number'})
        return data
