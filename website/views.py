from flask import Blueprint, redirect, render_template, request, flash
from .models import Client, Product, History, Order

views = Blueprint('views', __name__)

# format and Display orders 
def Order_info(id):

    info_orders = []
    orders =  Order.query.filter(Order.history_id == id).all()
    for order in orders:
        pro = Product.query.get(order.product_id)
        info_orders.append({
            'name': pro.name,
            'quantity': order.quantity,
            'price': order.price,
            'sum_price': float(order.quantity) * float(pro.price)
        })

    return info_orders


@views.route('/', methods=['POST', 'GET'])
def home_bage():
    return render_template('home.html')


#insert product
@views.route('/pro_insert', methods=['POST', 'GET'])
def insert_pro():

    massege = 'hello'
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        quantity = request.form.get('quantity')

    
        new_pro = Product(name = name, price = price, quantity=quantity)
        new_pro.insert()
        massege = 'success'
        print(massege)

        return redirect('/')

        
    return render_template('pro_insert.html', massege = massege)


#insert client
@views.route('/client_insert', methods=['POST', 'GET'])
def client_insert():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')

        new_client = Client(name = name, phone = phone, address = address)
        new_client.insert()


        return redirect('/')

    return render_template('clinet_insert.html')


#search product
@views.route('/pro_search', methods=['POST', 'GET'])
def pro_search():

    products = Product.query.all()
    if request.method == 'POST':
        search = request.form.get('search')
        if search:
            products = Product.query.filter(Product.name.ilike("%{}%".format(search))).all()
    return render_template('pro_search.html', products = products)


#ubdate data of product
@views.route('/update_pro/<int:id>', methods=['POST', 'GET'])
def update_pro(id):
    product = Product.query.get(id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.price = request.form.get('price')
        product.quantity = request.form.get('quantity')
        product.update()

        return redirect('/pro_search')

    return render_template('update_pro.html', product = product)


#search client
@views.route('/client_search', methods=['POST', 'GET'])
def client_search():

    clients = Client.query.all()
    if request.method == 'POST':
        search = request.form.get('search')
        if search:
            clients = Client.query.filter(Client.name.ilike("%{}%".format(search))).all()
    return render_template('client_search.html', clients = clients)

#ubdate data of client
@views.route('/update_client/<int:id>', methods=['POST', 'GET'])
def update_client(id):
    client = Client.query.get(id)
    if request.method == 'POST':
        client.name = request.form.get('name')
        client.phone = request.form.get('phone')
        client.address = request.form.get('address')
        client.update()

        return redirect('/client_search')

    return render_template('update_client.html', client = client)

# pay money (+ or -)
@views.route('/pay/<int:id>', methods=['POST', 'GET'])
def pay_order(id):
    if request.method == 'POST':
        pay = request.form.get('pay')
        if pay:
            pay = float(pay)
            history = History(client_id = id, amount = pay, check_out = True)
            history.insert()
            return redirect(f'/response/{history.id}')

    return render_template('pay.html')

# Order 
@views.route('/order/<int:id>', methods=['POST', 'GET'])
def order(id):

    history = History.query.filter(History.client_id == id).filter(History.check_out == False).first()
    history_id = ''
    print(history)
    orders = []
    if history:
        orders = Order_info(history.id)
    if request.method == 'POST':
        pro_name = request.form.get('pro_name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        if history == None:
            history = History(client_id = id)
            history.insert()
        history_id = history.id
        if pro_name:
            pro_order = Product.query.filter(Product.name.ilike("%{}%".format(pro_name))).first()
            order = Order(
                quantity = quantity, 
                product_id = pro_order.id, 
                history_id = history.id, 
                price = pro_order.price, 
                )
            pro_order.quantity -= int(quantity)
            pro_order.update()
            sum_price = pro_order.price*float(quantity)
            order.insert()
            history.amount += sum_price
            history.update()
            orders = Order_info(history.id)
   

    return render_template('order.html', orders = orders, history_id = history_id)
        
# response for pay or order
@views.route('/response/<int:id>')
def responce(id): 
    history = History.query.get(id)
    client = Client.query.get(history.client_id)
    if history.check_out:
        client.amount -= history.amount
        client.update()
        amount = {
        'history_amount': history.amount,
        'client_amount': client.amount
        }
    else:
        amount = {
            'history_amount': history.amount,
            'client_amount': client.amount + history.amount
        }
    info_orders = []
    orders = Order.query.filter(Order.history_id == id).all()
    if orders != []:
        info_orders = Order_info(id)

    return render_template('response.html', orders = info_orders, amount = amount)


# Display orders in waited
@views.route('/waited_order')
def waited_order():
    histories = History.query.filter(History.check_out == False).all()
    orders = ''
    if histories != []:
        orders = []
        for history in histories:
            client = Client.query.get(history.client_id)
            orders.append({
                'name': client.name,
                'amount': history.amount,
                'total_amount': client.amount + history.amount,
                'history_id': history.id
            })

    return render_template('waited_order.html', orders = orders)


# delete order from waited order if order out
@views.route('/check_out/<int:id>')
def check_out(id):

    history = History.query.get(id)
    client = Client.query.get(history.client_id)
    client.amount += history.amount
    history.check_out = True
    client.update()
    history.update()

    return redirect('/waited_order')

# see detail about order
@views.route('/see_order/<int:id>')
def see_order(id):
    history = History.query.get(id)
    client = Client.query.get(history.client_id)
    info_orders = []
    orders = Order.query.filter(Order.history_id == id).all()
    for order in orders:
        pro = Product.query.get(order.product_id)
        info_orders.append({
            'name': pro.name,
            'quantity': order.quantity,
            'price': order.price,
            'sum_price': float(order.quantity) * float(pro.price)
        })
    info = {
        'name': client.name,
        'Phone': client.phone,
        'address': client.address,
        'amount': history.amount,
        'old_amount': client.amount,
        'total_amount': history.amount + client.amount,
        'date': history.date,
        'check_out': history.check_out
    }
    
    return render_template('see_order.html', orders = info_orders, info = info)

# Display Histories
@views.route('/see_history/<int:id>')
def see_history(id):
    
    histories = History.query.filter(History.client_id == id).order_by(History.id).all()

    return render_template('see_history.html', histories = histories)