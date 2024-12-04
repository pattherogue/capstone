from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    filename='finance_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Load or train model
try:
    model = joblib.load('savings_model.joblib')
    scaler = joblib.load('scaler.joblib')
    logger.info("Model and scaler loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    # Train new model if loading fails
    df = pd.read_csv('data.csv')
    X = df.drop(['Desired_Savings_Percentage'], axis=1)
    y = df['Desired_Savings_Percentage']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)
    
    # Save model and scaler
    joblib.dump(model, 'savings_model.joblib')
    joblib.dump(scaler, 'scaler.joblib')
    logger.info("New model trained and saved")

def prepare_features(data):
    """Prepare features for prediction"""
    features = []
    feature_names = [
        'income', 'age', 'dependents', 'rent', 'loan_repayment', 'insurance',
        'groceries', 'transport', 'eating_out', 'entertainment', 'utilities',
        'healthcare', 'education', 'miscellaneous'
    ]
    
    try:
        # Extract and normalize features
        for name in feature_names:
            if name == 'income':
                value = float(data.get('income', 0))
            elif name in data.get('expenses', {}):
                value = float(data['expenses'].get(name, 0))
            else:
                value = 0.0
            features.append(value)
        
        return np.array(features).reshape(1, -1)
    except Exception as e:
        logger.error(f"Error preparing features: {e}")
        return None

def analyze_spending_patterns(transactions, income):
    """Analyze historical spending patterns"""
    try:
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        
        # Monthly aggregations
        monthly = df.resample('M').sum()
        
        # Calculate trends
        trend = monthly['amount'].pct_change().mean()
        volatility = monthly['amount'].std()
        
        # Category analysis
        category_totals = df.groupby('category')['amount'].sum()
        category_ratios = (category_totals / income * 100).round(2)
        
        return {
            'trend': trend,
            'volatility': volatility,
            'category_ratios': category_ratios.to_dict(),
            'monthly_totals': monthly['amount'].to_list()
        }
    except Exception as e:
        logger.error(f"Error analyzing spending patterns: {e}")
        return None

@app.route('/predict', methods=['POST'])
def predict():
    try:
        start_time = datetime.now()
        data = request.get_json()
        logger.info(f"Received prediction request for user data")
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'recommendations': ['Please provide financial data for analysis.']
            }), 400

        # Prepare features and make prediction
        features = prepare_features(data)
        if features is not None:
            features_scaled = scaler.transform(features)
            prediction = model.predict(features_scaled)[0]
            prediction_confidence = model.score(features_scaled, [prediction])
        else:
            prediction = None
            prediction_confidence = None

        # Analyze spending patterns
        spending_analysis = analyze_spending_patterns(
            data.get('transactions', []),
            data.get('income', 0)
        )

        # Generate recommendations
        recommendations = []
        insights = {}
        actions = []

        # Basic financial health check
        income = data.get('income', 0)
        expenses = data.get('expenses', {})
        total_expenses = sum(expenses.values())
        current_savings_ratio = ((income - total_expenses) / income * 100) if income > 0 else 0

        if prediction is not None:
            if current_savings_ratio < prediction:
                recommendations.append(f"You're saving {current_savings_ratio:.1f}% of your income. Our model suggests a target of {prediction:.1f}%")
            else:
                recommendations.append(f"Great job! You're exceeding the recommended savings ratio of {prediction:.1f}%")

        # Spending pattern recommendations
        if spending_analysis:
            if spending_analysis['trend'] < 0:
                recommendations.append("Your spending is trending downward - great job controlling expenses!")
            elif spending_analysis['trend'] > 0.1:
                recommendations.append("Your spending is trending upward. Consider reviewing recent expenses.")

            # Category-specific recommendations
            for category, ratio in spending_analysis['category_ratios'].items():
                if ratio > 30 and category in ['entertainment', 'eating_out']:
                    recommendations.append(f"Your {category} spending is high at {ratio:.1f}% of income. Consider reducing this expense.")

        # Add insights
        insights = {
            'spending_patterns': spending_analysis,
            'model_confidence': prediction_confidence,
            'savings_prediction': prediction
        }

        # Generate specific actions
        if current_savings_ratio < prediction:
            deficit = prediction - current_savings_ratio
            target_savings = (income * (prediction / 100))
            actions.append({
                'type': 'savings_adjustment',
                'description': f'To reach the recommended savings ratio, aim to save an additional ${(income * (deficit / 100)):.2f} per month',
                'target_amount': target_savings
            })

        response_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Prediction completed in {response_time} seconds")

        return jsonify({
            'recommendations': recommendations,
            'insights': insights,
            'actions': actions,
            'metrics': {
                'current_savings_ratio': current_savings_ratio,
                'predicted_optimal_ratio': prediction,
                'model_confidence': prediction_confidence
            }
        })

    except Exception as e:
        logger.error(f"Error processing prediction request: {e}")
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