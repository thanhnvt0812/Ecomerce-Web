from django.shortcuts import redirect, render
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product, Profile
import datetime
import uuid # unique user id for duplictate orders


# Create your views here.
def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    if request.user.is_authenticated:
        #checkout as login user
        shipping_user, _ = ShippingAddress.objects.get_or_create(user=request.user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)	

        return render(request, 'payment/checkout.html',{"cart_products": cart_products , "quantities": quantities, "totals": totals, "shipping_form": shipping_form})
    else:
        #checkout as guest
        shipping_form = ShippingForm(request.POST or None)	
        return render(request, 'payment/checkout.html',{"cart_products": cart_products , "quantities": quantities, "totals": totals, "shipping_form": shipping_form})
def payment_success(request):
    return render(request,'payment/payment_success.html',{})

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        #create session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        #check if user login
        if request.user.is_authenticated:
            #get the billing form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html',{"cart_products": cart_products , "quantities": quantities, "totals": totals, "shipping_info": request.POST, 'billing_form':billing_form})
        else:
            #not login
            #get the billing form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html',{"cart_products": cart_products , "quantities": quantities, "totals": totals, "shipping_info": request.POST, 'billing_form':billing_form})
            
        
    else:
        messages.success(request,'Access Denied')
        return redirect('home')

def process_order(request):
    if not request.POST:
        messages.success(request, "Access Denied")
        return redirect('home')
    
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    
    # Get Shipping Session Data
    my_shipping = request.session.get('my_shipping', {})
    full_name = my_shipping.get('shipping_full_name', '')
    email = my_shipping.get('shipping_email', '')
    shipping_address = "\n".join(filter(None, [
        my_shipping.get('shipping_address1', ''),
        my_shipping.get('shipping_address2', ''),
        my_shipping.get('shipping_city', ''),
        my_shipping.get('shipping_state', ''),
        my_shipping.get('shipping_zipcode', ''),
        my_shipping.get('shipping_country', '')
    ]))
    
    # Create an Order
    user = request.user if request.user.is_authenticated else None
    create_order = Order(
        user=user,
        full_name=full_name,
        email=email,
        shipping_address=shipping_address,
        amount_paid=totals
    )
    create_order.save()
    order_id = create_order.pk
    
    # Add order items
    for product in cart_products:
        price = product.sale_price if product.is_sale else product.price
        quantity = quantities.get(str(product.id), 0)
        if quantity:
            OrderItem.objects.create(
                order_id=order_id,
                product_id=product.id,
                user=user,
                quantity=quantity,
                price=price
            )
    
    # Clear cart session
    request.session.pop("session_key", None)
    
    # Clear old cart in database if user is authenticated
    if user:
        Profile.objects.filter(user__id=user.id).update(old_cart="")
    
    messages.success(request, "Order Placed!")
    return redirect('home')

def not_shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=False)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# Get the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=True, date_shipped=now)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')

		return render(request, "payment/not_shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')

def shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=True)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# grab the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=False)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')


		return render(request, "payment/shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')
     
def orders(request, pk):
	if request.user.is_authenticated and request.user.is_superuser:
		# Get the order
		order = Order.objects.get(id=pk)
		# Get the order items
		items = OrderItem.objects.filter(order=pk)

		if request.POST:
			status = request.POST['shipping_status']
			# Check if true or false
			if status == "true":
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				now = datetime.datetime.now()
				order.update(shipped=True, date_shipped=now)
			else:
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				order.update(shipped=False)
			messages.success(request, "Shipping Status Updated")
			return redirect('home')


		return render(request, 'payment/orders.html', {"order":order, "items":items})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')
