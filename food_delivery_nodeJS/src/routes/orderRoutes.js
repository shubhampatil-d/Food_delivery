const express = require('express');
const { placeOrder, getMyOrders, updateOrderStatus } = require('../controllers/orderController');
const protect = require('../middleware/auth');

const router = express.Router();

router.post('/', protect, placeOrder);
router.get('/', protect, getMyOrders);
router.put('/:id/status', protect, updateOrderStatus); // admin use for now

module.exports = router;
