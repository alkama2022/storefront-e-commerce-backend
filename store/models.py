from django.db import models


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=5, decimal_places=2)


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
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.PositiveIntegerField()
    last_update = models.DateTimeField(auto_now=True)

    collection = models.ForeignKey(
        Collection,
        on_delete=models.PROTECT,
        related_name='products'
    )

    promotions = models.ManyToManyField(
        Promotion,
        blank=True
    )


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_SILVER = 'S'

    MEMBERSHIP_CHOICES = (
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_GOLD, 'Gold'),
        (MEMBERSHIP_SILVER, 'Silver'),
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

    membership = models.CharField(
        max_length=1,
        choices=MEMBERSHIP_CHOICES,
        default=MEMBERSHIP_BRONZE
    )


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = (
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    )

    placed_at = models.DateTimeField(auto_now_add=True)

    payment_status = models.CharField(
        max_length=1,
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_STATUS_PENDING
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT
    )


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveSmallIntegerField()

    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='addresses'
    )