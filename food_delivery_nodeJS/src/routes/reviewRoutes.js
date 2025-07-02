const express = require('express');
const { addReview, getReviews } = require('../controllers/reviewController');
const protect = require('../middleware/auth');

const router = express.Router();

router.post('/', protect, addReview);
router.get('/:restaurantId', getReviews);

module.exports = router;
