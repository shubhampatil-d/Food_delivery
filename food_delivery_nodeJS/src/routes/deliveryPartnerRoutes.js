const express = require('express');
const {
  registerPartner,
  updateLocation,
  getLocation
} = require('../controllers/deliveryPartnerController');
const router = express.Router();

router.post('/register', registerPartner); // admin route
router.put('/:id/location', updateLocation); // delivery partner updates their location
router.get('/:id/location', getLocation); // customer/app fetches partner location

module.exports = router;
