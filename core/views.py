import django_filters as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter

from . import models, serializers


class OrganizationFilterSet(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='productcompany__price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='productcompany__price', lookup_expr='lte')
    category = filters.NumberFilter(field_name='productcompany__product__category',
                                    lookup_expr='exact')

    class Meta:
        model = models.Company
        fields = ('min_price', 'max_price', 'category')


class OrganizationsList(generics.ListAPIView):
    serializer_class = serializers.OrganizationsSerializer
    filterset_class = OrganizationFilterSet
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('products__title', 'title')

    def get_queryset(self):
        qs = models.Company.objects.filter(districts=self.kwargs['district_pk']).distinct()
        if not qs.exists():
            raise NotFound
        return qs
