# TaskMaster

A web-based task management application built with Django. Each registered user has a private workspace and can only access tasks they have created.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Authentication](#authentication)
- [Deployment on Render](#deployment-on-render)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

TaskMaster is a minimal but complete task management application developed as part of a Software Engineering project (Licence 2). It demonstrates the application of Object-Oriented Programming principles within the Django MVT architecture, using SQLite as the default database and a fully custom HTML/CSS interface.

---

## Features

- User registration and authentication
- Private task workspace per user (users cannot access each other's tasks)
- Create, read, update, and delete tasks
- Mark tasks as completed or revert them to in-progress
- Filter tasks by status or priority
- Dashboard with task statistics (total, in-progress, completed, high-priority)
- Responsive interface with flash messages for user feedback

---

## Tech Stack

- Python 3.10+
- Django 4.x
- SQLite (default) / PostgreSQL (production)
- HTML5 / CSS3 (no external CSS framework)
- Google Fonts (Playfair Display, Lato)

---

## Project Structure

```
taskmanager/
|
|-- taskmanager/
|   |-- settings.py
|   |-- urls.py
|   |-- wsgi.py
|   `-- asgi.py
|
|-- tasks/
|   |-- migrations/
|   |-- templates/
|   |   `-- tasks/
|   |       |-- base.html
|   |       |-- liste.html
|   |       |-- form.html
|   |       |-- connexion.html
|   |       |-- inscription.html
|   |       `-- confirmer_suppression.html
|   |-- __init__.py
|   |-- admin.py
|   |-- apps.py
|   |-- forms.py
|   |-- models.py
|   |-- urls.py
|   `-- views.py
|
|-- manage.py
|-- requirements.txt
`-- README.md
```

---

## Requirements

- Python 3.10 or higher
- pip
- virtualenv (recommended)

All Python dependencies are listed in `requirements.txt`.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/taskmaster.git
cd taskmaster
```

### 2. Create and activate a virtual environment

On Linux and macOS:
```bash
python -m venv venv
source venv/bin/activate
```

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Before running the application, review `taskmanager/settings.py`. The following values should be adjusted for your environment:

- `SECRET_KEY`: Change this to a long random string in production. Never commit the real secret key to version control.
- `DEBUG`: Set to `False` in production.
- `ALLOWED_HOSTS`: Add your domain or IP address when deploying.
- `DATABASES`: SQLite is configured by default. See the deployment section for PostgreSQL configuration.
- `TIME_ZONE`: Set to your local timezone. The default is `Africa/Abidjan`.

For production, it is strongly recommended to manage sensitive values using environment variables rather than hardcoding them in `settings.py`. See the [Environment Variables](#environment-variables) section below.

---

## Database Setup

Run the following commands after cloning and installing dependencies:

```bash
python manage.py makemigrations
python manage.py migrate
```

To create an administrator account for the Django admin panel at `/admin/`:

```bash
python manage.py createsuperuser
```

---

## Running the Application

Start the local development server:

```bash
python manage.py runserver
```

The application will be accessible at:

```
http://127.0.0.1:8000/
```

---

## Usage

### First-time users

1. Navigate to `http://127.0.0.1:8000/inscription/` to create an account.
2. Log in at `http://127.0.0.1:8000/connexion/`.
3. You will be redirected to your task dashboard.

### Managing tasks

From the dashboard, you can:

- Click "Nouvelle tache" to create a task. Each task requires a title and accepts an optional description, a priority level (Faible / Moyenne / Haute), and a status (En cours / Terminee).
- Click the edit button on any task row to modify it.
- Click "Terminer" to mark a task as completed. Click "Annuler" to revert it to in-progress.
- Click the delete button to permanently remove a task. A confirmation page is shown before deletion.
- Use the filter bar at the top of the dashboard to filter tasks by status or priority.

### Security note

Each view that accesses tasks is protected by the `@login_required` decorator. All queries are filtered by the currently authenticated user. Attempting to access another user's task by manipulating a URL will result in a 404 response.

---

## Authentication

The application uses Django's built-in authentication system. The following routes are available:

| Route | Description |
|-------|-------------|
| `/inscription/` | Create a new user account |
| `/connexion/` | Log in to an existing account |
| `/deconnexion/` | Log out of the current session |

Unauthenticated users who attempt to access any protected route are automatically redirected to `/connexion/`.

The following settings control authentication redirects in `settings.py`:

```python
LOGIN_URL = '/connexion/'
LOGIN_REDIRECT_URL = '/'
```

---

## Deployment on Render

### 1. Add required packages

Add the following to your `requirements.txt`:

```
gunicorn
whitenoise
dj-database-url
psycopg2-binary
python-decouple
```

### 2. Update settings.py for production

```python
import dj_database_url
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Static files (served by WhiteNoise)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... rest of middleware
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database (PostgreSQL on Render, SQLite locally)
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
    )
}
```

### 3. Create a build script

Create a file named `build.sh` at the root of the project:

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

Make it executable:

```bash
chmod +x build.sh
```

### 4. Configure the Render service

In your Render dashboard, create a new Web Service and set the following:

| Field | Value |
|-------|-------|
| Build Command | `./build.sh` |
| Start Command | `gunicorn taskmanager.wsgi:application` |
| Environment | Python 3 |

Add a PostgreSQL database from the Render dashboard and link it to your service. Render will provide a `DATABASE_URL` environment variable automatically.

---

## Environment Variables

The following environment variables should be defined in your deployment environment or in a `.env` file for local development. Never commit a `.env` file to version control.

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `your-very-long-random-string` |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `yourdomain.onrender.com` |
| `DATABASE_URL` | Full database connection string | `postgresql://user:pass@host/db` |

For local development, create a `.env` file at the project root:

```
SECRET_KEY=your-local-dev-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

Add `.env` to your `.gitignore` file:

```
.env
venv/
__pycache__/
*.pyc
db.sqlite3
staticfiles/
```

---

## Contributing

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature/your-feature-name`
3. Commit your changes with clear messages: `git commit -m "Add: description of change"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a pull request against the `main` branch.

Please ensure your code follows the existing style and that all views accessing user data include the appropriate filters and access controls.

---

## License

This project is distributed under the MIT License. See the `LICENSE` file for details.
