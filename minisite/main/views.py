from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Product
import random


# 🏠 Home Page (random featured product)
def home(request):
    products = Product.objects.all()[:10]
    header_product = random.choice(products) if products else None

    return render(request, 'home.html', {
        'products': products,
        'header_product': header_product
    })


# 🛍 Product List Page with Pagination
def products(request):
    product_list = Product.objects.all().order_by('id')  # Show all products ordered by ID
    paginator = Paginator(product_list, 8)  # 8 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products.html', {'products': page_obj})


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
