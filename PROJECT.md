# YKS Shop - E-Commerce Platform

## Project Overview

**YKS Shop** is a full-featured Django-based e-commerce platform specializing in men's wear. The application provides a complete online shopping experience with user authentication, product management, shopping cart functionality, order processing, and integrated payment gateway support.

## Technology Stack

### Backend Framework
- **Django 5.2.1** - High-level Python web framework
- **Django REST Framework** - For building RESTful APIs
- **Django AllAuth** - Integrated authentication solution with social login support

### Database
- **SQLite3** - Default database for development (can be configured for MySQL/PostgreSQL in production)

### Authentication & Security
- **JWT (JSON Web Tokens)** - Token-based authentication via `djangorestframework-simplejwt`
- **Django AllAuth** - Email-based authentication with OTP verification
- **Google OAuth** - Social authentication provider

### Payment Integration
- **Razorpay** - Payment gateway for online transactions
- Support for both online payments and Cash on Delivery (COD)

### Media & Storage
- **Cloudinary** - Cloud-based image storage and management
- **Pillow** - Image processing library

### Communication
- **Twilio** - WhatsApp notifications for order updates (optional)
- **SMTP Email** - Email notifications for registration, orders, and password resets

### Deployment & Production
- **Gunicorn** - WSGI HTTP server for production
- **WhiteNoise** - Static file serving for production

### Development Tools
- **python-dotenv** - Environment variable management
- **Cryptography** - Secure data encryption

## Project Structure

```
yksshop/
├── yksproject/              # Main Django project settings
│   ├── settings.py         # Project configuration
│   ├── urls.py            # Root URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
│
├── yksshop/                # Main application
│   ├── models.py          # Database models (Product, Order, Cart, etc.)
│   ├── views.py           # Web views and business logic
│   ├── jwt_views.py       # JWT authentication views
│   ├── auth_views.py      # Custom authentication views
│   ├── web_urls.py        # Web page URL routing
│   ├── api_urls.py        # API endpoint routing
│   ├── admin.py           # Django admin configuration
│   ├── signals.py         # Django signals
│   ├── notifications.py   # Notification handling
│   ├── jwt_middleware.py  # JWT authentication middleware
│   └── templates/         # HTML templates
│       └── shop/          # Shop-related templates
│
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── db.sqlite3            # SQLite database (development)
├── media/                # Local media files (development)
├── staticfiles/          # Collected static files
└── venv/                 # Python virtual environment
```

## Core Features

### 1. User Authentication & Management
- **Email-based Registration** with OTP verification
- **Email Activation** via activation links
- **JWT Token Authentication** for API access
- **Password Reset** functionality
- **User Profiles** with phone number
- **Social Login** via Google OAuth (Django AllAuth)

### 2. Product Management
- **Product Catalog** with categories
- **Product Variants** (size-based: XS, S, M, L, XL, XXL)
- **Product Images** with gallery support
- **Stock Management** per product and variant
- **Product Search & Filtering**
- **Cloudinary Integration** for image storage

### 3. Shopping Cart
- **Persistent Shopping Cart** per user
- **Add/Update/Remove** cart items via AJAX
- **Size Selection** for products with variants
- **Real-time Stock Validation**
- **Cart Total Calculation**

### 4. Order Management
- **Order Placement** with shipping details
- **Order Tracking** with status updates (Pending, Processing, Shipped, Delivered, Cancelled)
- **Order History** for users
- **Order Details** view
- **Unique Order Numbers** generation

### 5. Payment Integration
- **Razorpay Integration** for online payments
- **Payment Verification** with signature validation
- **Cash on Delivery (COD)** option
- **Payment Success/Failure** handling

### 6. Notifications
- **Email Notifications** for:
  - Registration confirmation
  - Order confirmations
  - Order status updates
  - Password reset links
- **WhatsApp Notifications** (optional, via Twilio)

### 7. Admin Panel
- **Django Admin Interface** for:
  - Product management
  - Order management
  - User management
  - Category management
  - Homepage hero content customization

## API Endpoints

### Authentication Endpoints
- `POST /api/token/` - Obtain JWT access and refresh tokens
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/token/verify/` - Verify token validity
- `POST /api/login/` - JWT login endpoint
- `GET /api/user/` - Get current user information

### Cart & Order Endpoints
- `POST /api/add-to-cart/` - Add product to cart
- `POST /api/update-cart/` - Update cart item quantity
- `POST /api/remove-from-cart/` - Remove item from cart
- `POST /api/place-order/` - Place a new order

## Web Pages

### Public Pages
- `/` - Homepage with hero section
- `/home/` - Homepage (alternative)
- `/products/` - Product listing page
- `/product/<slug>/` - Product detail page

### Authentication Pages
- `/register/` - User registration
- `/verify-otp/` - OTP verification
- `/login/` - User login
- `/logout/` - User logout
- `/password-reset/` - Password reset request
- `/reset/<uidb64>/<token>/` - Password reset confirmation

### User Pages
- `/profile/` - User profile page
- `/cart/` - Shopping cart view
- `/checkout/` - Checkout page
- `/orders/` - Order history
- `/order/<order_id>/` - Order details

### Payment Pages
- `/create-razorpay-order/<order_id>/` - Create Razorpay order
- `/razorpay-payment-success/` - Payment success handler
- `/razorpay-payment-failure/<order_id>/` - Payment failure handler
- `/order-success/<order_id>/` - Order success page

## Database Models

### User Models
- **User** - Django's built-in user model (extended)
- **Profile** - User profile with phone number
- **PendingUser** - Temporary user during OTP verification

### Product Models
- **Category** - Product categories
- **Product** - Main product model with pricing and stock
- **ProductVariant** - Size variants (XS, S, M, L, XL, XXL)
- **ProductImage** - Product image gallery

### E-Commerce Models
- **Cart** - User shopping cart
- **CartItem** - Individual cart items
- **Order** - Customer orders
- **OrderItem** - Order line items

### Content Models
- **HomeHero** - Homepage hero section content

## Environment Variables

The project uses environment variables for configuration. Create a `.env` file in the root directory:

### Required for Production
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
```

### Cloudinary (Image Storage)
```env
CLOUD_NAME=your-cloudinary-cloud-name
API_KEY=your-cloudinary-api-key
API_SECRET=your-cloudinary-api-secret
# OR use CLOUDINARY_URL
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
```

### Email Configuration (Development)
```env
DEV_EMAIL_HOST=smtp.gmail.com
DEV_EMAIL_PORT=587
DEV_EMAIL_USE_TLS=True
DEV_EMAIL_HOST_USER=your-email@gmail.com
DEV_EMAIL_HOST_PASSWORD=your-app-password
```

### Email Configuration (Production)
```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-sendgrid-username
EMAIL_HOST_PASSWORD=your-sendgrid-password
DEFAULT_FROM_EMAIL=YKS Men's Wear <no-reply@yksshop.com>
```

### Razorpay Payment Gateway
```env
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
```

### Twilio (Optional - WhatsApp Notifications)
```env
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_WHATSAPP_FROM=+14155238886
```

## Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd yksshop
```

### Step 2: Create and Activate Virtual Environment
```bash
# Windows (Git Bash)
source venv/Scripts/activate

# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the root directory with required variables (see Environment Variables section above).

### Step 5: Run Database Migrations
```bash
python manage.py migrate
```

### Step 6: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 7: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 8: Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Development Workflow

### Running Migrations
```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Creating Management Commands
The project includes custom management commands in `yksshop/management/commands/`

### Running Tests
```bash
python manage.py test
```

### Accessing Admin Panel
Navigate to `http://127.0.0.1:8000/admin/` and login with superuser credentials.

## Production Deployment

### Key Considerations
1. Set `DEBUG=False` in production
2. Configure proper `ALLOWED_HOSTS`
3. Use a production database (MySQL/PostgreSQL)
4. Set up proper static file serving (WhiteNoise or CDN)
5. Configure HTTPS for secure connections
6. Set secure cookie flags (`CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`)
7. Use environment variables for sensitive data
8. Configure proper email backend (SendGrid, AWS SES, etc.)

### Using Gunicorn
```bash
gunicorn yksproject.wsgi:application
```

### Environment Variables for Production
Ensure all production environment variables are set:
- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS` (configured in settings)
- Cloudinary credentials
- Email service credentials
- Razorpay credentials

## Security Features

- **JWT Token Authentication** with refresh token rotation
- **CSRF Protection** enabled
- **Password Hashing** using Django's password hashers
- **OTP Verification** for email registration
- **Email Activation** links for account verification
- **Secure Cookie Settings** (configurable for HTTPS)
- **Razorpay Payment Verification** with signature validation

## File Organization (Based on .gitignore)

The `.gitignore` file ensures the following are excluded from version control:

### Excluded Files & Directories
- **Virtual Environments**: `venv/`, `ENV/`, `env/`
- **Python Cache**: `__pycache__/`, `*.pyc`, `*.pyo`
- **Environment Variables**: `.env`, `.env.local`
- **IDE Files**: `.vscode/`, `.idea/`, `*.swp`
- **OS Files**: `.DS_Store`, `Thumbs.db`
- **Build Artifacts**: `build/`, `dist/`, `*.egg-info/`
- **Logs**: `*.log`
- **Test Coverage**: `.coverage`, `.pytest_cache/`
- **Sensitive Files**: `rzp-key-secret.txt` (Razorpay keys)
- **Node Modules**: `node_modules/` (if any frontend dependencies)

## API Documentation

The REST API uses JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### Example API Request
```bash
curl -X GET http://127.0.0.1:8000/api/user/ \
  -H "Authorization: Bearer <your-access-token>"
```

## Support & Maintenance

### Common Issues

1. **Database Errors**: Run `python manage.py migrate`
2. **Static Files Not Loading**: Run `python manage.py collectstatic`
3. **Import Errors**: Ensure virtual environment is activated
4. **Cloudinary Errors**: Verify environment variables are set correctly
5. **Email Not Sending**: Check email configuration in `.env` file

### Logging
Check Django logs for debugging. In production, configure proper logging handlers.

## License

[Specify your license here]

## Contributors

[Add contributor information]

---

**Note**: This project uses SQLite3 for development. For production, consider migrating to PostgreSQL or MySQL for better performance and scalability.

