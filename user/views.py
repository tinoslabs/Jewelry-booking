from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, Product, Order, OrderItem
from .forms import CheckoutForm
from django.conf import settings
from django.http import JsonResponse


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    shipping = 70 if subtotal > 0 else 0
    total = subtotal + shipping

    # If it's an AJAX request for updating totals
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'subtotal': subtotal,
            'shipping': shipping,
            'total': total
        })

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    }
    return render(request, 'user/cart.html', context)


@login_required
def update_cart_item(request, item_id):
    # Only accept POST
    if request.method != "POST":
        return JsonResponse({"success": False}, status=400)

    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)

    try:
        quantity = int(request.POST.get("quantity", cart_item.quantity))
    except (ValueError, TypeError):
        return JsonResponse({"success": False}, status=400)

    if quantity < 1:
        quantity = 1

    cart_item.quantity = quantity
    cart_item.save()

    # Recalculate totals for the user
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    subtotal = sum(float(item.product.price) * item.quantity for item in cart_items)
    shipping = 70.0 if subtotal > 0 else 0.0   # your shipping logic
    total = subtotal + shipping

    row_subtotal = float(cart_item.product.price) * cart_item.quantity

    return JsonResponse({
        "success": True,
        "row_subtotal": round(row_subtotal, 2),
        "subtotal": round(subtotal, 2),
        "shipping": round(shipping, 2),
        "total": round(total, 2),
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

# @login_required
# def checkout(request):

#     return render(request, 'user/checkout.html')
from django.db import transaction

@login_required
@transaction.atomic
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart')  # If cart empty, go to cart page

    # Calculate totals
    subtotal = sum(item.subtotal for item in cart_items)
    shipping_charge = 70  # example flat rate shipping
    total_amount = subtotal + shipping_charge

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Save order
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = total_amount
            order.save()

            # Save order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # Clear the cart
            cart_items.delete()

            return redirect('order_success', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'user/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_charge': shipping_charge,
        'total_amount': total_amount
    })


@login_required
def order_success(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return redirect('cart')  # if order doesn't exist, go back to cart

    return render(request, 'user/order_success.html', {
        'order': order,
        'order_items': order.items.all(),  # from related_name="items"
    })


@login_required
def my_orders(request):
    # Get all orders for the logged-in user, latest first
    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related("items__product")  # Optimized query for product info
        .order_by("-created_at")
    )
    return render(request, "user/my_orders.html", {"orders": orders})


# @login_required
# def checkout(request):
#     cart_items = Cart.objects.filter(user=request.user)
#     total_price = sum(item.product.price * item.quantity for item in cart_items)

#     shipping_methods = [
#         {"id": "flatrate", "label": "Flat Rate: $70.00", "cost": 70},
#         {"id": "freeshipping", "label": "Free Shipping", "cost": 0}
#     ]

#     user_billing = request.user.profile.billing_address if hasattr(request.user, 'profile') else None
#     user_shipping = request.user.profile.shipping_address if hasattr(request.user, 'profile') else None

#     payment_methods = [
#         {"id": "cashon", "label": "Cash On Delivery", "value": "cash"},
#         {"id": "directbank", "label": "Direct Bank Transfer", "value": "bank"},
#         {"id": "paypalpayment", "label": "Razorpay", "value": "paypal"}
#     ]

#     return render(request, 'user/checkout.html', {
#         'cart_items': cart_items,
#         'total_price': total_price,
#         'shipping_methods': shipping_methods,
#         'user_billing': user_billing,
#         'user_shipping': user_shipping,
#         'payment_methods': payment_methods
#     })