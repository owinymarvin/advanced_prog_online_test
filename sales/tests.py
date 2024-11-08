from django.test import TestCase
from .models import Product, DiscountedProduct


class ProductTestCase(TestCase):
    def setUp(self):
        # Create a regular product
        self.laptop = Product.objects.create(
            name="Laptop",
            price=1000.00,
            stock=10
        )

        # Create a discounted product
        self.smartphone = DiscountedProduct.objects.create(
            name="Smartphone",
            price=800.00,
            stock=15,
            discount_percentage=10
        )

    def test_product_price(self):
        """Ensure that the product price remains consistent"""
        self.assertEqual(self.laptop.get_price(), 1000.00)

    def test_discounted_product_price(self):
        """Check that the discount calculation remains accurate"""
        expected_discounted_price = self.smartphone.price * \
            (1 - self.smartphone.discount_percentage / 100)
        self.assertEqual(self.smartphone.apply_discount(),
                         expected_discounted_price)

    def test_update_product_price(self):
        """Test that updating the price does not affect unrelated fields"""
        self.laptop.price = 1200.00
        self.laptop.save()
        self.assertEqual(self.laptop.get_price(), 1200.00)
        self.assertEqual(self.laptop.stock, 10)  # Ensure stock is unaffected

    def test_discount_percentage_change(self):
        """Ensure that changing the discount does not disrupt other calculations"""
        self.smartphone.discount_percentage = 20
        self.smartphone.save()
        updated_discounted_price = self.smartphone.price * \
            (1 - self.smartphone.discount_percentage / 100)
        self.assertEqual(self.smartphone.apply_discount(),
                         updated_discounted_price)
