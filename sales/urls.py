from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='products'),
    path('products/discounted/', views.discounted_product_list,
         name='discounted_product_list'),
    path('products/calculated/', views.calculated_product_list,
         name='calculated_product_list'),
    path('discount-plot/<int:product_id>/',
         views.discount_plot_view, name='discount_plot'),

    #     for login and signup
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    # edit username, email, password
    path('user-profile/edit/username_or_email/',
         views.editUserNameOrEmail, name='editUserNameOrEmail'),
    path('user-profile/edit/password/',
         views.editUserPassword, name='editUserPassword'),

    # password reset
    path('password/reset/form/', views.passwordResetForm, name='passwordResetForm'),
    path('password/reset/form/<str:uid>/<str:token>/',
         views.passwordResetConfirm, name='passwordResetConfirm'),

    # pages
    path('', views.welcome, name='welcome'),
]
