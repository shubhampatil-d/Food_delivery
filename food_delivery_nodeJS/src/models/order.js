const mongoose = require('mongoose');

const orderItemSchema = new mongoose.Schema({
  menuItem: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'MenuItem',
    required: true,
  },
  quantity: {
    type: Number,
    required: true,
  },
  priceAtOrderTime: {
    type: Number,
    required: true,
  },
  customizations: [
    {
      name: String,
      price: Number,
    },
  ],
});

const orderSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
  },
  restaurant: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Restaurant',
    required: true,
  },
  address: {
    type: String,
    required: true,
  },
  status: {
    type: String,
    enum: ['placed', 'confirmed', 'preparing', 'out-for-delivery', 'delivered', 'cancelled'],
    default: 'placed',
  },
  items: [orderItemSchema],
  totalAmount: Number,
  deliveryFee: Number,
  paymentMethod: {
    type: String,
    enum: ['COD', 'UPI', 'CARD'],
    default: 'COD',
  },
  specialInstructions: String,
  estimatedDeliveryTime: String,
}, {
  timestamps: true,
});

module.exports = mongoose.model('Order', orderSchema);
