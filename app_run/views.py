from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Run, AthleteInfo, Challenge, Position
from .serializers import RunSerializer, UserSerializer, PositionSerializer
from .paginations import RunPagination, UserPagination, PositionPagination

User = get_user_model()

@api_view(['GET'])
def company_details(request):
    return Response({
            'company_name':settings.COMPANY_NAME,
            'slogan':settings.SLOGAN,
            'contacts':settings.CONTACTS
        })

class RunViewSet(ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['athlete', 'status']
    ordering_fields = ['created_at']
    pagination_class = RunPagination

    def get_queryset(self):
        return Run.objects.select_related('athlete').all()

class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['last_name', 'first_name']
    ordering_fields = ['date_joined']
    pagination_class = UserPagination

    def get_queryset(self):
        qs = self.queryset.filter(is_superuser=False) #сразу исключаем админов
        type = self.request.query_params.get('type', None)
        if type == 'coach':
            return qs.filter(is_staff=True)
        if type == 'athlete':
            return qs.filter(is_staff=False)
        return qs

class StartRunView(APIView):
    def post(self, request, id):
        run = get_object_or_404(Run, id=id)
        if run.status != 'init':
            return Response({'message':'Can not start the run'}, status=status.HTTP_400_BAD_REQUEST)
        run.status = 'in_progress'
        run.save()
        return Response({'message':run.status}, status=status.HTTP_200_OK)

class StopRunView(APIView):
    def post(self, request, id):
        run = get_object_or_404(Run, id=id)
        if run.status != 'in_progress':
            return Response({'message':'Can not stop the run'}, status=status.HTTP_400_BAD_REQUEST)
        run.status = 'finished'
        run.save()
        if Run.objects.filter(athlete=run.athlete, status='finished').count() >= 10:
            Challenge.objects.create(full_name='Сделай 10 Забегов!', athlete=run.athlete)
        return Response({'message':run.status}, status=status.HTTP_200_OK)

class AthleteInfoView(APIView):
    def get(self, request, user_id):
        athlete = get_object_or_404(User, id=user_id)
        athlete_info, created = AthleteInfo.objects.get_or_create(user=athlete)
        data = {
            'goals': athlete_info.goals,
            'weight': athlete_info.weight,
            'user_id': user_id,
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        athlete = get_object_or_404(User, id=user_id)
        weight = request.data.get('weight')
        if weight is not None:
            try:
                weight = int(weight)
            except (ValueError):
                return Response({'message': 'Invalid weight value'}, status=status.HTTP_400_BAD_REQUEST)
            if weight <= 0 or weight >= 900:
                return Response({'message': 'Invalid weight value'}, status=status.HTTP_400_BAD_REQUEST)
        athlete_info, created = AthleteInfo.objects.update_or_create(user=athlete, defaults={
            'goals': request.data.get('goals'),
            'weight': weight
        })
        data = {
            'goals': athlete_info.goals,
            'weight': athlete_info.weight,
            'user_id': user_id,
        }
        return Response(data, status=status.HTTP_201_CREATED)

class ChallengesView(APIView):
    def get(self, request):
        athlete_id = request.GET.get('athlete')
        if athlete_id is None:
            queryset = Challenge.objects.all()
        else:
            try:
                athlete_id = int(athlete_id)
            except(ValueError):
                return Response({'message': 'Invalid athlete id'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = list(Challenge.objects.filter(athlete=athlete_id))
        data = []
        for challenge in queryset:
            item = {'full_name': challenge.full_name, 'athlete': challenge.athlete.id}
            data.append(item)
        return Response(data, status=status.HTTP_200_OK)

class PositionViewSet(ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['run']
    pagination_class = PositionPagination

    #get по run id
    # def get_queryset(self):
    #     qs = self.queryset.all()
    #     run = self.request.query_params.get('run', None)
    #     if run:
    #         qs = qs.filter(run=run)
    #     return qs
