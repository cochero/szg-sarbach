# SZG Sarbach Health Centre - Deployment Guide

## Deploying to Shared Hosting with MySQL

This guide covers deploying the SZG Sarbach Health Centre Django application to shared hosting providers such as cPanel or Plesk with a MySQL database.

---

## Table of Contents

1. [Requirements](#1-requirements)
2. [Shared Hosting Setup](#2-shared-hosting-setup)
3. [Uploading Project Files](#3-uploading-project-files)
4. [MySQL Database Setup](#4-mysql-database-setup)
5. [Python Environment Setup](#5-python-environment-setup)
6. [Django Settings for Production](#6-django-settings-for-production)
7. [Running Migrations](#7-running-migrations)
8. [Static Files](#8-static-files)
9. [Creating the Super Admin](#9-creating-the-super-admin)
10. [WSGI Configuration (Passenger)](#10-wsgi-configuration-passenger)
11. [Domain Configuration](#11-domain-configuration)
12. [SSL / HTTPS Setup](#12-ssl--https-setup)
13. [Cron Jobs for Maintenance](#13-cron-jobs-for-maintenance)
14. [Environment Variables](#14-environment-variables)
15. [Backup Strategy](#15-backup-strategy)
16. [Troubleshooting](#16-troubleshooting)

---

## 1. Requirements

Before you begin, ensure your hosting environment meets these requirements:

- **Python 3.11** or higher
- **MySQL 5.7** or higher (or MariaDB 10.3+)
- **pip** (Python package manager)
- **SSH access** to the hosting server (recommended)
- **File Manager** or FTP access for uploading files
- At least **500 MB disk space** for the application and dependencies
- A registered **domain name** pointed to your hosting server

### Python Packages

The project depends on the following Python packages (listed in pyproject.toml):

- Django 5.2+
- django-widget-tweaks
- gunicorn
- Pillow (for image handling)
- mysqlclient (replaces psycopg2 for MySQL)
- python-dotenv
- whitenoise

---

## 2. Shared Hosting Setup

### cPanel

1. Log in to your cPanel account.
2. Navigate to **Setup Python App** (under the Software section).
3. Click **Create Application**.
4. Select **Python 3.11** (or the highest version available).
5. Set the **Application root** to your project directory (e.g., `szg_sarbach`).
6. Set the **Application URL** to your domain or subdomain.
7. Set the **Application startup file** to `passenger_wsgi.py`.
8. Click **Create**.
9. Note the path to the virtual environment that cPanel creates for you.

### Plesk

1. Log in to your Plesk panel.
2. Go to **Websites & Domains** and select your domain.
3. Click **Python** under the domain settings.
4. Enable Python support and select **Python 3.11**.
5. Set the document root to your project folder.
6. Configure the WSGI entry point as described in Section 10.

---

## 3. Uploading Project Files

Upload all project files to your hosting account using one of these methods:

### Via File Manager (cPanel/Plesk)

1. Compress the entire project folder into a ZIP file on your local machine.
2. Open File Manager in your hosting panel.
3. Navigate to the application root directory.
4. Upload the ZIP file and extract it.

### Via FTP

1. Connect to your hosting server using an FTP client (FileZilla, Cyberduck, etc.).
2. Upload all project files to the application root directory.

### Via SSH (recommended)

1. Connect to your server via SSH.
2. Navigate to the application root directory.
3. Use `git clone` or `scp` to transfer files.

**Important:** Make sure the following directories exist and are writable:

- `media/` (for uploaded images)
- `media/images/` (for treatment and doctor images)
- `staticfiles/` (will be created during static file collection)

---

## 4. MySQL Database Setup

### Creating the Database

#### In cPanel

1. Go to **MySQL Databases** in cPanel.
2. Under "Create New Database", enter a name such as `szg_sarbach_db` and click **Create Database**.
3. Under "MySQL Users", create a new user with a strong password.
4. Under "Add User to Database", select the user and the database, then click **Add**.
5. On the privileges screen, select **ALL PRIVILEGES** and click **Make Changes**.

#### In Plesk

1. Go to **Databases** under your domain.
2. Click **Add Database**.
3. Enter a database name, create a database user, and set a password.
4. Make sure the database type is **MySQL**.

### Database Character Set

Make sure the database uses UTF-8 encoding. Run the following SQL command in phpMyAdmin or via SSH:

```sql
ALTER DATABASE szg_sarbach_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 5. Python Environment Setup

### Activating the Virtual Environment

If your hosting provider created a virtual environment (cPanel does this automatically), activate it:

```bash
source /home/yourusername/virtualenv/szg_sarbach/3.11/bin/activate
```

### Installing Dependencies

Install the required Python packages. Since you are switching from PostgreSQL to MySQL, you need `mysqlclient` instead of `psycopg2`:

```bash
pip install django>=5.2
pip install django-widget-tweaks
pip install gunicorn
pip install Pillow
pip install mysqlclient
pip install python-dotenv
pip install whitenoise
```

Or install from the requirements file (create one first if needed):

```bash
pip install -r requirements.txt
```

**Note on mysqlclient:** If `mysqlclient` fails to install, you may need the MySQL development headers. Ask your hosting provider or try:

```bash
pip install PyMySQL
```

If using PyMySQL, add this to the top of `szg_sarbach/__init__.py`:

```python
import pymysql
pymysql.install_as_MySQLdb()
```

---

## 6. Django Settings for Production

Create a `.env` file in the project root directory with your production settings. Then modify `szg_sarbach/settings.py` for production use.

### Create the .env File

Create a file called `.env` in the same directory as `manage.py`:

```
DEBUG=False
SECRET_KEY=your-very-long-random-secret-key-here-change-this
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.mysql
DB_NAME=your_cpanel_prefix_szg_sarbach_db
DB_USER=your_cpanel_prefix_dbuser
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=3306
```

**Generate a secret key** using this Python command:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Modify settings.py for Production

Replace the database configuration section in `szg_sarbach/settings.py` with the following:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-in-production')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'yourdomain.com').split(',')

# Database Configuration - MySQL for Production
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.mysql'),
        'NAME': os.environ.get('DB_NAME', 'szg_sarbach_db'),
        'USER': os.environ.get('DB_USER', 'dbuser'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security headers for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com', 'https://www.yourdomain.com']

# If using HTTPS (recommended)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

**Important:** Replace `yourdomain.com` with your actual domain name in both `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.

---

## 7. Running Migrations

After configuring the database, create all the necessary tables:

```bash
python manage.py migrate
```

If you encounter errors, try running migrations app by app:

```bash
python manage.py migrate core
python manage.py migrate clinic
python manage.py migrate appointments
python manage.py migrate shop
python manage.py migrate blog_app
python manage.py migrate admin_panel
```

---

## 8. Static Files

Collect all static files into the `STATIC_ROOT` directory:

```bash
python manage.py collectstatic --noinput
```

This copies all CSS, JavaScript, images, and other static assets to the `staticfiles/` directory. WhiteNoise (already configured in the project) will serve these files efficiently.

If you need to serve static files through Apache/Nginx on your hosting, configure an alias:

- For Apache (in `.htaccess` or virtual host config):
  ```
  Alias /static/ /home/yourusername/szg_sarbach/staticfiles/
  Alias /media/ /home/yourusername/szg_sarbach/media/
  ```

---

## 9. Creating the Super Admin

Create the initial administrator account:

```bash
python manage.py createsuperuser
```

You will be prompted for a username, email, and password. Use these credentials to log into the admin panel at `/welcome/admin/`.

**Recommended:** Use `admin` as the username for consistency with the application's login system.

---

## 10. WSGI Configuration (Passenger)

Most shared hosting providers use Phusion Passenger to serve Python applications. Create a file called `passenger_wsgi.py` in the project root directory:

```python
import os
import sys

# Add the project directory to the Python path
project_home = os.path.dirname(os.path.abspath(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'szg_sarbach.settings'

# Load the .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import and set up the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### For cPanel with Passenger

1. Go to **Setup Python App** in cPanel.
2. Make sure the **Application startup file** is set to `passenger_wsgi.py`.
3. Click **Restart** to apply changes.

### For Apache with mod_wsgi (Alternative)

If your hosting uses mod_wsgi instead of Passenger, add this to your `.htaccess` file:

```apache
AddHandler wsgi-script .py
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ /passenger_wsgi.py/$1 [QSA,L]
```

### Creating the .htaccess File

Create an `.htaccess` file in the project root:

```apache
PassengerEnabled On
PassengerAppRoot /home/yourusername/szg_sarbach
PassengerPython /home/yourusername/virtualenv/szg_sarbach/3.11/bin/python

# Serve static files directly
RewriteEngine On
RewriteCond %{REQUEST_URI} ^/static/
RewriteRule ^(.*)$ - [L]
RewriteCond %{REQUEST_URI} ^/media/
RewriteRule ^(.*)$ - [L]
```

---

## 11. Domain Configuration

### DNS Settings

Point your domain to your hosting server by updating your DNS records:

1. **A Record:** Point `@` (root domain) to your server's IP address.
2. **A Record:** Point `www` to your server's IP address.
3. **CNAME Record (alternative):** Point `www` to `yourdomain.com`.

### In cPanel

1. Go to **Domains** or **Addon Domains**.
2. Add your domain and point it to the project directory.
3. Wait for DNS propagation (up to 24-48 hours).

### Update Django Settings

After configuring your domain, update these settings in your `.env` file:

```
ALLOWED_HOSTS=sarbach.swiss,www.sarbach.swiss
```

And update `CSRF_TRUSTED_ORIGINS` in `settings.py`:

```python
CSRF_TRUSTED_ORIGINS = ['https://sarbach.swiss', 'https://www.sarbach.swiss']
```

---

## 12. SSL / HTTPS Setup

### Free SSL with Let's Encrypt (cPanel)

1. Go to **SSL/TLS** in cPanel.
2. Click **Manage SSL Sites** or use **AutoSSL**.
3. cPanel's AutoSSL feature will automatically install a free Let's Encrypt certificate.
4. Enable **Force HTTPS Redirect** in cPanel or add to `.htaccess`:

```apache
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

### Free SSL with Let's Encrypt (Plesk)

1. Go to **SSL/TLS Certificates** under your domain in Plesk.
2. Click **Install** next to Let's Encrypt.
3. Select your domain and enable "Redirect HTTP to HTTPS".

### Django HTTPS Settings

Once SSL is active, ensure these settings are in `settings.py`:

```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

---

## 13. Cron Jobs for Maintenance

Set up cron jobs for regular maintenance tasks.

### In cPanel

Go to **Cron Jobs** and add the following:

**Daily: Clean expired sessions**

```
0 3 * * * /home/yourusername/virtualenv/szg_sarbach/3.11/bin/python /home/yourusername/szg_sarbach/manage.py clearsessions
```

**Daily: Database backup (see Backup Strategy below)**

```
0 2 * * * mysqldump -u dbuser -p'yourpassword' szg_sarbach_db > /home/yourusername/backups/db_$(date +\%Y\%m\%d).sql
```

**Weekly: Collect static files (in case of updates)**

```
0 4 * * 0 /home/yourusername/virtualenv/szg_sarbach/3.11/bin/python /home/yourusername/szg_sarbach/manage.py collectstatic --noinput
```

**Monthly: Clean old backups (keep last 30 days)**

```
0 5 1 * * find /home/yourusername/backups/ -name "db_*.sql" -mtime +30 -delete
```

---

## 14. Environment Variables

The following environment variables should be set in the `.env` file:

| Variable | Description | Example Value |
|---|---|---|
| `SECRET_KEY` | Django secret key (generate a unique one) | `a-long-random-string` |
| `DEBUG` | Debug mode (must be False in production) | `False` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed domains | `sarbach.swiss,www.sarbach.swiss` |
| `DB_ENGINE` | Database engine | `django.db.backends.mysql` |
| `DB_NAME` | MySQL database name | `szg_sarbach_db` |
| `DB_USER` | MySQL database username | `szg_dbuser` |
| `DB_PASSWORD` | MySQL database password | `your-secure-password` |
| `DB_HOST` | MySQL host | `localhost` |
| `DB_PORT` | MySQL port | `3306` |

---

## 15. Backup Strategy

### Database Backups

**Automated daily backups via cron (recommended):**

```bash
mysqldump -u dbuser -p'yourpassword' szg_sarbach_db > /home/yourusername/backups/db_$(date +%Y%m%d).sql
```

**Manual backup via phpMyAdmin:**

1. Open phpMyAdmin from cPanel.
2. Select the `szg_sarbach_db` database.
3. Click **Export**.
4. Choose **Quick** export method and **SQL** format.
5. Click **Go** to download the backup.

### Media File Backups

Back up uploaded images and files from the `media/` directory:

```bash
tar -czf /home/yourusername/backups/media_$(date +%Y%m%d).tar.gz /home/yourusername/szg_sarbach/media/
```

### Restoring from Backup

**Database restore:**

```bash
mysql -u dbuser -p'yourpassword' szg_sarbach_db < /home/yourusername/backups/db_20250101.sql
```

**Media files restore:**

```bash
tar -xzf /home/yourusername/backups/media_20250101.tar.gz -C /home/yourusername/szg_sarbach/
```

### Backup Retention

- Keep daily backups for the last 30 days.
- Keep weekly backups for the last 3 months.
- Keep monthly backups for the last year.

---

## 16. Troubleshooting

### Common Issues and Solutions

#### "DisallowedHost" Error

**Problem:** Django returns a "DisallowedHost" error page.
**Solution:** Add your domain to the `ALLOWED_HOSTS` setting in your `.env` file. Include both `yourdomain.com` and `www.yourdomain.com`.

#### "ModuleNotFoundError: No module named 'MySQLdb'"

**Problem:** MySQL client library is not installed.
**Solution:** Install `mysqlclient`:
```bash
pip install mysqlclient
```
If that fails, install PyMySQL as a fallback:
```bash
pip install PyMySQL
```
Then add to `szg_sarbach/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

#### Static Files Not Loading (404 Errors)

**Problem:** CSS, JavaScript, or images are not loading.
**Solution:**
1. Run `python manage.py collectstatic --noinput`.
2. Verify that `STATIC_ROOT` is set correctly.
3. Check that WhiteNoise middleware is in `MIDDLEWARE` in settings.py.
4. In cPanel, verify that the static directory is accessible via the web.

#### "CSRF Verification Failed"

**Problem:** Form submissions fail with CSRF errors.
**Solution:** Add your domain to `CSRF_TRUSTED_ORIGINS` in settings.py:
```python
CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com', 'https://www.yourdomain.com']
```

#### "OperationalError: (2002) Can't connect to MySQL server"

**Problem:** Django cannot connect to MySQL.
**Solution:**
1. Verify database credentials in your `.env` file.
2. Make sure the database exists and the user has access.
3. Try `DB_HOST=127.0.0.1` instead of `localhost`.

#### "Internal Server Error (500)" with No Details

**Problem:** The site shows a 500 error but no details.
**Solution:**
1. Temporarily set `DEBUG=True` in `.env` to see the full error.
2. Check the error log at `/home/yourusername/logs/error.log` or in cPanel under **Error Log**.
3. After fixing the issue, set `DEBUG=False` again.

#### Media Files (Images) Not Showing

**Problem:** Uploaded images (treatments, doctors, etc.) do not display.
**Solution:**
1. Ensure the `media/` directory exists and is writable: `chmod 755 media/`.
2. In production, configure your web server to serve files from the `media/` directory.
3. Add an Alias in your Apache config or `.htaccess` for the `/media/` path.

#### Passenger App Not Starting

**Problem:** The application does not load after deployment.
**Solution:**
1. Check the `passenger_wsgi.py` file is in the correct location.
2. Verify the Python path in your Passenger configuration.
3. Check the error logs: cPanel > Metrics > Errors.
4. Restart the Python app from the cPanel "Setup Python App" page.

#### Migrations Fail

**Problem:** `python manage.py migrate` throws errors.
**Solution:**
1. Make sure the database is empty (no conflicting tables).
2. Run `python manage.py migrate --run-syncdb` to synchronize all tables.
3. If a specific app fails, try migrating it individually:
   ```bash
   python manage.py migrate core
   python manage.py migrate clinic
   ```

---

## Quick Deployment Checklist

- [ ] Upload project files to hosting
- [ ] Create MySQL database and user
- [ ] Install Python dependencies (including `mysqlclient`)
- [ ] Create `.env` file with production settings
- [ ] Update `settings.py` for MySQL and production
- [ ] Run `python manage.py migrate`
- [ ] Run `python manage.py collectstatic --noinput`
- [ ] Run `python manage.py createsuperuser`
- [ ] Create `passenger_wsgi.py`
- [ ] Configure domain DNS
- [ ] Install SSL certificate
- [ ] Set up cron jobs for backups and maintenance
- [ ] Test all pages and login portals
- [ ] Set `DEBUG=False`
- [ ] Restart the application

---

## Support

For technical support:
- **Email:** help@sarbach.swiss
- **Phone:** +41 79 290 77 44
- **Address:** Dorfstrasse 19, CH-3954 Leukerbad, Wallis
