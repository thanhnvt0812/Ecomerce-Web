from .cart import Cart

#Create context processor to make cart available on all pages

def cart(request):
    #return the default data from our cart
    return {'cart': Cart(request)}