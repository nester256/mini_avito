from datetime import timedelta
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect
from django.utils import timezone
from requests import Response
from rest_framework import viewsets, status as status_codes, permissions
from .models import *
from django.contrib.auth import decorators
from .serializers import *
import requests as rq
from .forms import ProductsForm


def custom_main(req):
    return render(
        req,
        config.HOMEPAGE,
    )


@decorators.login_required(login_url='login')
def profile(request):
    client = Client.objects.get(user=request.user)
    if not client:
        return Response("Such client does not exist", status=status_codes.HTTP_404_NOT_FOUND)
    return render(request, config.PROFILE_ACCOUNTS, {'client': client})

class Permission(permissions.BasePermission):
    def has_permission(self, request, _):
        if request.method in ['GET', 'HEAD', 'PATCH']:
            return bool(request.user and request.user.is_authenticated)
        elif request.method in ['POST', 'PUT', 'DELETE']:
            return bool(request.user and request.user.is_superuser)
        return False


def query_from_request(request, cls_serializer=None) -> dict:
    if cls_serializer:
        query = {}
        for attr in cls_serializer.Meta.fields:
            attr_value = request.GET.get(attr, '')
            if attr_value:
                query[attr] = attr_value
        return query
    return request.GET


def create_viewset(cls_model: models.Model, serializer, permission, order_field):
    class_name = f"{cls_model.__name__}ViewSet"
    doc = f"API endpoint that allows users to be viewed or edited for {cls_model.__name__}"
    CustomViewSet = type(class_name,
                         (viewsets.ModelViewSet,),
                         {
                             "__doc__": doc,
                             "serializer_class": serializer,
                             "queryset": cls_model.objects.all().order_by(order_field),
                             "permission classes": [permission],
                             "get_queryset": lambda self, *args, **kwargs: cls_model.objects.filter(
                                 **query_from_request(self.request, serializer)).order_by(order_field)
                         }
                         )

    return CustomViewSet


ClientViewSet = create_viewset(Client, ClientSerializer, Permission, 'id')
UserViewSet = create_viewset(User, UserSerializer, Permission, 'id')
ProductViewSet = create_viewset(Products, ProductsSerializer, Permission, 'id')
Category_productViewSet = create_viewset(Category_products, Category_productsSerializer, Permission, 'id')
OrderViewSet = create_viewset(Order, OrderSerializer, Permission, 'id')


@decorators.login_required(login_url='login')
def products_list(request):
    products = Products.objects.filter(available=True)
    paginator = Paginator(products, config.PAGINATE_THRESHOLD)
    page = request.GET.get('page')
    products_on_page = paginator.get_page(page)
    return render(request, config.PRODUCT_LIST, {'products': products_on_page})


@decorators.login_required(login_url='login')
def product_page(request, p_id):
    product = Products.objects.get(id=p_id)
    images_products = Images_products.objects.filter(product=product)
    images = [images_products.id_img for images_products in images_products]
    client = Client.objects.get(user=request.user)
    n_quantity = request.POST.get('quantity')
    if request.method == 'POST':    # by radugaboost©
        with transaction.atomic():
            order = Order.objects.create(
                price=product.price * int(n_quantity),
                client=client,
                product=product,
                quantity=n_quantity
            )
            order.save()
            product.quantity = product.quantity - int(n_quantity)
            product.save()

        response = rq.post(
            url=config.BOOST_URL.format(instance='payment'),
            headers=config.BOOST_HEADERS,
            json={
                'recipient': config.BOOST_ACCOUNT,
                'amount': f'{product.price * int(n_quantity)}',
                'pay_date': f'{timezone.now() + timedelta(minutes=30)}',
                'callback': {
                    'url': config.BOOST_CALLBACK_URL.format(order_id=order.id),
                    'headers': config.BOOST_CALLBACK_HEADERS,
                    'redirect': config.BOOST_CALLBACK_REDIRECT
                }
            }
        )
        payment_id = response.json().get('id')
        return redirect(config.BOOST_REDIRECT.format(payment_id=payment_id))

    return render(
        request,
        config.PRODUCT_PAGE,
        {
            'product': product,
            'imgs': images
        })


@decorators.login_required(login_url='login')
def my_products_page(request):
    client = Client.objects.get(user=request.user)
    products = Products.objects.filter(client=client)
    active_products = products.filter(available=True)
    false_products = products.filter(available=False)
    return render(request,
                  config.MY_PRODUCT_PAGE,
                  {
                      'active_products': active_products,
                      'false_products': false_products
                  })


@decorators.login_required(login_url='login')
def my_orders_page(request):
    # TODO сделать удаление заказа
    client = Client.objects.get(user=request.user)
    orders = Order.objects.filter(client=client)
    if request.method == 'POST':
        order_on_d = Order.objects.filter(id=request.POST.get('id')).first()
        if order_on_d:
            with transaction.atomic():
                order_on_d.delivery_status = 'Delivered'
                order_on_d.save()
        else:
            ...
    return render(request,
                  config.ORDERS_PAGE,
                  {
                      'orders': orders
                  })


@decorators.login_required(login_url='login')
def my_sales_page(request):
    # TODO сделать отмену продажи
    client = Client.objects.get(user=request.user)
    products = Products.objects.filter(client=client)
    orders = Order.objects.filter(product__in=products)
    if request.method == 'POST':
        order_on_d = Order.objects.get(id=request.POST.get('id'))
        with transaction.atomic():
            order_on_d.delivery_status = 'On the way'
            order_on_d.save()
    return render(request,
                  config.SALES_PAGE,
                  {
                      'orders': orders,
                      'bost_url': config.BOOST_URL
                  })


@decorators.login_required(login_url='login')
def get_money(request):
    if request.method == 'POST':
        order_on_d = Order.objects.filter(id=request.POST.get('id')).first()
        if order_on_d:
            response = rq.post(
                url=config.BOOST_URL.format(instance='transact'),
                headers=config.BOOST_HEADERS,
                json={
                    'sender': config.BOOST_ACCOUNT,
                    'amount': f'{order_on_d.price}',
                    'recipient': str(request.POST.get('rec_id')),
                }
            )
            if response.status_code == 201:
                with transaction.atomic():
                    order_on_d.delivery_status = 'Completed'
                    order_on_d.save()
                return redirect('profile')
            return redirect('error_page')  # TODO Сделать


@decorators.login_required(login_url='login')
def create_product(request):
    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.client_id = Client.objects.get(user=request.user.id).id
            product.save()
            return redirect('product', p_id=product.id)
    else:
        form = ProductsForm()
    return render(request, config.CREATE_PRODUCT_PAGE, {'form': form})
