from .forms import CustomSignupForm
from .models import DiscountedProduct
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import matplotlib.pyplot as plt
from io import BytesIO
from django.shortcuts import render
from .models import Product, DiscountedProduct, CalculatedProduct

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomLoginForm


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            # Use Django's ORM to safely authenticate
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('product_list')
    else:
        form = CustomLoginForm()
    return render(request, 'sales/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to login page after successful signup
            return redirect('login')
    else:
        form = CustomSignupForm()
    return render(request, 'sales/signup.html', {'form': form})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'sales/product_list.html', {'products': products})


def discounted_product_list(request):
    discounted_products = DiscountedProduct.objects.all()
    return render(request, 'sales/discounted_product_list.html', {'discounted_products': discounted_products})


def calculated_product_list(request):
    calculated_products = CalculatedProduct.objects.all()
    return render(request, 'sales/calculated_product_list.html', {'calculated_products': calculated_products})


def discount_plot_view(request, product_id):
    # Fetch the product or return a 404 error if it doesn't exist
    product = get_object_or_404(DiscountedProduct, id=product_id)
    original_price = product.price
    discounted_price = product.apply_discount()

    # Prepare data for the bar chart
    prices = [original_price, discounted_price]
    labels = ["Original Price", "Discounted Price"]

    # Create the bar chart using Matplotlib
    fig, ax = plt.subplots()
    ax.bar(labels, prices, color=['blue', 'green'])
    ax.set_title(f"Price Comparison for {product.name}")
    ax.set_xlabel("Price Type")
    ax.set_ylabel("Amount ($)")

    # Save the plot to a BytesIO buffer in PNG format
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)

    # Return the plot as an HTTP response with image content type
    return HttpResponse(buffer, content_type='image/png')
