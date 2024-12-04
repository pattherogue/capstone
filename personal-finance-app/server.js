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
    category: String,
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

// Add transaction with improved validation
app.post('/api/transaction', async (req, res) => {
  try {
    const { email, transaction } = req.body;
    
    if (!email || !transaction) {
      return res.status(400).json({ 
        message: 'Missing required fields'
      });
    }

    const user = await User.findOne({ email });
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    // Validate and parse transaction data
    const parsedTransaction = {
      date: new Date(transaction.date),
      amount: Math.abs(Number(transaction.amount)), // Ensure positive number
      type: transaction.type || 'expense',
      category: transaction.type === 'income' ? null : transaction.category
    };

    // Validate amount
    if (isNaN(parsedTransaction.amount)) {
      return res.status(400).json({ message: 'Invalid amount' });
    }

    // Validate category for expenses
    if (parsedTransaction.type === 'expense' && !parsedTransaction.category) {
      return res.status(400).json({ message: 'Category required for expenses' });
    }

    // Add transaction to array
    user.transactions.push(parsedTransaction);

    // Update totals
    if (parsedTransaction.type === 'expense') {
      user.expenses[parsedTransaction.category] = (user.expenses[parsedTransaction.category] || 0) + parsedTransaction.amount;
    } else {
      user.income = (user.income || 0) + parsedTransaction.amount;
    }

    await user.save();
    res.json({
      message: 'Transaction added successfully',
      user
    });

  } catch (error) {
    console.error('Transaction error:', error);
    res.status(500).json({ message: error.message });
  }
});

// Delete transaction with improved error handling
app.delete('/api/transaction/:email/:index', async (req, res) => {
  try {
    const { email, index } = req.params;
    const parsedIndex = parseInt(index);

    const user = await User.findOne({ email });
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    if (isNaN(parsedIndex) || parsedIndex < 0 || parsedIndex >= user.transactions.length) {
      return res.status(400).json({ message: 'Invalid transaction index' });
    }

    // Get the transaction to be removed
    const transaction = user.transactions[parsedIndex];

    // Update totals
    if (transaction.type === 'expense' && transaction.category) {
      user.expenses[transaction.category] = Math.max(0, (user.expenses[transaction.category] || 0) - transaction.amount);
    } else if (transaction.type === 'income') {
      user.income = Math.max(0, (user.income || 0) - transaction.amount);
    }

    // Remove the transaction
    user.transactions.splice(parsedIndex, 1);
    await user.save();

    res.json({
      message: 'Transaction deleted successfully',
      user
    });
  } catch (error) {
    console.error('Delete transaction error:', error);
    res.status(500).json({ message: error.message });
  }
});

const PORT = process.env.PORT || 5001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});