from datetime import time

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking


BOOKING_START = time(hour=11, minute=0)
BOOKING_END = time(hour=23, minute=0)


@login_required
def booking(request):
    if request.method == 'POST':
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        number_of_people = request.POST.get('number_of_people')
        special_requests = request.POST.get('special_requests', '')

        try:
            booking_time_obj = time.fromisoformat(booking_time)
        except (TypeError, ValueError):
            messages.error(request, 'Please select a valid booking time between 11:00 and 23:00.')
            return redirect('booking')

        if not (BOOKING_START <= booking_time_obj <= BOOKING_END):
            messages.error(request, 'Booking time must be between 11:00 AM and 11:00 PM.')
            return redirect('booking')
        
        booking_obj = Booking.objects.create(
            user=request.user,
            booking_date=booking_date,
            booking_time=booking_time,
            number_of_people=number_of_people,
            special_requests=special_requests
        )
        
        messages.success(request, 'Table booked successfully!')
        return redirect('booking_confirmation', booking_id=booking_obj.id)
    
    return render(request, 'booking.html')


@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    context = {'booking': booking}
    return render(request, 'booking_confirmation.html', context)


@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user)
    context = {'bookings': bookings}
    return render(request, 'booking_history.html', context)


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully!')
        return redirect('booking_history')
    
    context = {'booking': booking}
    return render(request, 'cancel_booking.html', context)

