// dbTest.js
const mongoose = require("mongoose");
require("dotenv").config();

const uri = process.env.MONGO_URI;

mongoose
  .connect(uri, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => {
    console.log("✅ MongoDB Connected Successfully!");
    mongoose.connection.close(); // close after test
  })
  .catch((err) => {
    console.error("❌ MongoDB connection error:", err);
  });
