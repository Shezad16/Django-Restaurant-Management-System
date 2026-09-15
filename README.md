# Restaurant Management Web Application

A complete Django-based Restaurant Management System with frontend built using HTML, CSS, Bootstrap, and JavaScript.

## Features

### 1. **Authentication System**
- User registration with email validation
- Secure login/logout functionality
- Role-based access control (Admin, Customer)
- User profile management

### 2. **Menu Management**
- Browse restaurant menu organized by categories (Starters, Main Course, Desserts, Drinks)
- Search functionality to find items by name or description
- Filter menu items by category
- Detailed view for each menu item
- Product images (with fallback)

### 3. **Shopping Cart & Ordering**
- Add items to cart with quantity selection
- Update cart quantities
- Remove items from cart
- View cart summary with total pricing
- Checkout process
- Order history with status tracking
- Order detail view

### 4. **Order Management**
- Place orders with special instructions
- Order status tracking (Pending, Preparing, Ready, Delivered, Cancelled)
- Admin panel to update order status
- Customer order history

### 5. **Table Booking System**
- Book tables with date, time, and number of guests
- Special requests for bookings
- Booking confirmation
- Booking history
- Cancel bookings
- Booking status management

### 6. **Contact & Feedback**
- Contact form for customers
- Star rating system (1-5 stars)
- Message storage in database
- Admin view of all messages

### 7. **Responsive Design**
- Mobile-friendly Bootstrap 5 layout
- Responsive navigation bar
- Works on all device sizes

### 8. **Admin Dashboard**
- Django admin panel for managing:
  - Users and roles
  - Menu items and categories
  - Orders and order items
  - Table bookings
  - Contact messages

## Project Structure

```
restaurant_project/
├── venv/                          # Virtual environment
├── db.sqlite3                      # Database file
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
├── restaurant_config/              # Main project settings
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── accounts/                       # User authentication app
│   ├── models.py                  # User model
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── menu/                          # Menu management app
│   ├── models.py                  # Category, MenuItem models
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── orders/                        # Order management app
│   ├── models.py                  # Order, OrderItem models
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── booking/                       # Table booking app
│   ├── models.py                  # Booking model
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── contact/                       # Contact/Feedback app
│   ├── models.py                  # ContactMessage model
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── templates/                     # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── menu.html
│   ├── menu_detail.html
│   ├── cart.html
│   ├── checkout.html
│   ├── order_history.html
│   ├── order_detail.html
│   ├── booking.html
│   ├── booking_confirmation.html
│   ├── booking_history.html
│   ├── contact.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   └── cancel_booking.html
├── static/                        # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
├── media/                         # User-uploaded files
│   ├── menu_items/
│   └── categories/
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Navigate to Project Directory
```bash
cd "path/to/final restaurant project"
```

### Step 2: Activate Virtual Environment
On Windows:
```bash
.\venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:
```bash
pip install django djangorestframework python-decouple pillow
```

### Step 4: Run Migrations
```bash
python manage.py migrate
```

### Step 5: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account:
- Username: admin
- Email: admin@gmail.com
- Password: (set your own)

### Step 6: Start Development Server
```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## Usage

### Customer Functions
1. **Register/Login**: Create an account or login to existing account
2. **Browse Menu**: View all menu items, search, and filter by category
3. **Add to Cart**: Select items and quantities, add to shopping cart
4. **Checkout**: Review order and confirm purchase
5. **Track Orders**: View order history and status
6. **Book Table**: Reserve a table for dining in
7. **Contact Us**: Send feedback and ratings

### Admin Functions
1. **Admin Panel**: Access at `http://127.0.0.1:8000/admin/`
2. **Manage Menu**: Add, edit, delete menu items and categories
3. **View Orders**: See all orders and update their status
4. **Manage Bookings**: View and manage table bookings
5. **View Messages**: Read customer contact/feedback messages
6. **User Management**: Manage users and roles

## Models

### User Model (accounts/models.py)
- Extends Django's AbstractUser
- Fields: username, email, first_name, last_name, role, phone, address

### Category Model (menu/models.py)
- Fields: name, description, image

### MenuItem Model (menu/models.py)
- Fields: category, name, description, price, image, is_available

### Order Model (orders/models.py)
- Fields: user, status, total_price, special_instructions, created_at, updated_at

### OrderItem Model (orders/models.py)
- Fields: order, menu_item, quantity, price

### Booking Model (booking/models.py)
- Fields: user, booking_date, booking_time, number_of_people, special_requests, status

### ContactMessage Model (contact/models.py)
- Fields: name, email, phone, message, rating, is_read

## URL Routing

| URL | Purpose |
|-----|---------|
| `/` | Home page |
| `/accounts/register/` | User registration |
| `/accounts/login/` | User login |
| `/accounts/logout/` | User logout |
| `/accounts/profile/` | User profile |
| `/menu/` | Browse menu |
| `/menu/item/<id>/` | Menu item details |
| `/orders/cart/` | Shopping cart |
| `/orders/add/<id>/` | Add to cart |
| `/orders/remove/<id>/` | Remove from cart |
| `/orders/checkout/` | Checkout |
| `/orders/history/` | Order history |
| `/orders/detail/<id>/` | Order details |
| `/booking/` | Book table |
| `/booking/history/` | Booking history |
| `/booking/cancel/<id>/` | Cancel booking |
| `/contact/` | Contact form |
| `/admin/` | Django admin |

## Adding Menu Items (As Admin)

1. Login to admin panel: `http://127.0.0.1:8000/admin/`
2. Navigate to "Categories" and create categories if needed
3. Navigate to "Menu Items"
4. Click "Add Menu Item"
5. Fill in details:
   - Name
   - Description
   - Price
   - Category
   - Image (optional)
   - Is Available (checkbox)
6. Click "Save"

## Features Breakdown

### Authentication
- Secure password hashing
- Session management
- Login required decorators on protected views
- Registration form validation

### Cart System
- Session-based cart storage (can be upgraded to database)
- Real-time cart updates
- Quantity management
- Automatic total calculation

### Order Management
- Order status workflow (Pending → Preparing → Ready → Delivered)
- Order history tracking
- Special instructions support
- Admin order management

### Responsive Design
- Bootstrap 5 framework
- Mobile-first approach
- Responsive navigation
- Touch-friendly buttons
- Optimized for all screen sizes

## Customization

### Change Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #d4543f;    /* Change this */
    --secondary-color: #2c3e50;  /* Or this */
}
```

### Add Menu Items Programmatically
Use Django management command or admin panel.

### Configure Email Notifications
Update `settings.py` with email configuration for order/booking confirmations.

## Deployment

For production deployment:

1. Set `DEBUG = False` in `settings.py`
2. Set `ALLOWED_HOSTS` to your domain
3. Use a production database (PostgreSQL recommended)
4. Set up static files with WhiteNoise or CDN
5. Use environment variables for sensitive data
6. Deploy using Gunicorn + Nginx

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Database Issues
```bash
python manage.py migrate --run-syncdb
```

### Clear Django Cache
```bash
python manage.py cache_clear
```

## Future Enhancements

- [ ] Payment gateway integration (Stripe/PayPal)
- [ ] Email notifications for orders/bookings
- [ ] SMS notifications
- [ ] Rating system for food items
- [ ] Loyalty program/rewards
- [ ] Delivery tracking
- [ ] Admin analytics dashboard
- [ ] REST API with DRF
- [ ] Mobile app
- [ ] Multi-language support

## Technologies Used

- **Backend**: Django 6.0.4
- **Database**: SQLite (development)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Image Processing**: Pillow
- **REST Framework**: Django REST Framework

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please:
1. Check the documentation
2. Review the code comments
3. Test with sample data
4. Check browser console for JavaScript errors

## Admin Credentials (Default)
- Username: admin
- Email: admin@gmail.com
- Password: admin (change after first login!)

---

**Happy Restaurant Management!** 🍽️
