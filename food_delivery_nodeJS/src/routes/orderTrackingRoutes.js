const express = require('express');
const { addTrackingUpdate, getOrderTracking } = require('../controllers/orderTrackingController');
const protect = require('../middleware/auth');

const router = express.Router();

router.post('/', protect, addTrackingUpdate); // Admin use
router.get('/:orderId', protect, getOrderTracking); // For user

module.exports = router;
