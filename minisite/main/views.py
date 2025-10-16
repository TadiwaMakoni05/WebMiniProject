from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product
from .forms import ProductForm
import random


# 🏠 Home Page (random featured product)
def home(request):
    products = Product.objects.all()[:10]
    header_product = random.choice(products) if products else None

    return render(request, 'home.html', {
        'products': products,
        'header_product': header_product
    })


def products(request):
    product_list = Product.objects.all().order_by('-id')
    query = request.GET.get('q')
    if query:
        product_list = product_list.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    paginator = Paginator(product_list, 8) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj, 
        'query': query,  
    }
    
    return render(request, 'products.html', context)


# 📦 Product Detail Page
def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product-details.html', {'product': product})


# ➕ Add to Cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] += 1
        messages.info(request, f"Added another {product.name} to your cart.")
    else:
        cart[str(product_id)] = 1
        messages.success(request, f"{product.name} added to your cart!")

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')


# 🧾 View Cart Page
def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        total += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total,
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# ❌ Remove item from cart
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)

    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        request.session.modified = True
        messages.error(request, f"{product.name} removed from your cart.")

    return redirect('cart')



# ==================================
# ======= ADMIN CRUD VIEWS =========
# ==================================

# 🔐 Admin: List, Search, and Paginate products
def manage_products(request):
    """
    Handles the admin page for listing products.
    Includes logic for searching by name/description and pagination.
    """
    product_list = Product.objects.all().order_by('-id')
    query = request.GET.get('q')

    # If a search query is provided, filter the queryset
    if query:
        product_list = product_list.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Paginate the (potentially filtered) list of products
    paginator = Paginator(product_list, 5)  # Show 5 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'query': query,
    }
    return render(request, 'admin_products.html', context)


# ➕ Admin: Add a new product (Create)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully! 🎉')
            return redirect('manage_products')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})


# ✏️ Admin: Edit an existing product (Update)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.info(request, f"'{product.name}' updated successfully. ✨")
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form, 'product': product})


# 🗑️ Admin: Delete a product (Delete)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.error(request, f"Product '{product_name}' has been deleted. 🚮")
        return redirect('manage_products')
    return render(request, 'product_confirm_delete.html', {'product': product})