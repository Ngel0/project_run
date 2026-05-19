from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.conf import settings
from .models import Run
from .serializers import RunSerializer

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
