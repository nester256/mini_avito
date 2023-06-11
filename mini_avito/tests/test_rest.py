"""Tests for CRUD."""
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status
from mini_avito_app.serializers import *
from mini_avito_app.models import *
from rest_framework.authtoken.models import Token
import json

# from mini_avito.mini_avito_app.models import Client


def create_viewset_tests(
    url: str,
    cls_model: models.Model,
    cls_serializer: serializers.ModelSerializer,
    request_content: dict,
    to_change: dict,
):
    class ViewSetTests(APITestCase):

        def setUp(self):
            self.user = User.objects.create_user(
                is_superuser=True,
                id=1,
                username='test',
                first_name='test',
                last_name='test',
                email='test@mail.ru',
                password='test'
            )
            token = Token.objects.create(user=self.user)
            self.client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
            self.model = cls_model.objects.create(**request_content)

        def test_create_model(self):
            """Test for creating module."""
            response = self.client.post(url, data=request_content)
            serializer = cls_serializer(data=request_content)
            self.assertTrue(serializer.is_valid())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_get_model(self):
            """Test for getting module."""
            url_to_get = f'{url}{self.model.id}/'
            response = self.client.get(url_to_get)
            serializer = cls_serializer(data=request_content)
            self.assertTrue(serializer.is_valid())
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_update_model(self):
            """Test for updating module."""
            url_to_update = f'{url}{self.model.id}/'
            response = self.client.put(
                url_to_update,
                data=json.dumps(to_change),
                content_type='application/json'
            )
            serializer = cls_serializer(data=to_change)
            self.assertTrue(serializer.is_valid())
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_delete_model(self):
            """Test for deliting module."""
            url_to_delete = f'{url}{self.model.id}/'
            response = self.client.delete(url_to_delete)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertFalse(
                cls_model.objects.filter(id=self.model.id).exists()
            )

    return ViewSetTests


ClientTests = create_viewset_tests(
    '/rest/Category_product/',
    Category_products,
    Category_productsSerializer,
    {
        'cp_name': "Недвижимость"
    },
    {
        'cp_name': "Движимость"
    }
)


class ClientTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            is_superuser=True,
            id=1,
            username='test',
            first_name='test',
            last_name='test',
            email='test@mail.ru',
            password='test'
        )
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.request_data = {
            'user': f'{self.user.id}',
            'address': 'г. Липецк, ул. Неделена, д. 3',
            'full_name': f'{self.user.first_name} {self.user.last_name}',
            'phone': '88005553535',
            'mail': f'{self.user.email}'
        }
        user = User.objects.create(
            is_superuser=True,
            id=2,
            username='test1',
            first_name='test1',
            last_name='test1',
            email='test1@mail.ru',
            password='test1'
        )
        self.model = Client.objects.create(
            user=user,
            address='г. Липецк, ул. Неделена, д. 3',
            full_name=f'{user.first_name} {user.last_name}',
            phone='88005553535',
            mail=f'{self.user.email}'
        )
        self.to_change = {
            "full_name": 'Максим Безбородов',
            "phone": '88005555535',
            "mail": 'new_test@gmail.su'
        }

    def test_create_model(self):
        """Test for creating module."""
        response = self.client.post(
            '/rest/Client/',
            data=json.dumps(self.request_data),
            content_type='application/json'
        )
        serializer = ClientSerializer(data=self.request_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_model(self):
        """Test for getting module."""
        url_to_get = f'/rest/Client/{self.model.id}/'
        response = self.client.get(url_to_get)
        serializer = ClientSerializer(data=self.request_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_model(self):
        """Test for updating module."""
        url_to_update = f'/rest/Client/{self.model.id}/'
        response = self.client.patch(
            url_to_update,
            data=json.dumps(
                self.to_change,
            ),
            content_type='application/json'
        )
        serializer = ClientSerializer(data=self.to_change, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_model(self):
        """Test for deliting module."""
        url_to_delete = f'/rest/Client/{self.model.id}/'
        response = self.client.delete(url_to_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Client.objects.filter(id=self.model.id).exists()
        )


class ProductTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            is_superuser=True,
            id=1,
            username='test',
            first_name='test',
            last_name='test',
            email='test@mail.ru',
            password='test'
        )
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        client = Client.objects.create(
            user=self.user,
            address='г. Липецк, ул. Неделена, д. 3',
            full_name=f'{self.user.first_name} {self.user.last_name}',
            phone='88005553535',
            mail=f'{self.user.email}'
        )
        p_cat = Category_products.objects.create(
            cp_name='Запчасти'
        )
        self.request_data = {
            'client': f'{client.id}',
            'p_cat': f'{p_cat.id}',
            'name': 'Карбюратор',
            "available": "True",
            'description': 'Всем карбюраторам карбюратор',
            'quantity': 2,
            'price': 300
        }

        self.model = Products.objects.create(
            client=client,
            p_cat=p_cat,
            name='Карбюратор',
            available=True,
            description='Всем карбюраторам карбюратор',
            quantity=2,
            price=300
        )
        self.to_change = {
            "name": 'Карбулятор',
            "description": 'Лучший каргхбуляхтор',
            "price": '350.00'
        }

    def test_create_model(self):
        """Test for creating module."""
        response = self.client.post(
            '/rest/Products/',
            data=json.dumps(self.request_data),
            content_type='application/json'
        )
        serializer = ProductsSerializer(data=self.request_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_model(self):
        """Test for getting module."""
        url_to_get = f'/rest/Products/{self.model.id}/'
        response = self.client.get(url_to_get)
        serializer = ProductsSerializer(data=self.request_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_model(self):
        """Test for updating module."""
        url_to_update = f'/rest/Products/{self.model.id}/'
        response = self.client.patch(
            url_to_update,
            data=json.dumps(
                self.to_change,
            ),
            content_type='application/json'
        )
        serializer = ProductsSerializer(data=self.to_change, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_model(self):
        """Test for deliting module."""
        url_to_delete = f'/rest/Products/{self.model.id}/'
        response = self.client.delete(url_to_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Products.objects.filter(id=self.model.id).exists()
        )


class OrderTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            is_superuser=True,
            id=1,
            username='test',
            first_name='test',
            last_name='test',
            email='test@mail.ru',
            password='test'
        )
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        client = Client.objects.create(
            user=self.user,
            address='г. Липецк, ул. Неделена, д. 3',
            full_name=f'{self.user.first_name} {self.user.last_name}',
            phone='88005553535',
            mail=f'{self.user.email}'
        )
        p_cat = Category_products.objects.create(
            cp_name='Запчасти'
        )
        product = Products.objects.create(
            client=client,
            p_cat=p_cat,
            name='Карбюратор',
            available=True,
            description='Всем карбюраторам карбюратор',
            quantity=2,
            price=300
        )
        self.request_data = {
            'client': f'{client.id}',
            'product': f'{product.id}',
            'status': 'Waiting',
            'price': f'{product.price * product.quantity}',
            'quantity': f'{product.quantity}',
            'delivery_status': 'Waiting'
        }

        self.model = Order.objects.create(
            client=client,
            product=product,
            status='Waiting',
            price=product.price * product.quantity,
            quantity=product.quantity,
            delivery_status='Waiting'
        )
        self.to_change = {
            'status': 'Confirmed',
            'delivery_status': 'Completed'
        }

    def test_create_model(self):
        """Test for creating module."""
        response = self.client.post(
            '/rest/Order/',
            data=json.dumps(self.request_data),
            content_type='application/json'
        )
        serializer = OrderSerializer(data=self.request_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_model(self):
        """Test for getting module."""
        url_to_get = f'/rest/Order/{self.model.id}/'
        response = self.client.get(url_to_get)
        serializer = OrderSerializer(data=self.request_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_model(self):
        """Test for updating module."""
        url_to_update = f'/rest/Order/{self.model.id}/'
        response = self.client.patch(
            url_to_update,
            data=json.dumps(
                self.to_change,
            ),
            content_type='application/json'
        )
        serializer = OrderSerializer(data=self.to_change, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_model(self):
        """Test for deliting module."""
        url_to_delete = f'/rest/Order/{self.model.id}/'
        response = self.client.delete(url_to_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Order.objects.filter(id=self.model.id).exists()
        )
