from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from django.conf import settings
from django.contrib.auth import get_user_model
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

    def get_queryset(self):
        return Run.objects.select_related('athlete').all()

class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['last_name', 'first_name']

    def get_queryset(self):
        qs = self.queryset.filter(is_superuser=False) #сразу исключаем админов
        type = self.request.query_params.get('type', None)
        if type == 'coach':
            return qs.filter(is_staff=True)
        if type == 'athlete':
            return qs.filter(is_staff=False)
        return qs
