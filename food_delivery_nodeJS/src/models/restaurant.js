const mongoose = require('mongoose');

const restaurantSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  cuisineType: {
    type: String,
    required: true,
  },
  description: String,
  address: {
    type: String,
    required: true,
  },
  location: {
    latitude: {
      type: Number,
      required: true,
    },
    longitude: {
      type: Number,
      required: true,
    },
  },
  operatingHours: {
    open: String,  // "10:00 AM"
    close: String, // "11:00 PM"
  },
  minimumOrderAmount: {
    type: Number,
    default: 0,
  },
  deliveryFee: {
    type: Number,
    default: 0,
  },
  averagePrepTime: {
    type: Number, // in minutes
  },
  status: {
    type: String,
    enum: ['open', 'closed'],
    default: 'open',
  },
  rating: {
    type: Number,
    default: 0,
  },
}, {
  timestamps: true,
});

module.exports = mongoose.model('Restaurant', restaurantSchema);
