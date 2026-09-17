
from django.db import models


class Promotion(models.Model):
    description = models.CharField(max_length=255)

    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    def __str__(self):
        return self.description


class Collection(models.Model):
    title = models.CharField(max_length=255)

    featured_product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    inventory = models.PositiveIntegerField()

    last_update = models.DateTimeField(
        auto_now=True
    )

    collection = models.ForeignKey(
        Collection,
        on_delete=models.PROTECT,
        related_name='products'
    )

    promotions = models.ManyToManyField(
        Promotion,
        blank=True,
        related_name='products'
    )

    def __str__(self):
        return self.title


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = (
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    )

    first_name = models.CharField(
        max_length=255
    )

    last_name = models.CharField(
        max_length=255
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=20
    )

    birth_date = models.DateField(
        null=True,
        blank=True
    )

    membership = models.CharField(
        max_length=1,
        choices=MEMBERSHIP_CHOICES,
        default=MEMBERSHIP_BRONZE
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = (
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    )

    placed_at = models.DateTimeField(
        auto_now=True
    )

    payment_status = models.CharField(
        max_length=1,
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_STATUS_PENDING
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='orders'
    )

    def __str__(self):
        return f'Order #{self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items'
    )

    quantity = models.PositiveSmallIntegerField()

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f'{self.quantity} x {self.product.title}'


class Address(models.Model):
    street = models.CharField(
        max_length=255
    )

    city = models.CharField(
        max_length=255
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='addresses'
    )

    def __str__(self):
        return f'{self.street}, {self.city}'


class Review(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'{self.customer} - {self.product}'

