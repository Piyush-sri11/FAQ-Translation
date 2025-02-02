from rest_framework import viewsets
from .models import FAQ
from .serializers import FAQSerializer
from django.core.cache import cache
from rest_framework.response import Response

class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    """View to handle GET requests for FAQs."""
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    
    
