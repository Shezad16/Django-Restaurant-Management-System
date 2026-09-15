from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message_text = request.POST.get('message')
        rating = request.POST.get('rating')
        
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message_text,
            rating=rating if rating else None
        )
        
        messages.success(request, 'Thank you! Your message has been sent. We will get back to you soon!')
        return redirect('contact')
    
    return render(request, 'contact.html')

