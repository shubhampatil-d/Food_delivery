const express = require('express');
const { addCategory, addMenuItem, getMenuByRestaurant } = require('../controllers/menuController');
const protect = require('../middleware/auth');

const router = express.Router();

router.post('/categories', protect, addCategory); // Add category
router.post('/items', protect, addMenuItem);      // Add menu item
router.get('/:restaurantId', getMenuByRestaurant); // Public route to get menu

module.exports = router;
