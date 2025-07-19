// createsuperuser.js
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const readline = require('readline');
require('dotenv').config();

const User = require('./src/models/user');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Use the same logic as the main app for MongoDB URI
const mongoUri = process.env.MONGO_URI || process.env.MONGODB_URI || 'mongodb://localhost:27017/foodDelivery';

if (!mongoUri) {
  console.error('MongoDB URI not set. Please set MONGO_URI in your .env file.');
  process.exit(1);
}

mongoose.connect(mongoUri, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => {
    rl.question('Admin name: ', name => {
      rl.question('Admin email: ', email => {
        rl.question('Admin phone: ', phone => {
          rl.question('Admin password: ', async password => {
            try {
              const hashedPassword = await bcrypt.hash(password, 10);
              const user = new User({
                name,
                email,
                phone,
                password: hashedPassword,
                role: 'admin'
              });
              await user.save();
              console.log('Admin user created successfully!');
            } catch (err) {
              console.error('Error creating admin user:', err.message);
            } finally {
              mongoose.disconnect();
              rl.close();
            }
          });
        });
      });
    });
  })
  .catch(err => {
    console.error('DB connection error:', err);
    process.exit(1);
  }); 