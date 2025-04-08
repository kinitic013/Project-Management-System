# 🗂️ Project Management System (PMS) API

A RESTful backend for a Project Management System built using **Django** and **Django REST Framework**. This system allows authenticated users to manage projects, tasks, and associated images with activity logging and JWT-based authentication.
- GITHUB LINK [https://github.com/kinitic013/Project-Management-System]
---

## 🚀 Features

- 🔐 **JWT Authentication** (login, signup)
- 📁 **Project Management** (create, update, soft delete)
- ✅ **Task Management** (create, update status, delete)
- 🖼️ **Image Upload** (attach images to projects)
- 📝 **Activity Logs** (track user actions)
- 📦 **CSV Export** for project data

---

## 🔧 Tech Stack

- **Backend**: Django, Django REST Framework
- **Authentication**: SimpleJWT
- **Database**: SQLite
- **Documentation**: drf-yasg (Swagger UI) 

---
## 📦 Folder Structure
```
pms_project/
├── pms_project/              # Django project config
│   └── settings.py           # Project settings
├── pms_app/                  # Core application
│   ├── views/                # Modular views by entity
│   │   ├── auth_views.py         # Authentication (JWT, signup)
│   │   ├── project_views.py      # Project CRUD
│   │   ├── task_views.py         # Task operations
│   │   ├── image_views.py        # Image uploads & fetch
│   │   ├── activity_views.py     # Activity logs
│   │   └── __init__.py           # Exposes views for import
│   ├── serializers.py        # DRF serializers
│   ├── models.py             # Data models
│   ├── constants.py          # Centralized constants (enums, actions)
│   ├── utils.py              # Shared utility functions
│   ├── urls.py               # URL routes
│   ├── admin.py              # Django admin registration
│   └── apps.py               # App configuration
├── media/                    # Uploaded media (images)
├── db.sqlite3                # SQLite DB (development)
├── manage.py                 # Django CLI utility
├── requirements.txt          # Python dependencies
└── DataXai.postman_collection.json  # Postman collection for API testing
```  
## 📦 Installation

```bash
git clone https://github.com/kinitic013/Project-Management-System.git
cd Project-Management-System 
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```  
- postman-testing collection is added in the repo and it's best and fast way to test apis , create an environment and upload this collection file and everything works fine and smooth.
- Swagger-UI can be accessed using this (http://127.0.0.1:8000/swagger/) endpoint

