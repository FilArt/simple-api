from rest_framework.routers import DefaultRouter
from . import viewsets as _viewsets

router = DefaultRouter()

router.register(r'companies', _viewsets.CompanyViewSet, base_name='companies')
router.register(r'products', _viewsets.ProductViewSet, base_name='products')
