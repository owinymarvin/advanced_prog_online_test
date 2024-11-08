from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/discounted/', views.discounted_product_list,
         name='discounted_product_list'),
    path('products/calculated/', views.calculated_product_list,
         name='calculated_product_list'),
    path('discount-plot/<int:product_id>/',
         views.discount_plot_view, name='discount_plot'),
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
]
