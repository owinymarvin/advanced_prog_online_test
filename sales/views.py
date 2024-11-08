from .forms import SimpleUserCreationForm
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .forms import registrationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import DiscountedProduct
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import matplotlib.pyplot as plt
from io import BytesIO
from django.shortcuts import render
from .models import Product, DiscountedProduct, CalculatedProduct
from django.shortcuts import render, redirect


@login_required(login_url='login')
def product_list(request):
    products = Product.objects.all()
    context = {'page': "products", 'products': products}
    return render(request, 'sales/product_list.html', context)


@login_required(login_url='login')
def discounted_product_list(request):
    discounted_products = DiscountedProduct.objects.all()
    return render(request, 'sales/discounted_product_list.html', {'discounted_products': discounted_products, 'page': "discounted_product_list"})


@login_required(login_url='login')
def calculated_product_list(request):
    calculated_products = CalculatedProduct.objects.all()
    return render(request, 'sales/calculated_product_list.html', {'calculated_products': calculated_products, "page": "calculated_product_list"})


@login_required(login_url='login')
def discount_plot_view(request, product_id):
    product = get_object_or_404(DiscountedProduct, id=product_id)
    original_price = product.price
    discounted_price = product.apply_discount()
    prices = [original_price, discounted_price]
    labels = ["Original Price", "Discounted Price"]
    fig, ax = plt.subplots()
    ax.bar(labels, prices, color=['blue', 'green'])
    ax.set_title(f"Price Comparison for {product.name}")
    ax.set_xlabel("Price Type")
    ax.set_ylabel("Amount ($)")
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png')


def registerUser(request):
    page = 'register'

    if request.user.is_authenticated:
        return redirect('products')

    registration = registrationForm()

    if request.method == 'POST':
        # data is filled into the form
        registrationData = registrationForm(request.POST)

        if registrationData.is_valid():
            new_user = registrationData.save(commit=False)
            new_user.username = new_user.username.lower()

            # save the user
            new_user.save()
            login(request, new_user)

            return redirect('products')

        else:
            messages.error(
                request, 'ERROR:  The user form was not valid. Failed to create new user')

    else:
        # messages.error(request,'ERROR:  Submit form using mmethod \"POST\"')
        pass

    context = {'page': page, 'registrationForm': registration}
    return render(request, 'sales/userRegistration.html', context)


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('products')
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email'].lower()
        password = request.POST['password1']
        try:
            user = User.objects.get(
                Q(username=username_or_email) | Q(email=username_or_email))
            db_user = authenticate(
                request, username=user.username, password=password)
            if db_user is not None:
                login(request, db_user)
                subject = 'Todo App: Someone logged into your account'
                message = f'Hi {request.user.username}, \n You have successfully logged into your account.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [request.user.email]
                send_mail(subject, message, from_email,
                          recipient_list, fail_silently=True)
                return redirect('products')
            else:
                messages.error(
                    request, "ERROR: invalid username or password, please check the login details and try again.")
        except User.DoesNotExist:
            messages.error(
                request, "ERROR: invalid login credentials, please try agin.")
    context = {'page': page}
    return render(request, 'sales/userLogin.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def editUserNameOrEmail(request):
    page = 'editUserNameOrEmail'
    userProfile = request.user
    if request.method == 'POST':
        change_username = request.POST['change_username']
        change_email = request.POST['change_email']
        user_password = request.POST['password']
        correctUserPassword = authenticate(
            request, username=userProfile.username, password=user_password)
        if correctUserPassword:
            if change_username:
                username_already_exists = User.objects.filter(
                    username=change_username)
                if not username_already_exists:
                    old_username = request.user.username
                    userProfile.username = change_username
                    messages.success(
                        request, f'Username changed from "{old_username}" to "{change_username}"')
                else:
                    messages.error(
                        request, f'ERROR: The username "{change_username}" Already exists. Try using another')
            if change_email:
                email_already_exists = User.objects.filter(email=change_email)
                if not email_already_exists:
                    old_email = request.user.email
                    userProfile.email = change_email
                    messages.success(
                        request, f'Email changed from "{old_email}" to "{change_email}"')
                else:
                    messages.error(
                        request, f'ERROR: The email "{change_email}" Already exists. Try using another')
            userProfile.save()
            return redirect('editUserNameOrEmail')
        else:
            messages.error(
                request, 'Invalid password. Failed to update profile.')
    context = {'page': page, 'userProfile': userProfile}
    return render(request, 'sales/editUserNameOrEmail.html', context)


@login_required(login_url='login')
def editUserPassword(request):
    page = 'editUserPassword'
    userProfile = request.user
    if request.method == 'POST':
        old_password = request.POST['old_password']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user_with_password = authenticate(
            request, username=userProfile.username, password=old_password)
        if user_with_password:
            if password1 == password2:
                user_with_password.set_password(password1)
                user_with_password.save()
                messages.success(request, 'Password updated successfully.')
                login(request, user_with_password)
                return redirect('editUserNameOrEmail')
            else:
                messages.error(request, 'New passwords do not match.')
        else:
            messages.error(
                request, 'Invalid users password. Failed to update password.')
    context = {'page': page, 'userProfile': userProfile}
    return render(request, 'sales/editUserPassword.html', context)


def passwordResetForm(request):
    page = 'passwordResetForm'
    if request.user.is_authenticated:
        return redirect('products')
    if request.method == 'POST':
        reset_email = request.POST['reset_email']
        user_with_email_exists = User.objects.filter(email=reset_email)
        if user_with_email_exists:
            user = user_with_email_exists.first()
            uid = str(user.id)
            token = default_token_generator.make_token(user)
            password_reset_link = request.build_absolute_uri(f'{uid}/{token}/')
            subject = 'Todo App: Password Reset Requested'
            message = f'If you requested to change your password click on the link below. \n\n { password_reset_link } '
            try:
                send_mail(subject, message,
                          settings.EMAIL_HOST_USER, [user.email])
                messages.success(
                    request, f'A PASSWORD RESET EMAIL HAS BEEN SENT TO "{user.email}" ')
            except:
                messages.error(
                    request, f'Failed to send Email. Check your Internet Connection')
            return redirect('login')
        else:
            messages.error(
                request, "ERROR: No user account associated with the provided email.")
    context = {'page': page}
    return render(request, 'sales/passwordResetForm.html', context)


def passwordResetConfirm(request, uid, token):
    page = 'passwordResetConfirm'
    if request.user.is_authenticated:
        return redirect('products')
    try:
        userProfile = User.objects.get(id=uid)
    except User.DoesNotExist:
        userProfile = None
    if userProfile is not None and default_token_generator.check_token(userProfile, token):
        email_reset_link_success = True
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                userProfile.set_password(password1)
                userProfile.save()
                messages.success(request, 'Password updated successfully.')
                login(request, userProfile)
                return redirect('products')
            else:
                messages.error(request, 'ERROR: New passwords do not match.')
    else:
        email_reset_link_success = False
        messages.error(
            request, "The password reset link is invalid or has expired.")
    context = {'page': page,
               'email_reset_link_success': email_reset_link_success}
    return render(request, 'sales/editUserPassword.html', context)


def welcome(request):
    page = 'welcome'
    context = {'page': page}
    return render(request, 'sales/welcome.html', context)
