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
    if request.method == "POST":
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        payment_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('my_shipping')

        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            order_id= create_order.pk
            for product in cart_products():
               product_id= product.id
               if product.is_sale:
                  price=product.sale_price
               else:
                  price=product.price
               
               for key,value in quantities().items():
                  if int(key) == product.id:
                     create_order_item= OrderItem(order= order_id, product= product_id, user= user, quantity= value, price=price)
                     create_order_item.save()

        else:
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            order_id= create_order.pk
            for product in cart_products():
               product_id= product.id
               if product.is_sale:
                  price=product.sale_price
               else:
                  price=product.price
               
               for key,value in quantities().items():
                  if int(key) == product.id:
                     create_order_item= OrderItem(order= order_id, product= product_id, quantity= value, price=price)
                     create_order_item.save()
        
        messages.success(request, "Order placed successfully ✅")
        return redirect("payment_success")

    else:
        messages.error(request, "Access Denied")
        return redirect('home')




  