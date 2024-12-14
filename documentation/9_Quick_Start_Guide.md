# Quick Start Guide

## Current Project Structure
```
capstone/
├── client/                    # Frontend React application
├── personal-finance-app/      # Backend folder
├── data.csv                   # Dataset file
└── train_model.py            # ML model training script
```

## Prerequisites
- Node.js (v14+)
- Python (v3.8+)
- MongoDB
- npm or yarn

## Initial Python Setup (One-time Setup)
```bash
# In root capstone directory
# Create virtual environment
python3 -m venv venv

# Activate virtual environment (IMPORTANT: Do this from root directory)
source venv/bin/activate  # for Mac/Linux
# or venv\Scripts\activate  # for Windows

# Install required Python packages
pip install pandas numpy scikit-learn joblib flask flask-cors

# Train the ML model
python train_model.py
# This will create savings_model.joblib and scaler.joblib

# Copy model files to personal-finance-app folder
cp savings_model.joblib scaler.joblib personal-finance-app/
```

## Application Setup (Three Separate Terminals)

Terminal 1 - Backend (Node.js):
```bash
cd personal-finance-app

# Install Node.js dependencies (one-time setup)
npm install

# Create .env file with:
MONGO_URI=mongodb+srv://pmgomez248:wkHshupzeiZN3hSd@cluster0.0hnc5.mongodb.net/personal_finance?retryWrites=true&w=majority&appName=Cluster0
PORT=5001

# Start the backend server
node server.js
```

Terminal 2 - ML Service (Python):
```bash
# First, go to root directory and activate virtual environment
cd /path/to/capstone  # Go to root capstone directory
source venv/bin/activate  # for Mac/Linux
# or venv\Scripts\activate  # for Windows

# Then go to personal-finance-app and run predict.py
cd personal-finance-app
python predict.py
```

Terminal 3 - Frontend (React):
```bash
cd client

# Install React dependencies (one-time setup)
npm install

# Start the frontend
npm start
```

## Virtual Environment Notes
- Terminal 1 (Backend): NO virtual environment needed
- Terminal 2 (ML Service): YES virtual environment required (activate from root directory)
- Terminal 3 (Frontend): NO virtual environment needed

The virtual environment is ONLY needed for:
1. Installing Python packages (from root directory)
2. Running train_model.py (from root directory)
3. Running predict.py (activate from root directory)

## Verification Steps
1. Check MongoDB Connection (Terminal 1):
   - Should see: "MongoDB connected"
   - Should see: "Server running on port 5001"

2. Check ML Service (Terminal 2):
   - Should see: "Starting prediction server on port 5002"
   - Virtual environment must be active (activated from root directory)

3. Check Frontend (Terminal 3):
   - Browser should open to http://localhost:3000
   - Should see the dashboard interface

## Port Requirements
- Frontend: 3000
- Backend: 5001
- ML Service: 5002

## Common Issues and Solutions
1. MongoDB Connection Issues:
   - Verify .env file exists in personal-finance-app/
   - Check MongoDB URI is correct

2. ML Service Issues:
   - Make sure to activate virtual environment from root directory
   - Check model files are in personal-finance-app/
   - Verify port 5002 is available

3. Frontend Issues:
   - Verify all three services are running
   - Check console for errors
   - Clear browser cache if needed

4. Virtual Environment Issues:
   - Always activate from root capstone directory
   - If "no such file" error, make sure you're in root directory
   - Verify venv folder exists in root directory

## Package Versions
Backend (package.json):
```json
"dependencies": {
  "axios": "^1.7.8",
  "cors": "^2.8.5",
  "dotenv": "^16.4.7",
  "express": "^4.21.1",
  "mongoose": "^8.8.3"
}
```

Python (requirements.txt):
```
flask==3.1.0
flask-cors==5.0.0
numpy==2.1.3
pandas==2.2.3
scikit-learn==1.5.2
joblib==1.4.2
```

## Testing the Application
1. Add a test transaction:
   - Use the Add Transaction form
   - Fill in all required fields
   - Submit and verify charts update

2. View visualizations:
   - Check Expense Distribution pie chart
   - View Monthly Spending bar chart
   - Monitor Transaction History

3. Check ML insights:
   - View AI Analysis Insights
   - Check recommendations
   - Monitor savings progress

## Important Notes
- Keep three terminals running simultaneously
- Only Terminal 2 (ML Service) needs virtual environment
- Always activate virtual environment from root directory
- All services must be running for the application to work
- Check each terminal for error messages if issues occur

For the evaluator: 
1. Follow the terminal-specific instructions carefully
2. Remember to activate the virtual environment from the root capstone directory
3. Only the ML Service (Terminal 2) requires the Python virtual environment
4. Keep all three services running concurrently