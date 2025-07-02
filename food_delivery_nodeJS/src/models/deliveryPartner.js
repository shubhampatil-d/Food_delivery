const mongoose = require('mongoose');

const deliveryPartnerSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  phone: String,
  status: {
    type: String,
    enum: ['available', 'busy'],
    default: 'available',
  },
  currentLocation: {
    type: {
      latitude: Number,
      longitude: Number,
    },
    default: null
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('DeliveryPartner', deliveryPartnerSchema);
