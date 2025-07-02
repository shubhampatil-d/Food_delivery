const OrderTracking = require('../models/orderTracking');
const Order = require('../models/order');

exports.addTrackingUpdate = async (req, res) => {
  try {
    const { orderId, status } = req.body;
    const order = await Order.findById(orderId);
    if (!order) return res.status(404).json({ message: 'Order not found' });
    
    const tracking = await OrderTracking.create({ order: orderId, status });
    
    order.status = status;
    await order.save();

    res.status(201).json({ message: 'Tracking updated', tracking });
  } catch (err) {
    console.error(err)
    res.status(500).json({ message: 'Failed to update tracking' });
  }
};

exports.getOrderTracking = async (req, res) => {
  try {
    const orderId = req.params.orderId;
    const updates = await OrderTracking.find({ order: orderId }).sort('timestamp:1');
    res.json({ tracking: updates });
  } catch (err) {
    res.status(500).json({ message: 'Failed to fetch tracking' });
  }
};
