# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'categories'

    def __str__(self):
        return self.name


class OrderItems(models.Model):
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    amount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'order_items'


class Orders(models.Model):
    created_date = models.DateField()
    delivered_date = models.DateField()
    pick_point = models.ForeignKey('PickPoints', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    code = models.IntegerField(blank=True, null=True)
    status = models.ForeignKey('StatusOrder', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'orders'


class PickPoints(models.Model):
    zipcode = models.IntegerField()
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    builder = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pick_points'

    def __str__(self):
        return f'{self.zipcode}, {self.city}, {self.street}'


class Producers(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'producers'

    def __str__(self):
        return self.name


class Products(models.Model):
    articale = models.CharField(max_length=50, verbose_name='Артикул')
    name = models.CharField(max_length=255, verbose_name='Название')
    unit = models.ForeignKey('Units', models.DO_NOTHING, verbose_name='Единица измерения')
    price = models.IntegerField(verbose_name='Цена')
    provider = models.ForeignKey('Providers', models.DO_NOTHING, verbose_name='Поставщик')
    producer = models.ForeignKey(Producers, models.DO_NOTHING, verbose_name='Производитель')
    category = models.ForeignKey(Categories, models.DO_NOTHING, verbose_name='Категория')
    sale = models.IntegerField(blank=True, null=True, verbose_name='Скидка')
    amount = models.IntegerField(verbose_name='Количество')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(
        upload_to='images/',
        blank=True,
        null=True,
        verbose_name='Картинка',
        help_text='Загрузите изображение (JPG, PNG)'
    )

    class Meta:
        managed = False
        db_table = 'products'

    @property
    def final_price(self):
        if self.sale and self.sale > 0:
            return self.price * (1 - self.sale / 100)
        return self.price


class Providers(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'providers'

    def __str__(self):
        return self.name


class Roles(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'roles'

    def __str__(self):
        return self.name


class StatusOrder(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'status_order'

    def __str__(self):
        return self.name


class Units(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'units'

    def __str__(self):
        return self.name


class Users(models.Model):
    role = models.ForeignKey(Roles, models.DO_NOTHING)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'users'
