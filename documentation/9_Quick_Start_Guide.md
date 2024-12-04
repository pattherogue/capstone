# Quick Start Guide

## Prerequisites
- Node.js (v14+)
- Python (v3.8+)
- MongoDB
- npm or yarn

## Installation Steps

1. Clone the Repository
```bash
git clone [repository-url]
cd personal-finance-app
```

2. Backend Setup
```bash
# Install backend dependencies
cd personal-finance
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your MongoDB URI

# Start the server
npm start
```

3. ML Service Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install Python dependencies
pip install -r requirements.txt

# Start the ML service
python predict.py
```

4. Frontend Setup
```bash
# Install frontend dependencies
cd client
npm install

# Start the development server
npm start
```

## Usage Guide
1. Access the application at http://localhost:3000
2. Add transactions using the form
3. View financial insights in the dashboard
4. Monitor recommendations
5. Track savings progress

## Troubleshooting
- Check all three servers are running
- Verify MongoDB connection
- Check console for errors
- Ensure correct ports are available
