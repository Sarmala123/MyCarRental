from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # public
    path('', views.home, name='home'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
    path('search/', views.rental_search, name='rental_search'),
    path('contact-us/', views.contact_us, name='contact_us'),

    # auth
    path('signup/', views.signup, name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='rental/login.html'),name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # customer bookings
    path('dashboard/', views.my_bookings, name='customer_dashboard'),
    
    path('profile/', views.profile, name='profile'),


    
    # staff
    path('manage-bookings/', views.manage_bookings, name='manage_bookings'),
    path('manage-bookings/<int:booking_id>/<str:new_status>/', 
         views.update_booking_status, name='update_booking_status'),
    
    path('book/<int:car_id>/', views.create_booking, name='create_booking'),
    path("my-bookings/", views.view_bookings, name="my_bookings"),

  
    # mock‐payment (or “Pay now”)
    path("pay/<int:booking_id>/",  views.pay_booking,    name="pay_booking"),
    path("receipt/<int:pk>/",      views.payment_receipt, name="payment_receipt"),

    # stripe checkout flow
    path("stripe/checkout/<int:booking_id>/", views.stripe_checkout, name="stripe_checkout"),
    path("stripe/success/",               views.payment_success,  name="payment_success"),
    path("stripe/cancel/",                views.payment_cancel,   name="payment_cancel"),
    path("stripe/webhook/",              views.stripe_webhook,   name="stripe_webhook"),


]