# Email Configuration Setup Guide

## Overview
The forgot password feature now sends actual password reset emails to users' email addresses. This guide explains how to set it up.

## Setup Instructions

### Option 1: Using Gmail (Recommended)

1. **Enable 2-Factor Authentication on your Gmail account**
   - Go to https://myaccount.google.com/security
   - Find "2-Step Verification" and enable it
   - Follow the verification steps

2. **Generate an App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" as the app
   - Select your device type (Windows Computer, etc.)
   - Google will generate a 16-character password
   - Copy this password (it's a one-time display)

3. **Create a `.env` file in your project root directory**
   ```
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
   ```
   Replace with your actual email and the 16-character app password generated above.

4. **Make sure the `.env` file is NOT committed to git**
   - Add `.env` to your `.gitignore` file if using git

5. **Restart your Django development server**
   ```
   python manage.py runserver
   ```

### How It Works

1. User clicks "Forgot Password" on the login page
2. User enters their email address
3. System generates a secure password reset token (valid for 1 hour)
4. Email is sent with a reset link and password reset button
5. User clicks the link and resets their password
6. User can now login with the new password

### Email Features

- **HTML-formatted email** with professional styling
- **Reset button** for easy access (works in all email clients)
- **Alternative link** for cases where the button doesn't work
- **Security information** about link expiration (1 hour)
- **Security notification** if they didn't request the reset

### Testing

To test without actually sending emails, you can temporarily switch to console backend:

In `restaurant_config/settings.py`, change:
```python
# Comment out this:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Uncomment this for testing:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Emails will then be printed to your console/terminal instead of being sent.

### Troubleshooting

**Issue: "Connection refused" or connection errors**
- Make sure 2-Factor Authentication is enabled on Gmail
- Make sure you're using an App Password, not your regular Gmail password
- Check that EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are correct in .env

**Issue: "Authentication failed"**
- The app password might be typed incorrectly
- Generate a new app password and try again
- Make sure there are no extra spaces in the .env file

**Issue: "SMTP connection error"**
- Check your internet connection
- Gmail's SMTP server is smtp.gmail.com on port 587
- This should work from most networks, but some corporate firewalls may block it

### Alternative Email Services

If Gmail doesn't work for you, consider:

- **SendGrid**: https://sendgrid.com (free tier available)
- **Mailgun**: https://mailgun.com (free tier available)
- **AWS SES**: https://aws.amazon.com/ses/
- **Office 365**: Use smtp.office365.com on port 587

### Files Modified

1. `restaurant_config/settings.py` - Email backend configuration
2. `accounts/views.py` - Improved forgot_password function with HTML email
3. `templates/email/password_reset_email.html` - New HTML email template

### Security Notes

- The reset link expires after 1 hour (set by PASSWORD_RESET_TIMEOUT)
- Each reset link is single-use (can't be reused)
- The system doesn't reveal if an email exists in the database
- Passwords are securely hashed using Django's default hasher
