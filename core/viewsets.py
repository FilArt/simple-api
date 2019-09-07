from rest_framework import mixins, viewsets

from . import models
from . import serializers


class CompanyViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = models.Company.objects.select_related('group')
    serializer_class = serializers.CompanySerializer


class ProductViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
