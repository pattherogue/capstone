from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Load the trained model and scaler
try:
    model = joblib.load('savings_model.joblib')
    scaler = joblib.load('scaler.joblib')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    scaler = StandardScaler()

# Category spending thresholds (% of income)
CATEGORY_THRESHOLDS = {
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

def analyze_spending_trends(transactions, income):
    """Analyze spending trends over time"""
    if not transactions:
        return {}
    
    # Group transactions by month and category
    monthly_totals = {}
    for transaction in transactions:
        date = datetime.fromisoformat(transaction['date'].replace('Z', '+00:00'))
        month_key = date.strftime('%Y-%m')
        category = transaction['category']
        
        if month_key not in monthly_totals:
            monthly_totals[month_key] = {'total': 0, 'categories': {}}
        
        monthly_totals[month_key]['total'] += transaction['amount']
        monthly_totals[month_key]['categories'][category] = monthly_totals[month_key]['categories'].get(category, 0) + transaction['amount']
    
    return monthly_totals

def generate_smart_recommendations(data):
    """Generate personalized financial recommendations"""
    income = data.get('income', 0)
    expenses = data.get('expenses', {})
    transactions = data.get('transactions', [])
    savings_goal = data.get('savings', {}).get('monthlyGoal', 0)
    total_expenses = sum(expenses.values())
    surplus = income - total_expenses

    recommendations = []
    insights = {}
    actions = []

    # Analyze monthly trends
    spending_trends = analyze_spending_trends(transactions, income)
    
    # Calculate current savings ratio
    savings_ratio = ((income - total_expenses) / income * 100) if income > 0 else 0
    
    # Basic savings assessment
    if savings_ratio < 20:
        if savings_ratio < 10:
            recommendations.append("Your savings rate is critically low. Immediate action recommended.")
        else:
            recommendations.append("Your savings rate is below the recommended 20%. Consider reducing expenses.")
    else:
        recommendations.append("Great job maintaining a healthy savings rate!")

    # Category-specific analysis
    for category, amount in expenses.items():
        threshold = CATEGORY_THRESHOLDS.get(category, 0.1) * income
        if amount > threshold:
            percentage_over = ((amount - threshold) / threshold * 100)
            recommendations.append(
                f"Your {category} spending is {percentage_over:.1f}% over the recommended limit. "
                f"Consider reducing it by ${(amount - threshold):.2f}"
            )

    # Surplus allocation recommendations
    if surplus > 0:
        if data.get('debt', 0) > 0:
            debt_allocation = surplus * 0.7
            savings_allocation = surplus * 0.3
            actions.append({
                'type': 'allocation',
                'debt_payment': debt_allocation,
                'savings': savings_allocation,
                'message': f"Recommend allocating ${debt_allocation:.2f} to debt and ${savings_allocation:.2f} to savings"
            })
        else:
            emergency_fund = surplus * 0.4
            investments = surplus * 0.4
            discretionary = surplus * 0.2
            actions.append({
                'type': 'allocation',
                'emergency_fund': emergency_fund,
                'investments': investments,
                'discretionary': discretionary,
                'message': f"Consider splitting surplus: ${emergency_fund:.2f} to emergency fund, "
                         f"${investments:.2f} to investments, ${discretionary:.2f} for discretionary spending"
            })

    # Analyze spending trends
    if spending_trends:
        months = sorted(spending_trends.keys())
        if len(months) >= 2:
            current_month = spending_trends[months[-1]]['total']
            previous_month = spending_trends[months[-2]]['total']
            change = ((current_month - previous_month) / previous_month * 100)
            
            insights['spending_trend'] = {
                'current_month': current_month,
                'previous_month': previous_month,
                'change_percentage': change,
                'message': f"Your spending has {'increased' if change > 0 else 'decreased'} by {abs(change):.1f}% compared to last month"
            }

    return {
        'recommendations': recommendations,
        'insights': insights,
        'actions': actions,
        'spending_trends': spending_trends
    }

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'recommendations': ['Please provide financial data for analysis.']
            }), 400

        # Generate comprehensive recommendations
        analysis_result = generate_smart_recommendations(data)
        
        # Add ML model predictions if available
        if model is not None:
            features = prepare_features(data)
            if features is not None:
                features_scaled = scaler.transform(features.reshape(1, -1))
                prediction = model.predict(features_scaled)[0]
                analysis_result['predicted_savings_ratio'] = float(prediction)

        return jsonify(analysis_result)
        
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
    print("Starting enhanced prediction server on port 5002...")
    app.run(port=5002, debug=True)