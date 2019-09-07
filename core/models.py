from django.db import models


class _TitleModel(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class District(_TitleModel):
    ...


class Category(_TitleModel):
    ...


class CompaniesGroup(_TitleModel):
    ...


class Product(_TitleModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Company(_TitleModel):
    group = models.ForeignKey(CompaniesGroup, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    districts = models.ManyToManyField(District)
    products = models.ManyToManyField(Product, through='ProductCompany')


class ProductCompany(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        unique_together = ('company', 'product',)
