# YKS Shop

Modern online shopping platform built with Django. Simple to set up, easy to extend, and ready for custom themes, payment flows, and order management.

## Highlights
- Clean, user-friendly shopping experience
- Cart, checkout, and order flow
- Admin-friendly product and inventory management
- Django templating ready for custom UI

## Tech Stack
- Backend: Django, Python
- Database: SQLite (default)
- Frontend: HTML, CSS, JavaScript

## Quick Start
```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open the app at `http://127.0.0.1:8000/`.

## How to Run the Project Locally

### Prerequisites
- Python 3.11 or higher
- Git (optional, for cloning)

### Step-by-Step Setup

1. **Navigate to the project directory:**
   ```bash
   cd F:\yksshop
   ```

2. **Create a virtual environment** (if not already created):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   
   **On Windows (Git Bash):**
   ```bash
   source venv/Scripts/activate
   ```
   
   **On Windows (Command Prompt):**
   ```cmd
   venv\Scripts\activate
   ```
   
   **On Windows (PowerShell):**
   ```powershell
   venv\Scripts\Activate.ps1
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note:** If you encounter pip path errors, use:
   ```bash
   python -m pip install -r requirements.txt
   ```

5. **Verify .env file exists:**
   The project includes a `.env` file with configuration. Make sure it's in the root directory (`F:\yksshop\.env`).

6. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

8. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

9. **Access the application:**
   - Main app: `http://127.0.0.1:8000/` or `http://localhost:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

### Quick Start (If virtual environment already exists)
```bash
source venv/Scripts/activate  # Activate venv
python manage.py migrate      # Run migrations (if needed)
python manage.py runserver    # Start server
```

Optional (admin access):
```bash
python manage.py createsuperuser
```

Then visit:
- App: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

## Common Commands

### Database
```bash
python manage.py makemigrations    # Create migration files
python manage.py migrate           # Apply migrations
python manage.py migrate --run-syncdb  # Sync database
```

### User Management
```bash
python manage.py createsuperuser   # Create admin user
python manage.py changepassword    # Change user password
```

### Development Server
```bash
python manage.py runserver                    # Run on default port 8000
python manage.py runserver 8080              # Run on custom port
python manage.py runserver 0.0.0.0:8000     # Allow external connections
```

### Static Files
```bash
python manage.py collectstatic    # Collect static files for production
```

### Other Useful Commands
```bash
python manage.py shell            # Open Django shell
python manage.py dbshell          # Open database shell
python manage.py check            # Check for common problems
python manage.py showmigrations   # Show migration status
```

## Project Structure
- `yksproject/` Django project settings
- `yksshop/` Main app
- `yksshop/templates/` Templates
- `staticfiles/` Static assets

## Configuration Notes

### Environment Variables
The project uses a `.env` file for configuration. Key settings include:
- `DEBUG=True` - Set to `False` for production
- Email settings (Gmail SMTP for development)
- Cloudinary settings (for image storage)
- Razorpay settings (for payments)
- Twilio settings (for WhatsApp notifications, optional)

### Database
- **Development:** SQLite (default, no setup required)
- **Production:** Can be configured to use MySQL/PostgreSQL

### Important Settings
- Update `ALLOWED_HOSTS` in `yksproject/settings.py` for production
- Set `DEBUG=False` in production
- Configure proper email backend for production
- Set up proper static file serving for production

## Troubleshooting

### ModuleNotFoundError: No module named 'dotenv'
```bash
python -m pip install python-dotenv
```

### Pip path errors or "Unable to create process"
Use `python -m pip` instead of `pip` directly:
```bash
python -m pip install -r requirements.txt
```

### Database errors
If you get database-related errors:
```bash
python manage.py migrate --run-syncdb
```

### Port already in use
If port 8000 is already in use:
```bash
python manage.py runserver 8080
```

### Static files not loading
Collect static files:
```bash
python manage.py collectstatic
```

### Cryptography ImportError (PyO3 modules error)
If you see `ImportError: PyO3 modules compiled for CPython 3.8 or older may only be initialized once per interpreter process`:
```bash
# Uninstall and reinstall cryptography and PyJWT
python -m pip uninstall -y cryptography PyJWT
python -m pip install --no-cache-dir --force-reinstall cryptography PyJWT
```
This error occurs when cryptography was compiled for an older Python version. Reinstalling ensures it's compiled for your current Python version.

### Virtual environment issues
If the virtual environment seems corrupted, recreate it:
```bash
# Remove old venv (optional)
rm -rf venv  # or rmdir /s venv on Windows CMD

# Create new venv
python -m venv venv
source venv/Scripts/activate  # or venv\Scripts\activate on Windows
python -m pip install -r requirements.txt
```

## Deployment on Render

### Quick Setup
1. Push your code to GitHub
2. Connect your repository to Render
3. Render will automatically detect `render.yaml` and use the build script

### Manual Configuration (if not using render.yaml)
If you're configuring manually in the Render dashboard:

**Build Command:**
```bash
./build.sh
```

Or if build.sh doesn't work, use:
```bash
pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput --clear
```

**Start Command:**
```bash
gunicorn yksproject.wsgi:application
```

### Important Notes
- The `build.sh` script automatically runs migrations during deployment
- Ensure all environment variables are set in the Render dashboard
- The build script will fail if migrations have errors, preventing broken deployments

### Troubleshooting
If you see "no such table" errors:
1. Check that the build command includes `python manage.py migrate`
2. Verify migrations are in the `yksshop/migrations/` directory
3. Check Render build logs to ensure migrations ran successfully

## Contributing
Pull requests are welcome. For major changes, open an issue first to discuss the proposal.

## License
Add your license information here.
