from store.models import Product, Profile
class Cart():
    def __init__(self, request):
        self.session = request.session
        #get request
        self.request = request
        #get current session key if it exists
        cart = self.session.get('session_key')

        #if user is new, create a new session key
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #make sure cart is always available on all pages of the site
        self.cart = cart


    def add(self, product, qty):
        product_id = str(product.id)
        product_qty = str(qty)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True
        #deal with login user
        if self.request.user.is_authenticated:
            #get current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #convert data from JSON like {'3':1, '4':2} to {"3":1, "4":2} to save to db
            carty = str(self.cart) #{'3':1, '4':2} => "{'3':1, '4':2}"
            carty = carty.replace("\'","\"")
            #save carty to db
            current_user.update(old_cart=str(carty))

    #function add from store/views.py
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
		# Logic
        if product_id in self.cart:
            pass
        else:
			#self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

		# Deal with logged in user
        if self.request.user.is_authenticated:
			# Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
			# Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
            current_user.update(old_cart=str(carty))


    def cart_total(self):
		# Get product IDS
        product_ids = self.cart.keys()
		# lookup those keys in our products database model
        products = Product.objects.filter(id__in=product_ids)
		# Get quantities
        quantities = self.cart
		# Start counting at 0
        total = 0
		
        for key, value in quantities.items():
			# Convert key string into into so we can do math
            key = int(key)
            # Extract the quantity from the dictionary and convert to int
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)

            # print(key)
            # print(value)
            # print(total)
        return total
       



    def __len__(self):
            return len(self.cart)
    
    def get_prods(self):
		# Get ids from cart
        product_ids = self.cart.keys()
		# Use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)
		# Return those looked up products
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

		# Get cart
        ourcart = self.cart
		# Update Dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True
	

		# Deal with logged in user
        if self.request.user.is_authenticated:
			# Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
			# Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
            current_user.update(old_cart=str(carty))


        thing = self.cart
        return thing
    
    def delete(self, product):
        product_id = str(product)
		# Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

		# Deal with logged in user
        if self.request.user.is_authenticated:
			# Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
			# Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
            current_user.update(old_cart=str(carty))