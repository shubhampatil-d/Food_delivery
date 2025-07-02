const express = require('express');
const { recordPayment, getMyPayments } = require('../controllers/paymentController');
const protect = require('../middleware/auth');

const router = express.Router();

router.post('/', protect, recordPayment);
router.get('/', protect, getMyPayments);

module.exports = router;
