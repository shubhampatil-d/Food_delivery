const Review = require('../models/review');

exports.addReview = async (req, res) => {
  try {
    const { restaurant, rating, comment } = req.body;
    const review = await Review.create({
      user: req.user._id,
      restaurant,
      rating,
      comment,
    });
    res.status(201).json({ message: 'Review added', review });
  } catch (err) {
    res.status(500).json({ message: 'Failed to add review' });
  }
};

exports.getReviews = async (req, res) => {
  try {
    const restaurantId = req.params.restaurantId;
    const reviews = await Review.find({ restaurant: restaurantId }).populate('user', 'name');
    res.json({ reviews });
  } catch (err) {
    res.status(500).json({ message: 'Failed to fetch reviews' });
  }
};
