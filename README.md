# 🍔 BiteBlitz

A modern, full-stack Food Delivery platform with a Node.js/Express/MongoDB backend and a Flask frontend. This project allows users to browse restaurants, order food, manage carts, and track orders in real time. Admins can manage restaurants, menus, and orders. Built for learning, prototyping, and real-world deployment.

---

## 🚀 Features

- User registration, login, and authentication
- Browse restaurants and menus
- Add items to cart and place orders
- Address management
- Order tracking
- Admin dashboard for restaurant/menu management
- Secure JWT-based authentication
- Responsive, user-friendly UI

---

## 🛠️ Tech Stack

**Backend:**

- MongoDB (Mongoose)
- JWT Authentication
- RESTful API

**Frontend:**
- Python
- Flask
- Jinja2 Templates
- HTML5, CSS3, Bootstrap
- Requests, dotenv

---

## 📁 Project Structure

```
BiteBlitz/
├── food_delivery_nodeJS/         # Backend (Node.js/Express)
│   ├── src/
│   │   ├── controllers/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── utils/
│   │   └── app.js
│   ├── database/
│   ├── package.json
│   └── ...
├── food-delivery-frontend/       # Frontend (Flask)
│   ├── app.py
│   ├── requirements.txt
│   ├── templates/
│   ├── static/
│   └── ...
└── README.md
```

---

## 🖥️ Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/BiteBlitz.git
cd BiteBlitz
```

### 2. Backend Setup (Node.js/Express)

```bash
cd food_delivery_nodeJS
npm install
```

#### Create a `.env` file in `food_delivery_nodeJS/`:

```
MONGO_URI=your_mongodb_connection_string
PORT=5001
JWT_SECRET=your_jwt_secret
```

#### Start the backend server:

```bash
npm run dev   # For development (nodemon)
# or
npm start     # For production
```

The backend will run on `http://localhost:5001` by default.

---

### 3. Frontend Setup (Flask)

```bash
cd ../food-delivery-frontend
python -m venv venv
# Activate the virtual environment:
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

#### Create a `.env` file in `food-delivery-frontend/`:

```
API_BASE_URL=http://localhost:5001/api
SECRET_KEY=your_flask_secret_key
```

#### Start the frontend server:

```bash
# Make sure your virtual environment is activated
python app.py
```

The frontend will run on `http://localhost:5000` by default.

---

## 🧪 Testing the App

1. Register a new user and log in.
2. Browse restaurants, add items to your cart, and place an order.
3. Use the admin dashboard to manage restaurants and menus (login as admin).
4. Track your orders in real time.

---

## 📦 Tools & Technologies

- **Node.js** / **Express.js** / **MongoDB** / **Mongoose**
- **Python** / **Flask** / **Jinja2**
- **JWT** for authentication
- **Bootstrap** for UI
- **dotenv** for environment management
- **Nodemon** for backend development

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

[MIT](LICENSE)

---

## ✨ Acknowledgements

- Inspired by popular food delivery platforms
- Built with ❤️ by [Shubham Patil]

---

> _Happy Coding & Bon Appétit!_ 🍕🍟🍣 
