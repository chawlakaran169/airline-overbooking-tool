
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression

# Load dataset
df = pd.read_excel("../Data/MOCK_DATA.xlsx")

# Create route column and encode it
df['route'] = df['origin'] + ' -> ' + df['destination']
le = LabelEncoder()
df['route_encoded'] = le.fit_transform(df['route'])

# Feature and target selection
features = df[['capacity', 'ticket_price (IN USD)', 'route_encoded']]
target = df['no_show_rate']

# Train-test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict no-show rates for full dataset
df['predicted_no_show_rate'] = model.predict(features)

# Overbooking calculation function
def compute_optimal_overbooking(capacity, predicted_noshow_rate, buffer=0.9):
    adjusted_rate = buffer * (predicted_noshow_rate / 100)
    safe_tickets_to_sell = capacity / (1 - adjusted_rate)
    return int(safe_tickets_to_sell)

#1.  Apply to entire dataset
df['optimal_tickets_to_sell'] = df.apply(
    lambda row: compute_optimal_overbooking(row['capacity'], row['predicted_no_show_rate'], buffer=0.9), axis=1)

df['overbooking_margin'] = df['optimal_tickets_to_sell'] - df['capacity']

# Export to Excel
df.to_excel("Optimized_Overbooking_Output.xlsx", index=False)

print("✅ Optimization complete. Output saved to 'Optimized_Overbooking_Output.xlsx'")
# for a certain dataset 
capacity = 650
predicted_noshow = 7.44  # you can also use your model to predict this
optimal_tickets = compute_optimal_overbooking(capacity, predicted_noshow, buffer=0.9)

print(f"✅ Capacity: {capacity}")
print(f"📉 Predicted No-Show Rate: {predicted_noshow:.2f}%")
print(f"🎟️ Safe Tickets to Sell (with 90% buffer): {optimal_tickets}")
print(f"📈 Overbooking Margin: {optimal_tickets - capacity} seats")


# ------------------------------Phase 5 : Business Decision Making & strategy--------------------------------->
# route based risk analysis 
df['extra_revenue'] = df['overbooking_margin'] * df['ticket_price (IN USD)']

# group by route and calculate statistics 
route_summary = df.groupby('route').agg({
    'predicted_no_show_rate': ['mean', 'std'],
    'extra_revenue': 'mean'
}).reset_index()
# rename coulmns 
route_summary.columns = ['route','avg_no_show','std_dev','avg_extra_revenue']

# classify risk level 
def classify_risk(std_dev):
    if std_dev < 0.5:
        return 'Low'
    elif std_dev < 1.5:
        return 'Medium'
    else:
        return 'High'

route_summary['risk_level'] = route_summary['std_dev'].apply(classify_risk)
route_summary.to_excel("Route_Risk_Summary.xlsx", index=False)
print("✅ Route-based risk summary saved to 'Route_Risk_Summary.xlsx'")