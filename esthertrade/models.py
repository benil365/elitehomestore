from django.db import models
from decimal import Decimal
# model to represent the different types of commodities
class Commodity(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='commodities/')
    category = models.CharField(max_length=25)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f"{self.name}{self.price}"
# model to represent customer orders
class Order(models.Model):
    email = models.EmailField(default="example@example.com")
    phone_no = models.CharField(max_length=10)
    items = models.ManyToManyField(Commodity, through='OrderItem')
    ordered_at = models.DateTimeField(auto_now_add=True)
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2, default=450.00)
    delivery_place = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the order to the database first

        # Calculate the total_amount
        total_amount = self.delivery_fee
        for item in self.items.all():
            total_amount += item.price

        self.total_amount = total_amount
        super().save(update_fields=['total_amount'])

    def __str__(self):
        return f"Order #{self.total_amount} by {self.phone_no}"

# model to represent items within an order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # You can add more fields like discounts, taxes, etc.

    def __str__(self):
        return f"{self.quantity}x {self.commodity.id} in Order #{self.order.id}"
