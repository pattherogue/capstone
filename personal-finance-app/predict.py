from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import pandas as pd
from datetime import datetime
import joblib
import logging

# Configure logging
logging.basicConfig(
    filename='financial_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Category spending thresholds (% of income)
THRESHOLDS = {
    'rent': 0.3,
    'loanRepayment': 0.15,
    'insurance': 0.1,
    'groceries': 0.15,
    'transport': 0.15,
    'eatingOut': 0.1,
    'entertainment': 0.1,
    'utilities': 0.1,
    'healthcare': 0.1,
    'education': 0.2,
    'miscellaneous': 0.05
}

try:
    logger.info("Loading ML model and scaler...")
    model = joblib.load('savings_model.joblib')
    scaler = joblib.load('scaler.joblib')
    logger.info("Model loaded successfully")
except Exception as e:
    logger.warning(f"Error loading model: {e}")
    logger.info("Training new model...")
    
    # Load training data
    df = pd.read_csv('data.csv')
    
    # Prepare features
    features = ['Income', 'Rent', 'Loan_Repayment', 'Insurance', 'Groceries', 
                'Transport', 'Eating_Out', 'Entertainment', 'Utilities', 
                'Healthcare', 'Education', 'Miscellaneous']
    
    X = df[features]
    y = df['Desired_Savings_Percentage']
    
    # Train model
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)
    
    # Save model
    joblib.dump(model, 'savings_model.joblib')
    joblib.dump(scaler, 'scaler.joblib')
    logger.info("New model trained and saved")

def analyze_spending_patterns(transactions, income):
    """Analyze spending patterns and trends"""
    if not transactions:
        return None
        
    try:
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        
        # Monthly analysis
        monthly_spend = df.groupby('month')['amount'].sum()
        
        # Calculate trends
        if len(monthly_spend) > 1:
            trend = monthly_spend.pct_change().mean()
            volatility = monthly_spend.std() / monthly_spend.mean()
        else:
            trend = 0
            volatility = 0
            
        # Category analysis
        category_totals = df.groupby('category')['amount'].sum()
        category_percentages = (category_totals / income * 100).round(1)
        
        return {
            'trend': float(trend),
            'volatility': float(volatility),
            'monthly_totals': monthly_spend.tolist(),
            'category_analysis': category_percentages.to_dict()
        }
        
    except Exception as e:
        logger.error(f"Error in spending analysis: {e}")
        return None

def predict_optimal_savings(data):
    """Predict optimal savings ratio based on financial data"""
    try:
        features = np.zeros(12)  # Number of features used in training
        
        # Map input data to feature array
        features[0] = data.get('income', 0)
        expenses = data.get('expenses', {})
        
        for i, category in enumerate(['rent', 'loanRepayment', 'insurance', 'groceries',
                                    'transport', 'eatingOut', 'entertainment', 'utilities',
                                    'healthcare', 'education', 'miscellaneous']):
            features[i+1] = expenses.get(category, 0)
            
        # Scale features
        features_scaled = scaler.transform(features.reshape(1, -1))
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        
        # Get feature importance
        importance = dict(zip(
            ['income'] + list(THRESHOLDS.keys()),
            model.feature_importances_
        ))
        
        return prediction, importance
        
    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        return None, None

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No data provided',
                'recommendations': ['Please provide financial data for analysis.']
            }), 400
            
        # Get predictions
        optimal_savings, feature_importance = predict_optimal_savings(data)
        spending_patterns = analyze_spending_patterns(
            data.get('transactions', []),
            data.get('income', 0)
        )
        
        # Generate recommendations
        recommendations = []
        insights = {
            'spending_patterns': spending_patterns,
            'feature_importance': feature_importance,
            'optimal_savings_ratio': optimal_savings
        }
        
        # Add recommendations based on spending patterns
        if spending_patterns:
            if spending_patterns['trend'] > 0.1:
                recommendations.append("Your spending has been increasing. Consider reviewing your budget.")
            elif spending_patterns['trend'] < -0.05:
                recommendations.append("Great job reducing your spending!")
                
            if spending_patterns['volatility'] > 0.3:
                recommendations.append("Your spending patterns show high variability. Consider more consistent budgeting.")
                
        # Add recommendations based on optimal savings
        if optimal_savings:
            current_savings = data.get('income', 0) - sum(data.get('expenses', {}).values())
            current_ratio = (current_savings / data.get('income', 1)) * 100
            
            if current_ratio < optimal_savings:
                recommendations.append(
                    f"You could increase your savings rate from {current_ratio:.1f}% "
                    f"to {optimal_savings:.1f}% based on your income level."
                )
            else:
                recommendations.append("You're exceeding the recommended savings rate!")

        return jsonify({
            'recommendations': recommendations,
            'insights': insights,
            'metrics': {
                'optimal_savings_ratio': optimal_savings,
                'model_confidence': 0.85  # You could calculate this based on model metrics
            }
        })

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({
            'error': 'Internal server error',
            'recommendations': [
                'Unable to process financial data at this time.',
                'Please ensure all financial information is properly formatted.'
            ]
        }), 500

if __name__ == '__main__':
    logger.info("Starting prediction server on port 5002...")
    app.run(port=5002, debug=True)