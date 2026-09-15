# OTP-Based Password Reset System - Complete Guide

## Overview

The password reset system has been updated to use **OTP (One-Time Password)** instead of token-based links. This provides a more user-friendly and secure experience.

## How It Works

### User Flow

1. **Request Password Reset**
   - User enters their email address on the "Forgot Password" page
   - System generates a random 6-digit OTP
   - OTP is sent to their Gmail address with detailed instructions
   - User receives confirmation message

2. **Verify OTP**
   - User receives email with 6-digit code
   - User enters their email and OTP code on the verification page
   - System validates the OTP (valid for 10 minutes)
   - User has 3 attempts to enter correct OTP

3. **Reset Password**
   - After OTP verification, user sets a new password
   - Password requirements: minimum 8 characters
   - Confirmation field ensures password is entered correctly
   - Password strength indicator shows quality in real-time

4. **Success**
   - Password is updated in the system
   - User can login with new password immediately

## Features

✅ **6-Digit OTP Code**
- Randomly generated for each request
- Easy to enter and verify
- Printed in email for easy reference

✅ **Security Features**
- OTP expires after 10 minutes
- Can only be used once
- Maximum 3 attempts before requiring new OTP
- Each user can only have one active OTP at a time

✅ **User-Friendly**
- Clear step-by-step instructions
- HTML-formatted email with visual OTP code
- Real-time password strength indicator
- Password match validation

✅ **Email Integration**
- Professional HTML email template
- Security warnings included
- Works with Gmail SMTP
- Plain text fallback

## Setup

### Prerequisites

Your `.env` file should contain:

```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
```

If you don't have a Gmail App Password yet, see the SMTP Email Setup section below.

### SMTP Email Configuration

The system is configured to use Gmail SMTP for sending emails.

**Using Gmail:**

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and your device type
   - Copy the generated 16-character password
3. Add to `.env` file

## URL Routes

| URL | View | Purpose |
|-----|------|---------|
| `/accounts/forgot-password/` | forgot_password | Request OTP |
| `/accounts/verify-otp/` | verify_otp | Verify OTP code |
| `/accounts/reset-password/` | reset_password_after_otp | Reset password |

## Database

### New Model: PasswordResetOTP

```
- user (OneToOne to User)
- email (EmailField)
- otp_code (CharField, 6 digits)
- created_at (DateTime, auto)
- expires_at (DateTime, 10 minutes)
- is_used (Boolean, default False)
- attempts (Integer, default 0)
```

**Methods:**
- `generate_otp()` - Generates random 6-digit OTP
- `is_valid()` - Checks if OTP is not expired and not used
- `create_otp_for_user()` - Creates/updates OTP for user

## Customization

### Change OTP Expiration Time

In `accounts/models.py`, change this line:
```python
expires_at=timezone.now() + timedelta(minutes=10)  # Change 10 to desired minutes
```

### Change Maximum Attempts

In `accounts/views.py`, in the `verify_otp` function:
```python
if otp_instance.attempts >= 3:  # Change 3 to desired number
```

### Change Password Requirements

In `accounts/views.py`, in the `reset_password_after_otp` function:
```python
if len(password) < 8:  # Change 8 to desired length
```

## Testing

### Manual Testing

1. Go to `/accounts/forgot-password/`
2. Enter your email address (must be registered)
3. Check your email for the OTP code
4. Enter the OTP on the verification page
5. Set a new password
6. Login with new password

### With Console Email Backend (For Development)

To test without actually sending emails, update `settings.py`:

```python
# Comment out this:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Uncomment this:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Emails will then be printed to your console instead of being sent.

## Troubleshooting

### "OTP has expired"
- OTPs are valid for 10 minutes
- Solution: Request a new OTP

### "Too many incorrect attempts"
- You have 3 attempts to enter the correct OTP
- Solution: Go back to forgot password page and request new OTP

### "Invalid email or OTP"
- Email doesn't match the one OTP was sent to
- OTP code is incorrect
- Solution: Check email and OTP code carefully

### "SMTP Authentication Error"
- Gmail credentials in `.env` are incorrect
- 2-Factor Authentication not enabled
- Solution: Verify `.env` file and Gmail settings

### "ModuleNotFoundError: No module named 'decouple'"
- python-decouple is not installed
- Solution: Run `pip install python-decouple`

## Files Modified/Created

### Modified:
- `accounts/models.py` - Added PasswordResetOTP model
- `accounts/views.py` - Updated forgot_password, added verify_otp and reset_password_after_otp
- `accounts/urls.py` - Added new URL routes
- `templates/forgot_password.html` - Updated UI

### Created:
- `templates/verify_otp.html` - OTP verification page
- `templates/reset_password_after_otp.html` - Password reset form
- `templates/email/otp_email.html` - HTML email template
- `accounts/migrations/0002_passwordresetotp.py` - Database migration

## Email Template

The OTP email includes:
- Prominent display of 6-digit code
- Expiration time information
- Security warnings
- Link to report misuse
- Professional branding

## Security Considerations

1. **OTP Length**: 6 digits = 1 million possible combinations
2. **Expiration**: 10 minutes limits window for brute force
3. **Attempt Limiting**: 3 attempts prevents brute force
4. **Single Use**: OTP cannot be reused
5. **Email Verification**: User must have access to their email
6. **No Logging**: OTP codes are not logged (except in console backend)

## Future Enhancements

Potential improvements:
- SMS-based OTP as alternative
- OTP length configurability
- Custom email templates per user role
- Analytics on password reset attempts
- Multi-language email support

## Support

For issues or questions about the password reset system, check:
1. Console/server logs for error details
2. Email spam folder if OTP email not received
3. Gmail account security settings
