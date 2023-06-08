import re
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from . import config


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


def validation_created_date(dt_to_set):
    dt_new = datetime.strptime(f"{dt_to_set}", "%Y-%m-%d %H:%M:%S%z").replace(tzinfo=None)
    dt_cur = datetime.strptime(f"{datetime.now()}", "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=None)
    if dt_new > dt_cur:
        raise ValidationError('Дата не может быть в будущем.')


class CreatedMixin(models.Model):
    created = models.DateTimeField(
        _('created'),
        default=datetime.now,
        blank=False,
        null=False,
        validators=[validation_created_date]
    )

    class Meta:
        abstract = True


class ModifiedMixin(models.Model):
    modified = models.DateTimeField(
        _('modified'),
        default=datetime.now,
        blank=True,
        null=False,
        validators=[validation_created_date]
    )

    class Meta:
        abstract = True


def validate_phone_number(phone_number: str):
    pattern = r'^(\+\d{1,3}\s?)?(\(\d{1,4}\))?\s?\d{1,4}[\s.-]?\d{1,9}[\s.-]?\d{1,9}$'
    match = re.match(pattern, phone_number)
    if not match:
        raise ValidationError(  # from django.core.exceptions
            'We need 10 digits number',
            params={'phone_number': phone_number},
        )


def validate_mail(mail: str):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    match = re.match(pattern, mail)
    if not match:
        raise ValidationError(  # from django.core.exceptions
            'Please write valid mail',
            params={'mail': mail},
        )


class Client(CreatedMixin, ModifiedMixin, UUIDMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Ссылка на пользователя!
    address = models.TextField(_('address'), blank=True, null=True, max_length=config.CHARS_DEFAULT)
    full_name = models.CharField(_('full_name'), blank=False, null=False, max_length=config.CHARS_DEFAULT)
    phone = models.CharField(
        _('phone'),
        blank=True,
        null=True,
        max_length=config.CHARS_DEFAULT,
        validators=[validate_phone_number]
    )
    mail = models.CharField(
        _('mail'),
        blank=True,
        null=True,
        max_length=config.CHARS_DEFAULT,
        validators=[validate_mail]
    )
    image_client = models.ImageField(
        _('image_client'),
        blank=True,
        null=True,
        upload_to='clients/',
        default='clients/default_avatar.png'
    )

    class Meta:
        db_table = 'clients'

    def __str__(self):
        return f'{self.full_name} | {self.mail}'


class ClientMixin(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        abstract = True


class Category_products(UUIDMixin):
    cp_name = models.CharField(_('cp_name'), blank=False, null=False, max_length=config.CHARS_DEFAULT)

    class Meta:
        db_table = 'category_products'

    def __str__(self):
        return f'{self.cp_name}'


def validate_price(price: int):
    if int(price) <= 0:
        raise ValidationError(  # from django.core.exceptions
            f'Price {price} is less or equal zero',
            params={'price': price},
        )


class Products(CreatedMixin, UUIDMixin, ClientMixin):
    p_cat = models.ForeignKey(Category_products, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(_('name'), blank=False, null=False, max_length=config.CHARS_DEFAULT)
    available = models.BooleanField(_('available'), blank=False, null=False)
    description = models.TextField(_('description'), blank=False, null=False)
    quantity = models.IntegerField(_('quantity'), null=False, blank=False, default=1,
                                   validators=[MinValueValidator(0), MaxValueValidator(99)])
    price = models.DecimalField(
        verbose_name=_('price'),
        max_digits=config.DECIMAL_MAX_DIGITS,
        decimal_places=config.DECIMAL_PLACES,
        default=0,
        validators=[validate_price]
    )
    cur_img = models.ImageField(
        _('cur_img'),
        blank=True,
        null=True,
        upload_to='products/',
        default='products/default_product.png'
    )

    class Meta:
        db_table = 'products'

    def __str__(self):
        return f'{self.name}'


class Images(UUIDMixin):
    img = models.ImageField(upload_to='imgs/')

    class Meta:
        db_table = 'imgs'

    def __str__(self):
        return f'{self.img.name}'


class Product_Mixin(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        abstract = True


class Images_products(Product_Mixin):
    id_img = models.ForeignKey(Images, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        db_table = 'images_products'


pay_statuses = (
    ('Cancelled', 'Cancelled'),
    ('Confirmed', 'Confirmed'),
    ('Waiting', 'Waiting')
)

delivery_statuses = (
    ('Delivered', 'Delivered'),
    ('On the way', 'On the way'),
    ('Waiting', 'Waiting'),
    ('Completed', 'Completed'),
)


class Order(UUIDMixin, CreatedMixin, ModifiedMixin, ClientMixin, Product_Mixin):
    status = models.CharField(
        default='Waiting',
        blank=False,
        null=False,
        max_length=config.CHARS_DEFAULT,
        choices=pay_statuses
    )
    price = models.DecimalField(
        verbose_name=_('price'),
        max_digits=config.DECIMAL_MAX_DIGITS,
        decimal_places=config.DECIMAL_PLACES,
        default=0,
        validators=[validate_price]
    )
    quantity = models.IntegerField(_('quantity'), blank=False, null=False)
    delivery_status = models.CharField(
        default='Waiting',
        blank=False,
        null=False,
        max_length=config.CHARS_DEFAULT,
        choices=delivery_statuses
    )

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f'{self.client.full_name} - {self.price}'
