from flask import Flask, render_template, request, redirect, session, url_for, flash
import requests
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'
API_BASE = os.getenv('API_BASE_URL') or 'http://localhost:5001/api'

@app.route('/')
def home():
    user = session.get('user')
    if user:
        # Assume user['role'] is set; fallback to not admin
        is_admin = user.get('role', '').lower() == 'admin'
        user['is_admin'] = is_admin
    return render_template('home.html', user=user)

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
            # Redirect based on role
            if session['user'].get('role', '').lower() == 'admin':
                return redirect('/admin-home')
            else:
                return redirect('/')
        else:
            return render_template('login.html', error=res.json().get("message", "Login failed"))
    return render_template('login.html')

@app.route('/admin-home')
def admin_home():
    user = session.get('user')
    if user:
        user['is_admin'] = True
    return render_template('admin_home.html', user=user)

@app.route('/add-address', methods=['GET', 'POST'])
def add_address():
    if not session.get('token'):
        return redirect('/login')

    if request.method == 'POST':
        try:
            payload = {
                "addressLine": request.form['address'],
                "city": request.form['city'],
                "state": request.form['state'],
                "pincode": request.form['zip'],
                "type": request.form['type']
            }
            headers = {'Authorization': f"Bearer {session['token']}"}
            res = requests.post(f"{API_BASE}/addresses", json=payload, headers=headers)

            if res.status_code in [200, 201]:
                return redirect('/')  # Redirect to home page after successful addition
            else:
                return redirect('/login')  # Redirect to login if not successful (e.g., unauthorized)
        except Exception as e:
            return redirect('/login')  # Redirect to login on any error

    return render_template('add_address.html')

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
            from flask import get_flashed_messages
            messages = get_flashed_messages()
            return render_template('restaurants.html', restaurants=data.get('restaurants', []), messages=messages)
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
            return render_template('menu.html', menu_items=data.get('menu', []), restaurant=data.get('restaurant', {}), restaurant_id=id)
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
        menu_item_id = request.form['menuItem']
        restaurant_id = request.form['restaurant']
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

        # Map items to what the template expects
        cart_items = []
        for item in items:
            cart_items.append({
                'menu_item_name': item.get('menuItem', {}).get('name', 'Unknown'),
                'restaurant_name': restaurant.get('name', 'Unknown'),
                'quantity': item.get('quantity', 1),
                'price': item.get('menuItem', {}).get('price', 0),
                'id': item.get('_id', ''),
            })
        total_price = total
        return render_template('cart.html', 
                cart_items=cart_items,
                total_price=total_price, 
                restaurant=restaurant,
                addresses=addresses
                )
    elif cart_res.status_code == 404:
        # ✅ Handle empty cart with user-friendly message
        return render_template('cart.html', cart_items=[], total_price=0, restaurant={})

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
        mapped_orders = []
        for order in orders:
            mapped_orders.append({
                'id': order.get('_id', ''),
                'restaurant_name': order.get('restaurant', {}).get('name', 'Unknown') if isinstance(order.get('restaurant'), dict) else str(order.get('restaurant', '')),
                'status': order.get('status', ''),
                'total_price': order.get('totalAmount', 0),
                'items': [
                    {
                        'name': item.get('menuItem', {}).get('name', 'Unknown') if isinstance(item.get('menuItem'), dict) else str(item.get('menuItem', '')),
                        'quantity': item.get('quantity', 1),
                        'price': item.get('priceAtOrderTime', 0)
                    } for item in order.get('items', [])
                ]
            })
        return render_template('orders.html', orders=mapped_orders)
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

@app.route('/add-restaurant', methods=['GET', 'POST'])
def add_restaurant():
    if not session.get('token'):
        return redirect('/login')
    message = None
    if request.method == 'POST':
        try:
            payload = {
                'name': request.form['name'],
                'cuisineType': request.form['cuisineType'],
                'description': request.form.get('description', ''),
                'address': request.form['address'],
                'location': {
                    'latitude': float(request.form['latitude']),
                    'longitude': float(request.form['longitude'])
                },
                'operatingHours': {
                    'open': request.form.get('open', ''),
                    'close': request.form.get('close', '')
                },
                'minimumOrderAmount': float(request.form.get('minimumOrderAmount', 0)),
                'deliveryFee': float(request.form.get('deliveryFee', 0)),
                'averagePrepTime': float(request.form.get('averagePrepTime', 0)),
                'status': request.form.get('status', 'open'),
                'rating': float(request.form.get('rating', 0)),
            }
            headers = {'Authorization': f"Bearer {session['token']}"}
            res = requests.post(f"{API_BASE}/restaurants", json=payload, headers=headers)
            if res.status_code in [200, 201]:
                flash("✅ Restaurant added successfully!")
                return redirect('/restaurants')
            else:
                message = f"❌ Failed to add restaurant: {res.text}"
        except Exception as e:
            message = f"❌ Error: {str(e)}"
    return render_template('add_restaurant.html', message=message)

@app.route('/add-menu-item', methods=['GET', 'POST'])
def add_menu_item():
    if not session.get('token'):
        return redirect('/login')
    message = None
    headers = {'Authorization': f"Bearer {session['token']}"}
    restaurants = []
    categories = []
    restaurant_id = request.args.get('restaurant_id') or request.form.get('restaurant')
    try:
        res = requests.get(f"{API_BASE}/restaurants")
        if res.status_code == 200:
            restaurants = res.json().get('restaurants', [])
        # Use restaurant_id from query or default to first
        if not restaurant_id and restaurants:
            restaurant_id = restaurants[0]['_id']
        if restaurant_id:
            cat_res = requests.get(f"{API_BASE}/menu/categories?restaurant={restaurant_id}", headers=headers)
            if cat_res.status_code == 200:
                categories = cat_res.json().get('categories', [])
    except Exception as e:
        message = f"❌ Error fetching data: {str(e)}"
    if request.method == 'POST':
        try:
            payload = {
                'restaurant': restaurant_id,
                'category': request.form['category'],
                'name': request.form['name'],
                'isVeg': request.form['isVeg'] == 'true',
                'price': float(request.form['price']),
                'description': request.form.get('description', ''),
                'isAvailable': request.form['isAvailable'] == 'true',
            }
            res = requests.post(f"{API_BASE}/menu/items", json=payload, headers=headers)
            if res.status_code in [200, 201]:
                message = "✅ Menu item added successfully!"
            else:
                message = f"❌ Failed to add menu item: {res.text}"
        except Exception as e:
            message = f"❌ Error: {str(e)}"
    back_to_menu_url = f"/restaurants/{restaurant_id}/menu" if restaurant_id else "/restaurants"
    return render_template('add_menu_item.html', message=message, restaurants=restaurants, categories=categories, restaurant_id=restaurant_id, back_to_menu_url=back_to_menu_url)

@app.route('/add-category', methods=['GET', 'POST'])
def add_category():
    if not session.get('token'):
        return redirect('/login')
    message = None
    restaurant_id = request.args.get('restaurant_id') or request.form.get('restaurant_id')
    if request.method == 'POST':
        try:
            payload = {
                'restaurant': restaurant_id,
                'name': request.form['name'],
                'displayOrder': int(request.form.get('displayOrder', 0)) if request.form.get('displayOrder') else None
            }
            headers = {'Authorization': f"Bearer {session['token']}"}
            res = requests.post(f"{API_BASE}/menu/categories", json=payload, headers=headers)
            if res.status_code in [200, 201]:
                message = "✅ Category added successfully!"
            else:
                message = f"❌ Failed to add category: {res.text}"
        except Exception as e:
            message = f"❌ Error: {str(e)}"
    return render_template('add_category.html', message=message, restaurant_id=restaurant_id)

@app.route('/add-review', methods=['GET', 'POST'])
def add_review():
    if not session.get('token'):
        return redirect('/login')
    message = None
    restaurant_id = request.args.get('restaurant_id') or request.form.get('restaurant_id')
    if request.method == 'POST':
        try:
            payload = {
                'restaurant': restaurant_id,
                'rating': int(request.form['rating']),
                'comment': request.form.get('comment', '')
            }
            headers = {'Authorization': f"Bearer {session['token']}"}
            res = requests.post(f"{API_BASE}/reviews", json=payload, headers=headers)
            if res.status_code in [200, 201]:
                return redirect(f"/restaurants/{restaurant_id}/menu")
            else:
                message = f"❌ Failed to add review: {res.text}"
        except Exception as e:
            message = f"❌ Error: {str(e)}"
    return render_template('add_review.html', message=message, restaurant_id=restaurant_id)

@app.route('/menu/')
def menu_redirect():
    flash('Please select a restaurant to view its menu.')
    return redirect('/restaurants')

@app.route('/cart/update/<item_id>', methods=['POST'])
def update_cart_item(item_id):
    if not session.get('token'):
        return redirect('/login')
    quantity = int(request.form.get('quantity', 1))
    headers = {'Authorization': f"Bearer {session['token']}"}
    # Get current cart
    cart_res = requests.get(f"{API_BASE}/cart", headers=headers)
    if cart_res.status_code != 200:
        flash("❌ Failed to fetch cart.")
        return redirect('/cart')
    cart = cart_res.json().get('cart', {})
    items = cart.get('items', [])
    # Update the quantity for the item
    for item in items:
        if item.get('_id') == item_id:
            item['quantity'] = quantity
    # Prepare payload for backend update (replace all items)
    payload = {
        'items': [
            {
                'menuItem': item['menuItem']['_id'] if isinstance(item['menuItem'], dict) else item['menuItem'],
                'quantity': item['quantity'],
                'specialInstructions': item.get('specialInstructions', '')
            } for item in items
        ]
    }
    res = requests.put(f"{API_BASE}/cart", json=payload, headers=headers)
    restaurant_id = cart.get('restaurant', {}).get('_id', '')
    if res.status_code == 200 and restaurant_id:
        return redirect(f"/restaurants/{restaurant_id}/menu")
    else:
        flash("❌ Failed to update cart item.")
        return redirect('/cart')

@app.route('/cart/remove/<item_id>', methods=['POST'])
def remove_cart_item(item_id):
    if not session.get('token'):
        return redirect('/login')
    headers = {'Authorization': f"Bearer {session['token']}"}
    # Get current cart
    cart_res = requests.get(f"{API_BASE}/cart", headers=headers)
    if cart_res.status_code != 200:
        flash("❌ Failed to fetch cart.")
        return redirect('/cart')
    cart = cart_res.json().get('cart', {})
    items = cart.get('items', [])
    # Remove the item
    new_items = [item for item in items if item.get('_id') != item_id]
    if not new_items:
        # If no items left, clear cart and redirect to restaurants
        requests.delete(f"{API_BASE}/cart", headers=headers)
        return redirect('/restaurants')
    # Prepare payload for backend update (replace all items)
    payload = {
        'items': [
            {
                'menuItem': item['menuItem']['_id'] if isinstance(item['menuItem'], dict) else item['menuItem'],
                'quantity': item['quantity'],
                'specialInstructions': item.get('specialInstructions', '')
            } for item in new_items
        ]
    }
    res = requests.put(f"{API_BASE}/cart", json=payload, headers=headers)
    if res.status_code == 200:
        return redirect('/cart')
    else:
        flash("❌ Failed to remove cart item.")
        return redirect('/cart')

@app.route('/cart/checkout', methods=['POST'])
def cart_checkout():
    if not session.get('token'):
        return redirect('/login')
    address_id = request.form.get('addressId')
    payment_method = request.form.get('paymentMethod', 'CASH').upper()
    if not address_id:
        flash("❌ Please select a delivery address.")
        return redirect('/cart')
    headers = {'Authorization': f"Bearer {session['token']}"}
    payload = {
        'address': address_id,
        'paymentMethod': payment_method,
        'specialInstructions': '',
    }
    res = requests.post(f"{API_BASE}/orders", json=payload, headers=headers)
    if res.status_code == 201:
        flash("✅ Order placed successfully!")
        return redirect('/orders')
    else:
        flash(f"❌ Failed to place order: {res.text}")
        return redirect('/cart')

if __name__ == '__main__':
    app.run(debug=True)
