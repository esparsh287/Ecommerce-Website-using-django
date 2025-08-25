from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PaymentForm, ShippingForm
from .models import Order, OrderItem
from django.contrib.auth.models import User
from store.models import Product

from cart.cart import Cart
from .forms import ShippingForm
from .models import ShippingAddress

def payment_success(request):
  return render(request, 'payment/payment_success.html',{})

def checkout(request):
  cart= Cart(request)
  cart_products=cart.get_prods()
  quantities= cart.get_quants()
  totals=cart.cart_total()
  if request.user.is_authenticated:
    shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)
    shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    return render(request, 'payment/checkout.html',{'cart_products': cart_products, "quantities": quantities, "totals":totals, 'shipping_form':shipping_form})
  else:
    shipping_form = ShippingForm(request.POST or None)
    return render(request, 'payment/checkout.html',{'cart_products': cart_products, "quantities": quantities, "totals":totals, 'shipping_form':shipping_form})
  


def billing_info(request):
  if request.POST:
    cart= Cart(request)
    cart_products=cart.get_prods()
    quantities= cart.get_quants()
    totals=cart.cart_total()

    #Create a seesion:
    my_shipping=request.POST.dict()
    request.session['my_shipping']= my_shipping
    if request.user.is_authenticated:
      billing_form= PaymentForm()
      return render(request, 'payment/billing_info.html',{'cart_products': cart_products, "quantities": quantities, "totals":totals, 'shipping_info':request.POST, "billing_form":billing_form})
    else:
      return render(request, 'payment/billing_info.html',{'cart_products': cart_products, "quantities": quantities, "totals":totals, 'shipping_info':request.POST, "billing_form":billing_form})
    
  else:
    messages.error(request, "Access Denied")
    return redirect('home')
  


def process_order(request):
    if request.method != "POST":
        messages.error(request, "Access Denied")
        return redirect("home")

    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    my_shipping = request.session.get('my_shipping')
    if not my_shipping:
        messages.error(request, "Shipping information missing")
        return redirect("checkout")

    # Prepare order data
    full_name = my_shipping.get('shipping_full_name')
    email = my_shipping.get('shipping_email')
    shipping_address = (
        f"{my_shipping.get('shipping_address1')}\n"
        f"{my_shipping.get('shipping_address2')}\n"
        f"{my_shipping.get('shipping_city')}\n"
        f"{my_shipping.get('shipping_state')}\n"
        f"{my_shipping.get('shipping_zipcode')}\n"
        f"{my_shipping.get('shipping_country')}"
    )
    amount_paid = totals

    # Create order
    if request.user.is_authenticated:
        user = request.user
        order = Order.objects.create(
            user=user,
            full_name=full_name,
            email=email,
            shipping_address=shipping_address,
            amount_paid=amount_paid
        )
    else:
        order = Order.objects.create(
            full_name=full_name,
            email=email,
            shipping_address=shipping_address,
            amount_paid=amount_paid
        )
        user = None  # For anonymous users

    # Create order items
    for product in cart_products:
        price = product.sale_price if getattr(product, "is_sale", False) else product.price
        quantity = quantities.get(str(product.id), 1)  # Default 1 if not found
        OrderItem.objects.create(
            order=order,
            product=product,
            user=user,
            quantity=quantity,
            price=price
        )

    # Clear cart session
    for key in list(request.session.keys()):
        if key.startswith("session_key") or key == "my_shipping":
            del request.session[key]

    messages.success(request, "Order placed successfully ✅")
    return redirect("home")
    


def not_shipped_dash(request):
   if request.user.is_authenticated and request.user.is_superuser:
      orders= Order.objects.filter(shipped=False)
      return render(request, "payment/not_shipped_dash.html", {'orders':orders})
   else:
      messages.success(request, "Access Denied")
      return redirect('home')
      
   

def shipped_dash(request):
   if request.user.is_authenticated and request.user.is_superuser:
      orders= Order.objects.filter(shipped=True)
      return render(request, "payment/shipped_dash.html", {'orders':orders})
   else:
      messages.success(request, "Access Denied")
      return redirect('home')
   

def orders(request, pk):
   if request.user.is_authenticated and request.user.is_superuser:
      order= Order.objects.get(id=pk)
      items= OrderItem.objects.filter(order= pk)
      return render(request, 'payment/orders.html', {'order':order, 'items':items})
   else:
      messages.success(request, "Access Denied")
      return redirect('home')
      
   




  