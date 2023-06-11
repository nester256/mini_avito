from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.status import HTTP_200_OK as OK
from django.test.client import Client as APIClient
from string import ascii_lowercase as letters
from mini_avito_app import models


def create_view_tests(url, page_name, template):
    class ViewTests(TestCase):

        def setUp(self):
            self.client = APIClient()
            default = letters[:10]
            self.user = User.objects.create_user(
                username=default,
                password=default
            )
            models.Client.objects.create(
                user=self.user,
                address='г. Липецк, ул. Неделена, д. 3',
                full_name=f'{self.user.first_name} {self.user.last_name}',
                phone='88005553535',
                mail=f'{self.user.email}'
            )
            self.client.login(username=default, password=default)

        def test_view_exists_at_url(self):
            self.assertEqual(self.client.get(url).status_code, OK)

        def test_view_exists_by_name(self):
            self.assertEqual(self.client.get(
                reverse(page_name)).status_code, OK)

        def test_view_uses_template(self):
            resp = self.client.get(reverse(page_name))
            self.assertEqual(resp.status_code, OK)
            self.assertTemplateUsed(resp, template)
            self.assertTemplateUsed(resp, 'base.html')

    return ViewTests


HomePageViewTests = create_view_tests(
    '/',
    'homepage',
    'app/index.html'
)

RegisterPageViewTests = create_view_tests(
    '/accounts/register/',
    'register',
    'accounts/register.html'
)

LoginPageViewTests = create_view_tests(
    '/accounts/login/',
    'login',
    'accounts/login.html'
)

ProfilePageViewTests = create_view_tests(
    '/profile/',
    'profile',
    'app/profile.html'
)

ProductsListPageViewTests = create_view_tests(
    '/product_list/',
    'product_list',
    'app/products_list.html'
)

OrdersListPageViewTests = create_view_tests(
    '/my_orders/',
    'my_orders',
    'app/my_orders.html'
)

MyProductsPageViewTests = create_view_tests(
    '/my_products/',
    'my_products',
    'app/my_products.html'
)

MySalesPageViewTests = create_view_tests(
    '/my_sales/',
    'my_sales',
    'app/my_sales.html'
)

CreateProductPageViewTests = create_view_tests(
    '/create_product/',
    'create_product',
    'app/create_product.html'
)
