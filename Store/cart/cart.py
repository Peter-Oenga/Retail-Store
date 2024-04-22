from core.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session

        #Get the current session key if it exists
        cart = self.session.get('session_key')


        #If the user is new and therefore no session key create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #Make sure that the cart is available to all the processes
        self.cart = cart


    def add(self, product, quantity):
        product_id = str(product.id)

        product_quantity = str(quantity)

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {"Product price: ": str(product.price)}
            self.cart[product_id] = int(product_quantity)

        self.session.modified = True


    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        #Get the IDs from the cart
        product_ids = self.cart.keys()

        # Lookup the products in the database
        products = Product.objects.filter(id__in=product_ids)

        return products

    def get_quantities(self):
        quantities =self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_quantity = int(quantity)
        
        # Get the cart
        ourcart = self.cart

        # Update Cart
        ourcart[product_id] = product_quantity

        