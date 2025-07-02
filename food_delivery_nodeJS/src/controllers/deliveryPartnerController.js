const DeliveryPartner = require('../models/deliveryPartner');

// Create a partner (admin use only)
exports.registerPartner = async (req, res) => {
  try {
    const partner = await DeliveryPartner.create(req.body);
    res.status(201).json({ message: 'Partner registered', partner });
  } catch (err) {
    res.status(500).json({ message: 'Failed to register partner' });
  }
};

// Update location
exports.updateLocation = async (req, res) => {
  try {
    const { latitude, longitude } = req.body;
    const partnerId = req.params.id;

    const updated = await DeliveryPartner.findByIdAndUpdate(
      partnerId,
      { currentLocation: { latitude, longitude }, status: 'busy' },
      { new: true }
    );

    res.json({ message: 'Location updated', updated });
  } catch (err) {
    res.status(500).json({ message: 'Failed to update location' });
  }
};

// Get partner location
exports.getLocation = async (req, res) => {
  try {
    const partnerId = req.params.id;
    const partner = await DeliveryPartner.findById(partnerId);
    res.json({ location: partner.currentLocation });
  } catch (err) {
    res.status(500).json({ message: 'Failed to fetch location' });
  }
};
