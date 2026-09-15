from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from .models import User, PasswordResetOTP
from django.views.decorators.http import require_http_methods


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long!')
            return redirect('register')
        
        if not any(c.isupper() for c in password) or not any(c.islower() for c in password) or not any(c.isdigit() for c in password) or not any(not c.isalnum() for c in password):
            messages.error(request, 'Password should include uppercase, lowercase, number, and symbol for a stronger password.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('register')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='customer'
        )
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')
    
    return render(request, 'register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!!!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('home')


@login_required
def profile(request):
    user = request.user
    context = {'user': user}
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone = request.POST.get('phone', user.phone)
        user.address = request.POST.get('address', user.address)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'profile.html', context)


def forgot_password(request):
    """Handle forgot password request - send OTP to email"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            # Create OTP for this user
            otp_instance = PasswordResetOTP.create_otp_for_user(user, email)
            
            # Send OTP via email
            subject = 'Password Reset OTP - Restaurant Management'
            context = {
                'user_name': user.first_name or user.username,
                'otp_code': otp_instance.otp_code,
                'expires_in': '10 minutes',
                'domain': request.get_host(),
            }
            
            # HTML Email
            html_message = render_to_string('email/otp_email.html', context)
            
            # Plain text fallback
            plain_message = f"""Hello {user.first_name or user.username},

Your OTP (One-Time Password) to reset your password is:

{otp_instance.otp_code}

This code will expire in 10 minutes.

If you didn't request this, please ignore this email.

Best regards,
Restaurant Management Team"""
            
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=html_message,
                fail_silently=False,
            )
            
            # Redirect to OTP verification page
            messages.success(request, 'OTP has been sent to your email!')
            return redirect('verify_otp')
            
        except User.DoesNotExist:
            # Don't reveal if email exists for security
            messages.info(request, 'If an account exists with that email, you will receive an OTP.')
            return redirect('verify_otp')
    
    return render(request, 'forgot_password.html')


def verify_otp(request):
    """Verify OTP and allow password reset"""
    if request.method == 'POST':
        email = request.POST.get('email')
        otp_code = request.POST.get('otp_code')
        
        try:
            user = User.objects.get(email=email)
            otp_instance = PasswordResetOTP.objects.get(user=user, email=email)
            
            # Check if OTP is valid
            if not otp_instance.is_valid():
                messages.error(request, 'OTP has expired or been used. Please request a new one.')
                return redirect('forgot_password')
            
            # Check if OTP matches
            if otp_instance.otp_code != otp_code:
                otp_instance.attempts += 1
                otp_instance.save()
                
                if otp_instance.attempts >= 3:
                    otp_instance.delete()
                    messages.error(request, 'Too many incorrect attempts. Please request a new OTP.')
                    return redirect('forgot_password')
                
                messages.error(request, f'Invalid OTP. {3 - otp_instance.attempts} attempts remaining.')
                return redirect('verify_otp')
            
            # OTP is valid, mark as used and redirect to password reset
            otp_instance.is_used = True
            otp_instance.save()
            
            # Store email in session for password reset view
            request.session['reset_email'] = email
            messages.success(request, 'OTP verified! Please enter your new password.')
            return redirect('reset_password_after_otp')
            
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            messages.error(request, 'Invalid email or OTP. Please try again.')
            return redirect('forgot_password')
    
    return render(request, 'verify_otp.html')


def reset_password_after_otp(request):
    """Reset password after OTP verification"""
    # Check if email is in session (OTP was verified)
    email = request.session.get('reset_email')
    if not email:
        messages.error(request, 'Please verify your OTP first.')
        return redirect('forgot_password')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'reset_password_after_otp.html')
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long!')
            return render(request, 'reset_password_after_otp.html')
        
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            
            # Clean up session
            del request.session['reset_email']
            
            messages.success(request, 'Password has been reset successfully! Please login.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('forgot_password')
    
    return render(request, 'reset_password_after_otp.html')


def reset_password(request, uidb64, token):
    """Handle password reset confirmation (legacy - kept for compatibility)"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            
            if password != password_confirm:
                messages.error(request, 'Passwords do not match!')
                return render(request, 'password_reset_confirm.html')
            
            if len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters long!')
                return render(request, 'password_reset_confirm.html')
            
            user.set_password(password)
            user.save()
            messages.success(request, 'Password has been reset successfully! Please login.')
            return redirect('login')
        
        return render(request, 'password_reset_confirm.html')
    else:
        messages.error(request, 'Invalid or expired password reset link!')
        return redirect('login')

