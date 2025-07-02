const Payment = require('../models/payment');
const Order = require('../models/order');

exports.recordPayment = async (req, res) => {
  try {
    const { orderId, method, transactionId, status } = req.body;
    const order = await Order.findById(orderId);
    if (!order) return res.status(404).json({ message: 'Order not found' });

    const payment = await Payment.create({
      order: order._id,
      user: req.user._id,
      method,
      status,
      transactionId,
      amount: order.totalAmount,
    });

    res.status(201).json({ message: 'Payment recorded', payment });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Failed to record payment' });
  }
};

exports.getMyPayments = async (req, res) => {
  try {
    const payments = await Payment.find({ user: req.user._id }).populate('order');
    res.json({ payments });
  } catch (err) {
    res.status(500).json({ message: 'Failed to fetch payments' });
  }
};
