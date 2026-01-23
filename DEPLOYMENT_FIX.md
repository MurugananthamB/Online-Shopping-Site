# Fix for "no such table: yksshop_homehero" Error on Render

## Problem
The application was failing on Render with the error:
```
sqlite3.OperationalError: no such table: yksshop_homehero
```

This happens because database migrations weren't running during deployment.

## Solution Applied

### 1. Created Build Script (`build.sh`)
This script automatically runs migrations during the build phase on Render:
- Installs dependencies
- Runs database migrations
- Collects static files

### 2. Created Render Configuration (`render.yaml`)
This file configures Render to use the build script automatically.

### 3. Added Error Handling
Updated `HomeHero.get_solo()` method to gracefully handle cases where the table doesn't exist yet (prevents 500 errors during initial deployment).

## Next Steps

### Option 1: Using render.yaml (Recommended)
1. Push the updated code to GitHub
2. Render will automatically detect `render.yaml` and use the build script
3. The migrations will run automatically during build

### Option 2: Manual Configuration
If you're not using `render.yaml`, configure in Render dashboard:

1. Go to your Render service settings
2. Set **Build Command** to:
   ```bash
   ./build.sh
   ```
   Or if that doesn't work:
   ```bash
   pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput --clear
   ```

3. Set **Start Command** to:
   ```bash
   gunicorn yksproject.wsgi:application
   ```

### Verify the Fix
After deployment:
1. Check Render build logs - you should see "Running database migrations..."
2. The build should complete successfully
3. Visit your site - it should load without the table error

## Files Changed
- ✅ `build.sh` - Created build script
- ✅ `render.yaml` - Created Render configuration
- ✅ `yksshop/models.py` - Added error handling to `HomeHero.get_solo()`
- ✅ `README.md` - Added deployment instructions

## Important Notes
- The build script runs migrations with `--noinput` flag (non-interactive)
- Static files are collected during build for better performance
- Error handling in the model provides a fallback, but migrations should always run
