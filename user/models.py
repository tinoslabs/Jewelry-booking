from django.conf import settings
from django.db import models

# Import Product from inventory app
from inventory.models import Product

# Import UserProfile from core app
from core.models import UserProfile


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) - {self.user.username}"

    @property
    def subtotal(self):
        return self.product.price * self.quantity
    
    
class Order(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash On Delivery'),
        ('bank', 'Direct Bank Transfer'),
        ('paypal', 'Razorpay/Paypal'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    company_name = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=100)
    street_address1 = models.CharField(max_length=255)
    street_address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    division = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, blank=True, null=True)
    order_note = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

# Create your models here.
