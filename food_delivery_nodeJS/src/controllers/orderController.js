const Cart = require('../models/cart');
const MenuItem = require('../models/menuItem');
const Order = require('../models/order');

exports.placeOrder = async (req, res) => {
  try {
    const { address, paymentMethod, specialInstructions } = req.body;

    const cart = await Cart.findOne({ user: req.user._id })
      .populate('restaurant')
      .populate('items.menuItem');

    if (!cart || !cart.items || cart.items.length === 0) {
      return res.status(400).json({ message: 'Cart is empty or items missing' });
    }

    // ✅ Validate items and skip invalid ones
    const orderItems = [];

    for (const item of cart.items) {
      if (!item.menuItem || !item.menuItem._id || !item.menuItem.price) {
        console.warn('❌ Invalid item in cart:', item);
        continue; // skip invalid menuItem
      }

      orderItems.push({
        menuItem: item.menuItem._id,
        quantity: item.quantity,
        priceAtOrderTime: item.menuItem.price,
        customizations: item.customizations || [],
      });
    }

    // ✅ If no valid items remain
    if (orderItems.length === 0) {
      return res.status(400).json({ message: 'Cart has no valid items to place order' });
    }

    const totalAmount = orderItems.reduce(
      (sum, item) => sum + item.priceAtOrderTime * item.quantity,
      0
    ) + (cart.restaurant.deliveryFee || 0);

    const order = await Order.create({
      user: req.user._id,
      restaurant: cart.restaurant._id,
      address,
      status: 'placed',
      items: orderItems,
      totalAmount,
      deliveryFee: cart.restaurant.deliveryFee,
      paymentMethod,
      specialInstructions,
      estimatedDeliveryTime: '30-45 mins',
    });

    await Cart.deleteOne({ user: req.user._id });

    res.status(201).json({ message: 'Order placed successfully', order });

  } catch (err) {
    console.error('❌ Order Error:', err.message);
    res.status(500).json({ message: err.message || 'Failed to place order' });
  }
};


exports.getMyOrders = async (req, res) => {
  try {
    const orders = await Order.find({ user: req.user._id }).sort({ createdAt: -1 });
    res.json({ orders });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Failed to fetch orders' });
  }
};

exports.updateOrderStatus = async (req, res) => {
  try {
    const { status } = req.body;
    const { id } = req.params;

    const validStatuses = ['confirmed', 'preparing', 'out-for-delivery', 'delivered', 'cancelled'];
    if (!validStatuses.includes(status)) {
      return res.status(400).json({ message: 'Invalid status' });
    }

    const order = await Order.findByIdAndUpdate(id, { status }, { new: true });
    res.json({ message: 'Order status updated', order });

  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Failed to update order status' });
  }
};
