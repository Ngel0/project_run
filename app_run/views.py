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
from .models import Run
from .serializers import RunSerializer, UserSerializer

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

    def get_queryset(self):
        return Run.objects.select_related('athlete').all()

class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['last_name', 'first_name']
    ordering_fields = ['date_joined']

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
        return Response({'message':run.status}, status=status.HTTP_200_OK)
