# Create your views here.
from django.shortcuts import get_object_or_404
from providers.models import Provider
from providers.serializers import ProviderSerializer

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import detail_route, list_route


# Create your views here.
class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    # /api/provider/{pk}/detail/
    @detail_route(methods=['get'])
    def detail(self, request, pk=None):
        provider = get_object_or_404(Provider, pk=pk)
        result = {
            'providerName': provider.providerName,
            'providerID': provider.providerID
        }

        return Response(result, status=status.HTTP_200_OK)

    # /api/provider/all_providerName/
    @list_route(methods=['get'])
    def all_providerName(self, request):
        provider = Provider.objects.values_list('providerName', flat=True).distinct()
        return Response(provider, status=status.HTTP_200_OK)
