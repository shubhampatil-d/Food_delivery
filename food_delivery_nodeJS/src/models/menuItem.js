const mongoose = require('mongoose');

const menuItemSchema = new mongoose.Schema({
  restaurant: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Restaurant',
    required: true,
  },
  category: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'MenuCategory',
    required: true,
  },
  name: {
    type: String,
    required: true,
  },
  isVeg: {
    type: Boolean,
    default: true,
  },
  price: {
    type: Number,
    required: true,
  },
  description: String,
  isAvailable: {
    type: Boolean,
    default: true,
  },
  customizations: [
    {
      name: String,
      price: Number,
    }
  ],
}, {
  timestamps: true,
});

module.exports = mongoose.model('MenuItem', menuItemSchema);
