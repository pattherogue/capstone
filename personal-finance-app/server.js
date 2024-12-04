const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const dotenv = require('dotenv');
const axios = require('axios');

dotenv.config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// MongoDB connection with error handling
mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.error('MongoDB connection error:', err));

// User Schema
const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  income: { type: Number, default: 0 },
  expenses: {
    rent: { type: Number, default: 0 },
    loanRepayment: { type: Number, default: 0 },
    insurance: { type: Number, default: 0 },
    groceries: { type: Number, default: 0 },
    transport: { type: Number, default: 0 },
    eatingOut: { type: Number, default: 0 },
    entertainment: { type: Number, default: 0 },
    utilities: { type: Number, default: 0 },
    healthcare: { type: Number, default: 0 },
    education: { type: Number, default: 0 },
    miscellaneous: { type: Number, default: 0 }
  },
  savings: {
    currentAmount: { type: Number, default: 0 },
    targetAmount: { type: Number, default: 0 },
    monthlyGoal: { type: Number, default: 0 }
  },
  transactions: [{
    date: { type: Date, required: true },
    category: { type: String, required: true },
    amount: { type: Number, required: true },
    type: { type: String, required: true, enum: ['income', 'expense'] }
  }]
});

const User = mongoose.model('User', userSchema);

// Prediction endpoint - proxy to Flask server
app.post('/api/predict', async (req, res) => {
  try {
    const response = await axios.post('http://localhost:5002/predict', req.body);
    res.json(response.data);
  } catch (error) {
    console.error('Prediction error:', error.message);
    res.status(500).json({ 
      error: 'Failed to get prediction',
      recommendations: [
        'Unable to process financial data at this time.',
        'Consider maintaining a savings rate of 20% of your income.',
        'Review your largest expense categories for potential savings.'
      ]
    });
  }
});

// Create default user if doesn't exist
app.get('/api/user/:email', async (req, res) => {
  try {
    let user = await User.findOne({ email: req.params.email });
    
    if (!user) {
      // Create a default user if none exists
      user = await User.create({
        email: req.params.email,
        income: 5000,
        expenses: {
          rent: 1500,
          loanRepayment: 500,
          insurance: 200,
          groceries: 400,
          transport: 200,
          eatingOut: 300,
          entertainment: 200,
          utilities: 150,
          healthcare: 100,
          education: 0,
          miscellaneous: 100
        },
        savings: {
          currentAmount: 1000,
          targetAmount: 10000,
          monthlyGoal: 500
        },
        transactions: []
      });
    }
    
    res.json(user);
  } catch (error) {
    console.error('User fetch error:', error);
    res.status(500).json({ 
      message: error.message,
      details: 'Error creating or fetching user'
    });
  }
});

// Update user financial data
app.post('/api/user/update', async (req, res) => {
  try {
    const { email, income, expenses, savings } = req.body;
    if (!email) {
      return res.status(400).json({ 
        message: 'Email is required'
      });
    }

    const user = await User.findOneAndUpdate(
      { email },
      { income, expenses, savings },
      { new: true, runValidators: true }
    );

    if (!user) {
      return res.status(404).json({ 
        message: 'User not found'
      });
    }

    res.json(user);
  } catch (error) {
    console.error('Update error:', error);
    res.status(500).json({ 
      message: error.message,
      details: 'Error updating user data'
    });
  }
});

// Add transaction with improved error handling
app.post('/api/transaction', async (req, res) => {
  try {
    const { email, transaction } = req.body;
    
    if (!email || !transaction) {
      return res.status(400).json({ 
        message: 'Missing required fields',
        details: 'Email and transaction data are required'
      });
    }

    // Validate transaction data
    const { date, category, amount, type } = transaction;
    if (!date || !category || !amount || !type) {
      return res.status(400).json({ 
        message: 'Invalid transaction data',
        details: 'Date, category, amount, and type are required'
      });
    }

    const user = await User.findOne({ email });
    if (!user) {
      return res.status(404).json({ 
        message: 'User not found',
        details: 'No user found with the provided email'
      });
    }

    // Add transaction to user's transactions array
    user.transactions.push({
      date: new Date(date),
      category: String(category),
      amount: Number(amount),
      type: String(type)
    });

    // Update the corresponding expense category
    user.expenses[category] = (user.expenses[category] || 0) + Number(amount);

    // Save the updated user document
    await user.save();

    res.json({
      message: 'Transaction added successfully',
      user
    });

  } catch (error) {
    console.error('Transaction error:', error);
    res.status(500).json({ 
      message: 'Error adding transaction',
      details: error.message
    });
  }
});

const PORT = process.env.PORT || 5001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});