from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Company, CompaniesGroup, Product, Category, ProductCompany, District


# noinspection DuplicatedCode
class OrganizationTests(APITestCase):
    def setUp(self) -> None:
        """
        Ensure we can filter and search in /organizations aep.
        """
        group1 = CompaniesGroup.objects.create(title='Test group 1')
        group2 = CompaniesGroup.objects.create(title='Test group 2')
        self.district1 = District.objects.create(title='Test district 1')
        self.company1 = Company.objects.create(
            group=group1,
            title='Test company 1',
            description='t1',
        )
        self.company2 = Company.objects.create(
            group=group2,
            title='Test company 2',
            description='t2',
        )

        self.company1.districts.add(self.district1)
        self.company2.districts.add(self.district1)

        category1 = Category.objects.create(title='Test category')
        self.product1 = Product.objects.create(title='Test product 1 (100)', category=category1)
        category2 = Category.objects.create(title='Test category')
        self.product2 = Product.objects.create(title='Test product 2 (200)', category=category2)

        ProductCompany.objects.bulk_create([
            ProductCompany(company=self.company1, product=self.product1, price=100),
            ProductCompany(company=self.company2, product=self.product2, price=200),
        ])

        self.district2 = District.objects.create(title='Test district 2')
        self.company3 = Company.objects.create(
            group=group2,
            title='Test company 3',
            description='t3',
        )
        self.company3.districts.add(self.district2)

    def test_list(self):
        response = self.client.get('/organizations/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [
            {'id': 1, 'products': [{'product': {'id': 1, 'title': 'Test product 1 (100)', 'category': 1}}],
             'title': 'Test company 1', 'description': 't1', 'group': {'id': 1, 'title': 'Test group 1'},
             'districts': [{'id': 1, 'title': 'Test district 1'}]},
            {'id': 2, 'products': [{'product': {'id': 2, 'title': 'Test product 2 (200)', 'category': 2}}],
             'title': 'Test company 2', 'description': 't2', 'group': {'id': 2, 'title': 'Test group 2'},
             'districts': [{'id': 1, 'title': 'Test district 1'}]}
        ])

        response = self.client.get('/organizations/2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [
            {'id': 3, 'products': [],
             'title': 'Test company 3', 'description': 't3', 'group': {'id': 2, 'title': 'Test group 2'},
             'districts': [{'id': 2, 'title': 'Test district 2'}]},
        ])

        response = self.client.get('/organizations/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_min_price(self):
        response = self.client.get('/organizations/1/?min_price=150')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [
            {'id': 2, 'products': [{'product': {'id': 2, 'title': 'Test product 2 (200)', 'category': 2}}],
             'title': 'Test company 2', 'description': 't2', 'group': {'id': 2, 'title': 'Test group 2'},
             'districts': [{'id': 1, 'title': 'Test district 1'}]}
        ])

    def test_filter_max_price(self):
        response = self.client.get('/organizations/1/?max_price=150')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [
            {'id': 1, 'products': [{'product': {'id': 1, 'title': 'Test product 1 (100)', 'category': 1}}],
             'title': 'Test company 1', 'description': 't1', 'group': {'id': 1, 'title': 'Test group 1'},
             'districts': [{'id': 1, 'title': 'Test district 1'}]},
        ])

    def test_filter_price(self):
        response = self.client.get('/organizations/1/?max_price=0')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_filter_category(self):
        for category_id in (1, 2):
            response = self.client.get(f'/organizations/1/?category={category_id}')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json(), [
                {'id': category_id, 'products': [
                    {'product': {
                        'id': category_id,
                        'title': f'Test product {category_id} ({category_id}00)',
                        'category': category_id}}
                ],
                 'title': f'Test company {category_id}',
                 'description': f't{category_id}',
                 'group': {'id': category_id, 'title': f'Test group {category_id}'},
                 'districts': [{'id': 1, 'title': 'Test district 1'}]},
            ])

    def test_non_existent_category(self):
        response = self.client.get('/organizations/1/?category=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])
