from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name="logout"),
    path('dashboard', views.dashboard, name='dashboard'),
    path('new_customer', views.new_customer, name='new_customer'),
    path('new_insurance', views.new_insurance, name='new_insurance'),
    path('customer/<int:customer_id>', views.customer_details, name='customer_details'),
    path('add_new_customer', views.add_new_customer, name='add_new_customer'),
    path('add_new_insurance', views.add_new_insurance, name='add_new_insurance'),
    path('customers', views.customers, name='customers'),
    path('insurances_view', views.insurances_view, name='insurances_view'),
    path('insurance_details/<int:insurance_code>', views.insurance_details, name='insurance_details'),
    path('insurers', views.insurers, name='insurers'),
    path('insurer_details/<int:insurer_id>', views.insurer_details, name="insurer_details"),
    path('update_customer/<int:customer_id>', views.update_customer, name="update_customer"),
    path('add_new_updated_customer/<int:customer_id>', views.add_new_updated_customer, name="add_new_updated_customer"),
    path('update_insurance/<int:insurance_id>', views.update_insurance, name="update_insurance"),
    path('add_new_updated_insurance/<int:insurance_id>', views.add_new_updated_insurance, name="add_new_updated_insurance"),
    path('delete_insurance/<int:insurance_id>', views.delete_insurance, name="delete_insurance"),
    path('delete_customer/<int:customer_id>', views.delete_customer, name="delete_customer")
]