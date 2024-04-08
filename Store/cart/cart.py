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


    def add(self, product):
        product_id = str(product_id)