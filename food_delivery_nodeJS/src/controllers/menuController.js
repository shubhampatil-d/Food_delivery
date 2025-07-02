const MenuCategory = require('../models/menuCategory');
const MenuItem = require('../models/menuItem');

// Add a category to a restaurant
exports.addCategory = async (req, res) => {
  try {
    const { restaurant, name, displayOrder } = req.body;
    const category = await MenuCategory.create({ restaurant, name, displayOrder });
    res.status(201).json({ category });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Failed to create category' });
  }
};

// Add item to a category
exports.addMenuItem = async (req, res) => {
  try {
    const { restaurant, category, name, isVeg, price, description, isAvailable, customizations } = req.body;

    const menuItem = await MenuItem.create({
      restaurant,
      category,
      name,
      isVeg,
      price,
      description,
      isAvailable,
      customizations,
    });

    res.status(201).json({ menuItem });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Failed to add menu item' });
  }
};

// Get menu of a restaurant grouped by category
exports.getMenuByRestaurant = async (req, res) => {
  try {
    const restaurantId = req.params.restaurantId;

    const categories = await MenuCategory.find({ restaurant: restaurantId }).sort('displayOrder');

    const menu = [];

    for (const category of categories) {
      const items = await MenuItem.find({ category: category._id, isAvailable: true });
      menu.push({ category: category.name, items });
    }

    res.json({ menu });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Failed to get menu' });
  }
};
