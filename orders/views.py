from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Order, OrderItem
from menu.models import MenuItem
import json
import razorpay
from django.conf import settings

# Razorpay client initialization
razorpay_client = razorpay.Client(auth=("rzp_test_D7ANXcGhfhhYf1", "2jUjQvr2yNJnjOmhBnHEdRYI"))


@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for item_id, quantity in cart.items():
        try:
            item = MenuItem.objects.get(id=item_id)
            item_total = item.price * quantity
            total_price += item_total
            cart_items.append({
                'item': item,
                'quantity': quantity,
                'total': item_total,
            })
        except MenuItem.DoesNotExist:
            pass
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    
    return render(request, 'cart.html', context)


@login_required
@require_http_methods(["POST"])
def add_to_cart(request, item_id):
    try:
        item = MenuItem.objects.get(id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        
        cart = request.session.get('cart', {})
        
        if str(item_id) in cart:
            cart[str(item_id)] += quantity
        else:
            cart[str(item_id)] = quantity
        
        request.session['cart'] = cart
        messages.success(request, f'{item.name} added to cart!')
        
    except (MenuItem.DoesNotExist, ValueError):
        messages.error(request, 'Error adding item to cart!')
    
    return redirect('view_cart')


@login_required
@require_http_methods(["POST"])
def update_cart(request, item_id):
    try:
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        
        if quantity > 0:
            cart[str(item_id)] = quantity
        else:
            cart.pop(str(item_id), None)
        
        request.session['cart'] = cart
        messages.success(request, 'Cart updated!')
        
    except (ValueError, KeyError):
        messages.error(request, 'Error updating cart!')
    
    return redirect('view_cart')


@login_required
@require_http_methods(["POST"])
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    cart.pop(str(item_id), None)
    request.session['cart'] = cart
    messages.success(request, 'Item removed from cart!')
    
    return redirect('view_cart')


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('view_cart')
    
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            special_instructions=request.POST.get('instructions', '')
        )
        
        total_price = 0
        for item_id, quantity in cart.items():
            try:
                item = MenuItem.objects.get(id=item_id)
                order_item = OrderItem.objects.create(
                    order=order,
                    menu_item=item,
                    quantity=quantity,
                    price=item.price
                )
                total_price += order_item.get_total()
            except MenuItem.DoesNotExist:
                pass
        
        order.total_price = total_price
        order.save()
        
        request.session['cart'] = {}
        messages.success(request, f'Order #{order.id} placed successfully!')
        
        return redirect('order_detail', order_id=order.id)
    
    cart_items = []
    total_price = 0
    
    for item_id, quantity in cart.items():
        try:
            item = MenuItem.objects.get(id=item_id)
            item_total = item.price * quantity
            total_price += item_total
            cart_items.append({
                'item': item,
                'quantity': quantity,
                'total': item_total,
            })
        except MenuItem.DoesNotExist:
            pass
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    
    return render(request, 'checkout.html', context)


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'order_history.html', context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Create Razorpay order
    razorpay_order = razorpay_client.order.create({
        "amount": int(order.total_price * 100),  # Convert to paise
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        "order": order,
        "razorpay_order": razorpay_order,
        "user": request.user
    }
    return render(request, "order_detail.html", context)

