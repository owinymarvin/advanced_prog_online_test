import matplotlib.pyplot as plt
from sales.models import DiscountedProduct
import django
import os

# Initialize Django settings if running as a standalone script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")
django.setup()


def visualize_discount(product_id):
    try:
        # Fetch the discounted product by ID
        product = DiscountedProduct.objects.get(id=product_id)
        original_price = product.price
        discounted_price = product.apply_discount()

        # Prepare data for visualization
        prices = [original_price, discounted_price]
        labels = ["Original Price", "Discounted Price"]

        # Create the bar chart
        plt.figure(figsize=(8, 5))
        plt.bar(labels, prices, color=['blue', 'green'])
        plt.title(f"Price Comparison for {product.name}")
        plt.xlabel("Price Type")
        plt.ylabel("Amount ($)")
        plt.show()

    except DiscountedProduct.DoesNotExist:
        print(f"Product with ID {product_id} does not exist.")


# Example usage
# Replace `1` with the ID of the product you want to visualize
visualize_discount(1)
