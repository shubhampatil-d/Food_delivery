const Cart = require('../models/cart');

exports.addToCart = async (req, res) => {
  const { menuItem, restaurant, quantity, specialInstructions } = req.body;

  try {
    let cart = await Cart.findOne({ user: req.user._id });

    if (cart) {
      // Ensure same restaurant
      if (cart.restaurant.toString() !== restaurant) {
        return res.status(409).json({ message: 'You can only order from one restaurant at a time' });
      }

      const existingItem = cart.items.find(item => item.menuItem.toString() === menuItem);
      if (existingItem) {
        existingItem.quantity += quantity;
      } else {
        cart.items.push({ menuItem, quantity, specialInstructions });
      }

      await cart.save();
    } else {
      // Create new cart
      cart = await Cart.create({
        user: req.user._id,
        restaurant,
        items: [{ menuItem, quantity, specialInstructions }],
      });
    }

    res.status(200).json({ message: 'Item added to cart', cart });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Failed to add item to cart' });
  }
};

exports.getCart = async (req, res) => {
  try {
    let cart = await Cart.findOne({ user: req.user._id })
      .populate('restaurant')
      .populate('items.menuItem');

    if (!cart) {
      return res.status(404).json({ message: 'Cart not found' });
    }
    cart.items = cart.items.filter(item => item.menuItem);
    const totalAmount = cart.items.reduce((sum, item) => {
      return sum + item.menuItem.price * item.quantity;
    }, 0);

    res.json({ cart: { ...cart.toObject(), totalAmount } });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Failed to fetch cart' });
  }
};

exports.clearCart = async (req, res) => {
  try {
    await Cart.findOneAndDelete({ user: req.user._id });
    res.json({ message: 'Cart cleared' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Failed to clear cart' });
  }
};

exports.updateCart = async (req, res) => {
  try {
    const userId = req.user._id;
    const { items } = req.body;
    let cart = await Cart.findOne({ user: userId });
    if (!cart) {
      return res.status(404).json({ message: 'Cart not found' });
    }
    if (!items || !Array.isArray(items)) {
      return res.status(400).json({ message: 'Invalid items array' });
    }
    if (items.length === 0) {
      // If no items left, clear cart
      await Cart.findOneAndDelete({ user: userId });
      return res.json({ message: 'Cart cleared' });
    }
    cart.items = items;
    await cart.save();
    cart = await Cart.findOne({ user: userId })
      .populate('restaurant')
      .populate('items.menuItem');
    // Recalculate totalAmount
    const totalAmount = cart.items.reduce((sum, item) => {
      return sum + (item.menuItem.price * item.quantity);
    }, 0);
    res.json({ cart: { ...cart.toObject(), totalAmount } });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Failed to update cart' });
  }
};
