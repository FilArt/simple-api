from django.contrib import admin
from . import models

admin.site.register(models.Category)
admin.site.register(models.Company)
admin.site.register(models.District)
admin.site.register(models.CompaniesGroup)


class CompanyInline(admin.TabularInline):
    model = models.ProductCompany
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = (CompanyInline,)


admin.site.register(models.Product, ProductAdmin)
