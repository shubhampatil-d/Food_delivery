const express = require("express");
const helmet = require("helmet");
const morgan = require("morgan");
const dotenv = require("dotenv");
const cors = require("cors");
const connectDB = require("./config/database");
const authRoutes = require("./routes/authRoutes");
const addressRoutes = require("./routes/addressRoutes")
const restaurantRoutes= require('./routes/restaurantRoutes')
const cartRoutes = require('./routes/cartRoutes');
const menuRoutes = require('./routes/menuRoutes');
const orderRoutes = require('./routes/orderRoutes');
const paymentRoutes = require('./routes/paymentRoutes');
const trackingRoutes = require('./routes/orderTrackingRoutes');
const reviewRoutes = require('./routes/reviewRoutes');
const deliveryPartnerRoutes = require('./routes/deliveryPartnerRoutes');

dotenv.config();
// ✅ Connect to MongoDB (Only Once)
connectDB();
const app = express();



// ✅ Middleware
app.use(express.json());
app.use(morgan("dev"));
app.use(cors());
app.use(helmet());

// ✅ Routes
app.use("/api/auth", authRoutes);
app.use('/api/addresses', addressRoutes);
app.use('/api/restaurants',restaurantRoutes)
app.use('/api/cart', cartRoutes);
app.use('/api/menu', menuRoutes);
app.use('/api/orders', orderRoutes);
app.use('/api/payments', paymentRoutes);
app.use('/api/tracking', trackingRoutes);
app.use('/api/reviews', reviewRoutes);
app.use('/api/delivery-partners', deliveryPartnerRoutes);

app.get("/", (req, res) => res.send("App is running"))

// ✅ Global Error Handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status || 500).json({ error: err.message || "server error" });
});


// ✅ Start Server
const PORT = process.env.PORT || 5001;
app.listen(PORT, () => {
  console.log(`Server started on port ${PORT}`);
});



