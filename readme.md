#  Classic Fitness (Gym Management) System API

A complete **Gym Management System REST API** built using **Django Rest Framework (DRF)**.  
This project is designed for real-world gym operations including memberships, class booking,
attendance tracking, services, feedback, and admin analytics.

---

##  Key Features

###  User Roles
- **Admin** – Full system control
- **Staff** – Attendance & class management
- **Member** – Book classes, give feedback, view subscriptions

---

###  Modules Overview

-  Authentication & Role-based Authorization
-  Membership Plans & Subscriptions
-  Fitness Classes & Booking System
-  Attendance Management
-  Class Feedback (Nested API)
-  Gym Services & Gallery

---

##  Tech Stack

| Layer        | Technology |
|--------------|------------|
| Backend      | Django, Django Rest Framework |
| Database     | PostgreSQL / SQLite |
| Auth         | JWT / Session Authentication |
| API Docs     | Swagger (drf-yasg) |
| Routing      | DRF Routers & Nested Routers |

---

##  Project Structure

```text
gym_management/
│
├── accounts/          # Custom User, roles & permissions
├── classes/           # Fitness classes & bookings
├── memberships/       # Plans & subscriptions
├── attendance/        # Attendance tracking
├── services/          # Gym services, gallery, feedback
├── reports/           # Admin analytics & dashboard APIs
├── api/               # Central API routing
│
├── manage.py
├── requirements.txt
├── README.md
└── LICENSE
```

AUTHENTICATION AND PERMISSIONS

Authentication:
- JWT based authentication
- Email and password login
- Implemented using Djoser

Authentication Endpoints:
```bash
POST   /api/v1/auth/jwt/create/      Login
POST   /api/v1/auth/jwt/refresh/     Refresh token
POST   /api/v1/auth/users/           Register
GET    /api/v1/auth/users/me/        Current user
```

Authorization:
Roles are enforced using custom permission classes:
- IsAdmin
- IsStaff
- IsAdminOrReadOnly

Example:
permission_classes = [IsAuthenticated, IsAdmin]

--------------------------------------------------

API ENDPOINTS

Fitness Classes:
```bash
GET     /api/v1/classes/
POST    /api/v1/classes/              Admin only
GET     /api/v1/classes/{id}/
POST    /api/v1/classes/{id}/book/    Member only
GET     /api/v1/classes/my_booking/
```

Membership Plans:
```bash
GET     /api/v1/membership-plans/
POST    /api/v1/membership-plans/     Admin only
```

Subscription:
```bash
POST    /api/v1/membership-plans/{id}/subscribe/
GET     /api/v1/subscription/my/
```

Rules:
- One active subscription per user
- Start and end dates auto-calculated

Attendance:
```bash
GET     /api/v1/attendance/   Admin Only
POST    /api/v1/attendance/   Admin Only
```

Rules:
- Admin and Staff only
- Only active members allowed

Feedback (Nested API):
```bash
GET     /api/v1/classes/{class_id}/feedback/
POST    /api/v1/classes/{class_id}/feedback/
```

Rules:
- One feedback per user per class
- Members can see only their own feedback


Gym Services:
```bash
GET     /api/v1/services/
POST    /api/v1/services/             Admin only
```

Gallery:
```bash
GET     /api/v1/gallery/
POST    /api/v1/gallery/              Admin only
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mdarafathossensojib/ClassicFitness

   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```    |

API Documentation:
Swagger documentation is available at:
```
http://127.0.0.1:8000/swagger/
```

ReDoc documentation is available at:
```
http://127.0.0.1:8000/redoc/
```

Environment Variables:
Create a `.env` file in the root directory and add the following:
```ini
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
ALLOWED_HOSTS=*
EMAIL_HOST=your_email_host
```

License:
This project is licensed under the MIT License.

---
Author:
- MD Arafat Hossen
- Backend Developer (Django & DRF)
- GitHub: https://github.com/mdarafathossensojib/