from django.test import TestCase
from django.urls import reverse
from .models import Car, Booking, Profile
from django.contrib.auth import get_user_model

User = get_user_model()

class CarModelTests(TestCase):
    def setUp(self):
        self.car = Car.objects.create(
            name="Test Car",
            price_per_day=100,
            available=True
        )

    def test_car_creation(self):
        self.assertEqual(self.car.name, "Test Car")
        self.assertEqual(self.car.price_per_day, 100)
        self.assertTrue(self.car.available)

class BookingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.car = Car.objects.create(name="Test Car", price_per_day=100, available=True)
        self.booking = Booking.objects.create(
            customer=self.user,
            car=self.car,
            start_date="2023-10-01",
            end_date="2023-10-05",
            status=Booking.CONFIRMED
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.customer, self.user)
        self.assertEqual(self.booking.car, self.car)
        self.assertEqual(self.booking.start_date, "2023-10-01")
        self.assertEqual(self.booking.end_date, "2023-10-05")
        self.assertEqual(self.booking.status, Booking.CONFIRMED)

class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)

class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_car_list_view(self):
        response = self.client.get(reverse('car_list'))
        self.assertEqual(response.status_code, 200)

    def test_customer_dashboard_view(self):
        response = self.client.get(reverse('customer_dashboard'))
        self.assertEqual(response.status_code, 200)