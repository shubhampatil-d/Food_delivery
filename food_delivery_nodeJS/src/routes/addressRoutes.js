const express = require('express');
const protect = require('../middleware/auth');
const {
  addAddress,
  getAddresses,
  setDefaultAddress,
} = require('../controllers/addressController');

const router = express.Router();

router.post('/', protect, addAddress);
router.get('/', protect, getAddresses);
router.put('/:id/set-default', protect, setDefaultAddress);

module.exports = router;
