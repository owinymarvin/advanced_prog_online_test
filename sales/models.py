from django.contrib.auth.models import AbstractUser, User
import os
from django.conf import settings
from django.utils import timezone
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def get_price(self):
        """Retrieve the price of the product, demonstrating encapsulation."""
        return self.price

    def __str__(self):
        return self.name


class DiscountedProduct(Product):
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def apply_discount(self):
        """Apply discount to the product price."""
        discounted_price = self.price * (1 - self.discount_percentage / 100)
        return discounted_price


class CalculatedProduct(Product):
    additional_fee = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)

    def calculate_final_price(self):
        """Add an additional fee to the product price."""
        return self.price + self.additional_fee



