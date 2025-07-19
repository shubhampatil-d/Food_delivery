const express = require('express');
const protect = require('../middleware/auth');
const { addToCart, getCart, clearCart, updateCart } = require('../controllers/cartController');

const router = express.Router();

router.get('/', protect, getCart);
router.post('/', protect, addToCart);
router.delete('/', protect, clearCart);
router.put('/', protect, updateCart);

module.exports = router;
