# JobTrack

A Django job application tracker for managing applications, following their status, and finding records by company, role, or status.

## Features

- User registration, login, and logout
- Private job application records for each account
- Create, view, edit, and delete application records
- Applied, Interview Scheduled, Selected, and Rejected statuses
- Search by company or role and filter by status
- SQLite for local development, with optional MySQL support

## Requirements

- Python 3.8 or newer
- pip
- MySQL Server and its development libraries only if using MySQL

## Quick start (Windows PowerShell)

From the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/> and create an account. The Django admin is at <http://127.0.0.1:8000/admin/>.

## Quick start (macOS/Linux)

From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## MySQL configuration

Install the optional MySQL driver:

```powershell
python -m pip install -r requirements-mysql.txt
```

Create a database, then configure the connection in the current terminal before running migrations:

```powershell
$env:DB_ENGINE = "django.db.backends.mysql"
$env:DB_NAME = "job_tracker"
$env:DB_USER = "your_mysql_user"
$env:DB_PASSWORD = "your_mysql_password"
$env:DB_HOST = "127.0.0.1"
$env:DB_PORT = "3306"
python manage.py migrate
python manage.py runserver
```

The same `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` variables can be set in the environment used to launch Django on other platforms. Do not commit credentials.

## Production settings

Set these environment variables in the deployment environment:

- `DJANGO_SECRET_KEY`: a unique, randomly generated secret key
- `DJANGO_DEBUG`: set to `false`
- `DJANGO_ALLOWED_HOSTS`: comma-separated hostnames, for example `jobs.example.com,www.jobs.example.com`

The app refuses to start with `DEBUG` disabled unless `DJANGO_SECRET_KEY` is provided. Configure HTTPS and review Django's deployment checklist before exposing the app publicly: <https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/>.

## Tests

```bash
python manage.py test applications
```

## License

No license has been selected yet. Choose one before publishing if you want to grant others explicit reuse rights.
