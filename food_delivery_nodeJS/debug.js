const mongoose = require("mongoose");
const dotenv = require("dotenv");
dotenv.config();

const MenuCategory = require("./src/models/menuCategory");
const MenuItem = require("./src/models/menuItem");

mongoose.connect(process.env.MONGO_URI)
  .then(async () => {
    console.log("Connected to MongoDB ✅");

    const categories = await MenuCategory.find();
    console.log("\n📦 Menu Categories:");
    console.log(categories);

    const items = await MenuItem.find();
    console.log("\n🍔 Menu Items:");
    console.log(items);

    mongoose.connection.close();
  })
  .catch((err) => {
    console.error("MongoDB connection error ❌", err);
  });
