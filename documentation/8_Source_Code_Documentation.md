# Source Code and Executable Files Documentation

This section provides an overview of the project's repository structure, key source code files, executable files, build, and run instructions, as well as the required dependencies.

## Repository Structure
The repository is organized as follows:

```
personal-finance-app/
├── client/                        # Frontend React application
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── Dashboard.js      # Main dashboard component
│   │   │   ├── ExpenseForm.js    # Transaction form component
│   │   │   ├── MLInsights.js     # ML insights component
│   │   │   ├── RecommendationCard.js  # Recommendations component
│   │   │   └── TransactionList.js     # Transaction history component
│   │   ├── App.js               # Root React component
│   │   └── index.js             # Entry point
│   └── package.json             # Frontend dependencies
│
├── personal-finance/            # Backend Node.js application
│   ├── server.js               # Express server
│   ├── predict.py              # ML prediction service
│   ├── train_model.py          # ML model training script
│   ├── requirements.txt        # Python dependencies
│   └── package.json            # Backend dependencies
│
├── data/                       # Data files
│   └── data.csv               # Training dataset
│
└── models/                     # Trained ML models
    ├── savings_model.joblib    # Saved RandomForest model
    └── scaler.joblib          # Saved StandardScaler
```

## Executable Files
The following are the executable commands used for building and running the application:

1. Frontend Application (client/):
   - `npm start`: Starts development server
   - `npm run build`: Creates production build

2. Backend Server (personal-finance/):
   - `node server.js`: Starts Express server
   - `npm start`: Starts server with nodemon

3. ML Service:
   - `python train_model.py`: Trains and saves ML model
   - `python predict.py`: Starts prediction service

4. Model Files:
   - `savings_model.joblib`: Trained ML model
   - `scaler.joblib`: Feature scaler

## Key Source Code Files

### Frontend (React)
1. Dashboard.js - Main component
```javascript
// Main visualization and data display logic
// Handles data fetching and state management
// Integrates all sub-components
```

2. MLInsights.js - ML visualization
```javascript
// Displays ML predictions and insights
// Handles data transformation for charts
// Shows model confidence and recommendations
```

### Backend (Node.js)
1. server.js - Express server
```javascript
// API endpoints
// Database operations
// Transaction handling
// User management
```

### ML Service (Python)
1. train_model.py - Model training
```python
# Data preprocessing
# Model training
# Model evaluation
# Model saving
```

2. predict.py - Prediction service
```python
# Model loading
# Feature processing
# Prediction generation
# Recommendation logic
```

## Build and Run Instructions
1. Build Frontend:
```bash
cd client
npm install
npm run build
```

2. Build Backend:
```bash
cd personal-finance
npm install
```

3. Prepare Python Environment:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Run All Services:
```bash
# Terminal 1 - Frontend
cd client
npm start

# Terminal 2 - Backend
cd personal-finance
node server.js

# Terminal 3 - ML Service
cd personal-finance
python predict.py
```

## Dependencies
1. Frontend:
- React: JavaScript library for building user interfaces.
- Material-UI: UI components library for React.
- Recharts: Charting library for React.
- Axios: HTTP client for making API requests.

2. Backend:
- Express: Web framework for Node.js.
- Mongoose: ODM (Object Data Modeling) library for MongoDB.
- Cors: Middleware to enable cross-origin requests.
- Dotenv: Module for loading environment variables.

3. ML Service:
- Flask: Python web framework for creating APIs.
- Scikit-learn: Machine learning library for Python.
- Pandas: Data manipulation and analysis library.
- NumPy: Core library for numerical computations.
- Joblib: Library for saving and loading Python objects, such as trained models.