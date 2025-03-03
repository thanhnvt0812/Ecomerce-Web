from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    return render(request, 'cart_summary.html',{"cart_products": cart_products , "quantities": quantities, "totals": totals})

def cart_add(request):
    #get the cart
    cart = Cart(request)
    #test for POST request
    if request.POST.get('action') == 'post':
        #get the product_id from the form
        product_id = int(request.POST.get('product_id'))
        #get the product quantity from the form
        product_qty = int(request.POST.get('product_qty'))
        #get the product object in DB
        product = get_object_or_404(Product, id=product_id)
        #save to the session and add to cart
        cart.add(product=product, qty=product_qty)
        #get the cart quantity
        cart_quantity = cart.__len__()
        #get the cart total
        cart_total = cart.cart_total()
        #return the response
        response = JsonResponse({'Product Name: ': product.name,'qty': cart_quantity, 'total': cart_total})
        messages.success(request, (f'Successful add {str(product_qty)} {str(product)} into your cart'))
        return response
    else:
        return render(request, 'cart_add.html',{})

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #get product
        product_id = int(request.POST.get('product_id'))
        #delete function
        cart.delete(product = product_id)
        response = JsonResponse({'product': product_id})
        #redirect cart_summary
        messages.success(request, ("Item Deleted From Shopping Cart..."))
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'product_id': product_id, 'qty': product_qty})
        messages.success(request, ("Your cart has been updated"))
        return response
    else:
        return render(request, 'cart_update.html',{})
    
