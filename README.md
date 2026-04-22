
**MyCarRental**

**MyCarRental is a Django-based web application that allows users to browse available cars, make bookings, and manage rental services through a simple and structured system.**



**Overview**

**This project provides a basic online car rental platform where users can view cars, check availability, and place rental requests. It demonstrates core Django concepts including database management, user interaction, and dynamic web pages.**



**Features**

* Browse available cars
* View car details
* Book rental cars
* Manage rental requests
* Simple and user-friendly interface



**Tech Stack**

* Python
* Django
* HTML
* CSS
* SQLite (default database)



**Project Structure**

* car_rental/ → Main Django project settings
* rental/ → Core application logic
* templates/ → HTML templates
* static/ → CSS and assets
* manage.py → Django project entry point



**Installation**

**1. Clone the repository**

```bash id="r1"
git clone https://github.com/Sarmala123/MyCarRental.git
cd MyCarRental
```

**2. Create virtual environment**

```bash id="r2"
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash id="r3"
pip install -r requirements.txt
```

**4. Run migrations**

```bash id="r4"
python manage.py migrate
```

**5. Create superuser**

```bash id="r5"
python manage.py createsuperuser
```

**6. Run server**

```bash id="r6"
python manage.py runserver
```



**Usage**

* Open homepage to browse available cars
* View car details and availability
* Book rental cars easily
* Admin manages cars and bookings via Django admin panel



**Notes**

* This project is for academic and learning purposes
* Uses SQLite as default database
* Django admin panel is available for management



**Author**

**Sarmala Tamang**

