from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
CORS(app)

# Load the trained model and scaler
try:
    model = joblib.load('savings_model.joblib')
    scaler = joblib.load('scaler.joblib')
except Exception as e:
    print(f"Error loading model: {e}")
    # Initialize empty model and scaler for development
    model = None
    scaler = StandardScaler()

def prepare_features(data):
    """Prepare features for prediction"""
    # Initialize feature array
    features = np.zeros(15)  # Adjust based on your model's expected features
    
    try:
        # Extract values from data
        income = float(data.get('income', 0))
        expenses = data.get('expenses', {})
        
        # Map features to array
        features[0] = income
        features[1] = float(expenses.get('rent', 0))
        features[2] = float(expenses.get('loanRepayment', 0))
        features[3] = float(expenses.get('insurance', 0))
        features[4] = float(expenses.get('groceries', 0))
        features[5] = float(expenses.get('transport', 0))
        features[6] = float(expenses.get('eatingOut', 0))
        features[7] = float(expenses.get('entertainment', 0))
        features[8] = float(expenses.get('utilities', 0))
        features[9] = float(expenses.get('healthcare', 0))
        features[10] = float(expenses.get('education', 0))
        features[11] = float(expenses.get('miscellaneous', 0))
        
    except Exception as e:
        print(f"Error preparing features: {e}")
        return None
    
    return features

def generate_basic_recommendations(income, expenses):
    """Generate basic recommendations without ML model"""
    recommendations = []
    total_expenses = sum(expenses.values())
    savings_ratio = ((income - total_expenses) / income * 100) if income > 0 else 0
    
    # Basic recommendations based on savings ratio
    if savings_ratio < 10:
        recommendations.extend([
            "Your current savings rate is below recommended levels.",
            "Consider reducing non-essential expenses.",
            "Look for opportunities to increase your income."
        ])
    elif savings_ratio < 20:
        recommendations.extend([
            "You're saving at a moderate rate.",
            "Review your monthly subscriptions for potential savings.",
            "Consider setting up automatic savings transfers."
        ])
    else:
        recommendations.extend([
            "Excellent savings rate! Keep up the good work.",
            "Consider investing your surplus savings.",
            "Review your investment strategy periodically."
        ])
    
    # Category-specific recommendations
    for category, amount in expenses.items():
        if amount > (income * 0.3) and category == 'rent':
            recommendations.append("Your housing costs are relatively high. Consider if there are ways to reduce this expense.")
        elif amount > (income * 0.15) and category == 'eatingOut':
            recommendations.append("You might save more by reducing dining out expenses.")
        elif amount > (income * 0.1) and category == 'entertainment':
            recommendations.append("Consider looking for free or lower-cost entertainment options.")
    
    return recommendations

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'recommendations': ['Please provide financial data for analysis.']
            }), 400
        
        # Extract main values
        income = float(data.get('income', 0))
        expenses = data.get('expenses', {})
        
        # Generate recommendations based on rules if model isn't available
        recommendations = generate_basic_recommendations(income, expenses)
        
        # If model is available, add ML-based predictions
        if model is not None:
            features = prepare_features(data)
            if features is not None:
                features_scaled = scaler.transform(features.reshape(1, -1))
                prediction = model.predict(features_scaled)[0]
                
                recommendations.append(f"Based on our analysis, your optimal savings ratio should be {prediction:.1f}%")
        
        return jsonify({
            'recommendations': recommendations,
            'status': 'success'
        })
        
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({
            'error': 'Internal server error',
            'recommendations': [
                'Unable to process financial data at this time.',
                'Please ensure all financial information is properly formatted.'
            ]
        }), 500

if __name__ == '__main__':
    print("Starting prediction server on port 5002...")
    app.run(port=5002, debug=True)