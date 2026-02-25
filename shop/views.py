from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Medicine, Order, OrderItem
from clinic.models import Department


def shop(request, slug):
    department = get_object_or_404(Department, slug=slug)
    products = Medicine.objects.filter(department=department, is_active=True)
    return render(request, 'shop/shop.html', {
        'department': department,
        'products': products,
    })


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        qty = int(request.POST.get('qty', 1))
        product = get_object_or_404(Medicine, pk=product_id)
        
        cart = request.session.get('cart', {})
        str_id = str(product_id)
        if str_id in cart:
            cart[str_id]['qty'] += qty
        else:
            cart[str_id] = {
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'qty': qty,
                'image': product.image.url if product.image else '',
                'label': product.quantity,
            }
        request.session['cart'] = cart
        total_items = sum(item['qty'] for item in cart.values())
        return JsonResponse({'total_items': total_items})
    return JsonResponse({'total_items': 0})


def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for key, item in cart.items():
        subtotal = float(item['price']) * item['qty']
        cart_items.append({**item, 'subtotal': subtotal, 'key': key})
        total += subtotal
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    str_id = str(item_id)
    if str_id in cart:
        del cart[str_id]
    request.session['cart'] = cart
    messages.success(request, 'Item removed from cart successfully.')
    return redirect('cart')


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')
    
    cart_items = []
    total = 0
    for key, item in cart.items():
        subtotal = float(item['price']) * item['qty']
        cart_items.append({**item, 'subtotal': subtotal})
        total += subtotal
    
    return render(request, 'shop/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })


@login_required
def checkout_submit(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('cart')
        
        total = sum(float(item['price']) * item['qty'] for item in cart.values())
        
        order = Order.objects.create(
            user=request.user,
            total=total,
            payment_method=request.POST.get('pay_method', 'cod'),
            billing_name=f"{request.POST.get('fname', '')} {request.POST.get('lname', '')}",
            billing_email=request.POST.get('bemail', ''),
            billing_phone=request.POST.get('bphone', ''),
            billing_address=request.POST.get('baddress', ''),
            billing_town=request.POST.get('btown', ''),
            billing_zipcode=request.POST.get('bzipcode', ''),
            billing_country=request.POST.get('bcountry', ''),
        )
        
        for key, item in cart.items():
            OrderItem.objects.create(
                order=order,
                medicine_id=item['id'],
                item_name=item['name'],
                item_price=item['price'],
                quantity=item['qty'],
                subtotal=float(item['price']) * item['qty'],
                item_image=item.get('image', ''),
            )
        
        request.session['cart'] = {}
        return redirect('my_orders')
    return redirect('checkout')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/orders.html', {'orders': orders})
