const express = require('express');
const { addCategory, addMenuItem, getMenuByRestaurant, getCategoriesByRestaurant } = require('../controllers/menuController');
const protect = require('../middleware/auth');

const router = express.Router();

router.post('/categories', protect, addCategory); // Add category
router.post('/items', protect, addMenuItem);      // Add menu item
router.get('/categories', protect, getCategoriesByRestaurant); // Fetch categories for a restaurant
router.get('/:restaurantId', getMenuByRestaurant); // Public route to get menu

module.exports = router;
