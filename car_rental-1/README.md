# Car Rental Project

This is a Django-based car rental application that allows users to browse available cars, create bookings, manage their profiles, and handle payments. The application also includes an admin interface for managing bookings and users.

## Features

- User authentication (signup, login, profile management)
- Car listing with availability status
- Booking creation and management
- Payment processing (mock and Stripe integration)
- Admin interface for managing bookings and users
- Responsive design with HTML templates

## Project Structure

```
car_rental/
├── rental/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── car_rental/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd car_rental
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser for the admin interface:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000/`.

## Usage

- Visit the home page to browse available cars.
- Users can sign up, log in, and manage their bookings.
- Admins can manage bookings and users through the admin interface.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.