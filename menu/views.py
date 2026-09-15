from django.shortcuts import render
from .models import Category, MenuItem
from django.db.models import Q


def menu(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    search_query = request.GET.get('search')
    
    items = MenuItem.objects.filter(is_available=True)
    
    # Ensure search_query is valid
    search_query = search_query if search_query and search_query.lower() != 'none' else None
    
    # Ensure selected_category is valid and exists in the database
    if selected_category and selected_category.isdigit():
        if categories.filter(id=int(selected_category)).exists():
            items = items.filter(category_id=int(selected_category))
        else:
            selected_category = None  # Reset if invalid category is selected
    
    # Filter by search query
    if search_query:
        items = items.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    context = {
        'categories': categories,
        'items': items,
        'selected_category': selected_category,
        'search_query': search_query,
    }
    
    return render(request, 'menu.html', context)


def menu_detail(request, pk):
    item = MenuItem.objects.get(pk=pk)
    related_items = MenuItem.objects.filter(
        category=item.category,
        is_available=True
    ).exclude(pk=pk)[:4]
    
    context = {
        'item': item,
        'related_items': related_items,
    }
    
    return render(request, 'menu_detail.html', context)


def home(request):
    featured_items = MenuItem.objects.filter(is_available=True)[:6]
    categories = Category.objects.all()
    
    context = {
        'featured_items': featured_items,
        'categories': categories,
    }
    
    return render(request, 'home.html', context)

