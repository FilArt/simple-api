from rest_framework import serializers

from . import models


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        depth = 1
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class ProductCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCompany
        depth = 1
        fields = ('product',)


class OrganizationsSerializer(serializers.ModelSerializer):
    products = ProductCompanySerializer(many=True, source='productcompany_set')

    class Meta:
        model = models.Company
        depth = 1
        fields = '__all__'
