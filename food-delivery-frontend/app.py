from flask import Flask, render_template, request, redirect, session, url_for
import requests
import os
from dotenv import load_dotenv
from flask import flash


load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'
API_BASE = os.getenv('API_BASE_URL') or 'http://localhost:5001/api'

@app.route('/')
def home():
    return render_template('home.html', user=session.get('user'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {
            "name": request.form['name'],
            "phone": request.form['phone'],
            "email": request.form['email'],
            "password": request.form['password'],
        }
        res = requests.post(f"{API_BASE}/auth/register", json=data)
        if res.status_code == 201:
            return redirect('/login')
        else:
            return res.text, res.status_code
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = {
            "email": request.form['email'],
            "password": request.form['password']
        }
        res = requests.post(f"{API_BASE}/auth/login", json=data)
        print("Status Code:", res.status_code)
        print("Response JSON:", res.json())
        if res.status_code == 200:
            json_data = res.json()
            session['token'] = json_data.get('accessToken') or json_data.get('token')
            session['user'] = json_data.get('user', {})
            return redirect('/')
        else:
            return render_template('login.html', error=res.json().get("message", "Login failed"))
    return render_template('login.html')

@app.route('/add-address', methods=['GET', 'POST'])
def add_address():
    if not session.get('token'):
        return redirect('/login')

    message = None

    if request.method == 'POST':
        try:
            payload = {
                "addressLine": request.form['address'],
                "latitude": float(request.form['latitude']),
                "longitude": float(request.form['longitude']),
                "type": request.form['type']
            }
            headers = {'Authorization': f"Bearer {session['token']}"}
            res = requests.post(f"{API_BASE}/addresses", json=payload, headers=headers)

            if res.status_code in [200, 201]:  # Support both 200 & 201
                message = "✅ Address added successfully!"
            else:
                message = f"❌ Failed to add address: {res.text}"
        except Exception as e:
            message = f"❌ Error: {str(e)}"

    return render_template('add_address.html', message=message)

@app.route('/addresses')
def view_addresses():
    if not session.get('token'):
        return redirect('/login')

    headers = {'Authorization': f"Bearer {session['token']}"}
    res = requests.get(f"{API_BASE}/addresses", headers=headers)

    if res.status_code == 200:
        addresses = res.json().get('addresses', [])
    else:
        addresses = []
    
    return render_template('view_addresses.html', addresses=addresses)


@app.route('/addresses/<id>/set-default', methods=['POST'])
def set_default_address(id):
    if not session.get('token'):
        return redirect('/login')

    headers = {'Authorization': f"Bearer {session['token']}"}
    res = requests.put(f"{API_BASE}/addresses/{id}/set-default", headers=headers)

    if res.status_code == 200:
        flash("✅ Default address updated.")
    else:
        flash("❌ Failed to update default address.")

    return redirect('/addresses')

@app.route('/restaurants')
def restaurants():
    try:
        res = requests.get(f"{API_BASE}/restaurants")
        if res.status_code == 200:
            data = res.json()
            return render_template('restaurants.html', restaurants=data.get('restaurants', []))
        else:
            return "Error fetching restaurants", 500
    except Exception as e:
        return str(e), 500
    
@app.route('/restaurants/<id>/menu')
def restaurant_menu(id):
    try:    
        res = requests.get(f"{API_BASE}/restaurants/{id}/menu")
        if res.status_code == 200:
            data = res.json()
            return render_template('menu.html', menu=data.get('menu', []), restaurant_id=id)
        else:
            flash("Menu not found")
            return redirect('/restaurants')
    except Exception as e:
        flash(f"❌ Error fetching menu: {str(e)}")
        return redirect('/restaurants')
    

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    if not session.get('token'):
        return redirect('/login')

    try:
        menu_item_id = request.form['menuItemId']
        restaurant_id = request.form['restaurantId']
        quantity = int(request.form['quantity'])
        special = request.form.get('specialInstructions', '')

        payload = {
            "menuItem": menu_item_id,
            "restaurant": restaurant_id,
            "quantity": quantity,
            "specialInstructions": special
        }
        print("DEBUG payload:", payload)
        headers = {'Authorization': f"Bearer {session['token']}"}
        res = requests.post(f"{API_BASE}/cart", json=payload, headers=headers)

        # ✅ Fix here:
        if res.status_code == 200 or res.status_code == 201:
            flash("✅ Item added to cart!")
        elif res.status_code == 409:
            flash("⚠️ You can only order from one restaurant at a time. Please clear your cart to continue.")
        else:
            flash(f"❌ Failed to add item: {res.text}")

    except Exception as e:
        flash(f"❌ Error adding item: {str(e)}")

    return redirect(request.referrer or '/restaurants')

@app.route('/cart', methods=['GET'])
def view_cart():
    if not session.get('token'):
        return redirect('/login')

    headers = {'Authorization': f"Bearer {session['token']}"}
    
    cart_res = requests.get(f"{API_BASE}/cart", headers=headers)
    addr_res = requests.get(f"{API_BASE}/addresses", headers=headers)

    if cart_res.status_code == 200 and addr_res.status_code == 200:
        cart_data = cart_res.json().get('cart', {})
        print("📦 CART DATA:", cart_data)

        items = cart_data.get('items', [])
        total = cart_data.get('totalAmount', 0)
        restaurant = cart_data.get('restaurant', {})
        addresses = addr_res.json().get('addresses', [])

        return render_template('cart.html', 
                items=items,
                total=total, 
                restaurant=restaurant,
                addresses=addresses
                )
    elif cart_res.status_code == 404:
        # ✅ Handle empty cart with user-friendly message
        # flash("🛒 Your cart is empty.")
        return render_template('cart.html', cart={}, items=[], total=0, restaurant={})

    else:
        print("DEBUG: Cart or Address API failed")
        flash("❌ Failed to fetch cart or address.")
        return redirect('/restaurants')




@app.route('/cart/clear', methods=['POST'])
def clear_cart():
    if not session.get('token'):
        return redirect('/login')
    headers = {'Authorization': f"Bearer {session['token']}"}
    res = requests.delete(f"{API_BASE}/cart", headers=headers)

    if res.status_code == 200:
        flash("🗑️ Cart cleared successfully.")
    else:
        try:
            flash(f"❌ Failed to clear cart: {res.json().get('message')}")
        except:
            flash("❌ Failed to clear cart.")

    return redirect('/cart')

@app.route('/order/place', methods=['POST'])
def place_order():
    if not session.get('token'):
        return redirect('/login')

    headers = {'Authorization': f"Bearer {session['token']}"}
    payload = {
        "address": request.form['addressId'],
        "paymentMethod": request.form['paymentMethod'].upper(),
        "specialInstructions": "",
    }

    # Send the request to backend
    res = requests.post(f"{API_BASE}/orders", json=payload, headers=headers)

    if res.status_code == 201:
        flash("✅ Order placed successfully!")
    else:
        flash(f"❌ Failed to place order: {res.text}")

    return redirect('/cart')  # ✅ Always return something

@app.route('/orders', methods=['GET'])
def view_orders():
    if not session.get('token'):
        return redirect('/login')

    headers = {'Authorization': f"Bearer {session['token']}"}
    res = requests.get(f"{API_BASE}/orders", headers=headers)

    if res.status_code == 200:
        orders = res.json().get('orders', [])
        return render_template('orders.html', orders=orders)
    else:
        flash("❌ Failed to fetch order history.")
        return redirect('/')

@app.route('/orders/<order_id>/track', methods=['GET'])
def track_order(order_id):
    if not session.get('token'):
        return redirect('/login')

    headers = {'Authorization': f"Bearer {session['token']}"}
    res = requests.get(f"{API_BASE}/orders/{order_id}/tracking", headers=headers)

    if res.status_code == 200:
        tracking = res.json().get('tracking', [])
        return render_template('order_tracking.html', tracking=tracking, order_id=order_id)
    else:
        flash("❌ Failed to fetch order tracking.")
        return redirect('/orders')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
