# combined_overbooking_tool.py
# 🔁 Full pipeline: Predict no-show, safe overbooking, and profit optimization

import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

# 1️⃣ Input from user
origin = input("Enter origin airport code (e.g., DEL): ")
destination = input("Enter destination airport code (e.g., DXB): ")
route = origin + ' -> ' + destination
capacity = int(input("Enter flight capacity (e.g., 620): "))
ticket_price = int(input("Enter ticket price in ₹ (e.g., 30000): "))

data_path = os.path.join("Data", "MOCK_DATA.xlsx")
df = pd.read_excel(data_path)

# 2️⃣ Create route column and encode
df['route'] = df['origin'] + ' -> ' + df['destination']
le = LabelEncoder()
df['route_encoded'] = le.fit_transform(df['route'])

# 3️⃣ Train model
model = LinearRegression()
df['route_encoded'] = le.transform(df['route'])
features = df[['capacity', 'ticket_price (IN USD)', 'route_encoded']]
target = df['no_show_rate']
model.fit(features, target)

# Encode the input route
try:
    input_route_encoded = le.transform([route])[0]
except ValueError:
    print("❌ Error: Route not found in training data.")
    exit()

# 4️⃣ Predict no-show rate
new_data = pd.DataFrame([[capacity, ticket_price, input_route_encoded]],
                        columns=['capacity', 'ticket_price (IN USD)', 'route_encoded'])
predicted_noshow = model.predict(new_data)[0]
print(f"\nPredicted No-Show Rate: {predicted_noshow:.2f}%")

# 5️⃣ Calculate safe overbooking
safe_extra = int(capacity / (1 - 0.9 * (predicted_noshow / 100)) - capacity)
print(f"Safe Overbooking (buffered): +{safe_extra} tickets")

# 6️⃣ Simulate optimal overbooking point
SIMULATIONS = 1000
denied_boarding_cost = 2 * ticket_price
max_profit = -float('inf')
best_extra = 0

for extra in range(0, 100):
    total_profit = []
    for _ in range(SIMULATIONS):
        actual_noshow_rate = np.random.normal(predicted_noshow, 1.0) / 100
        actual_showup = int((capacity + extra) * (1 - actual_noshow_rate))
        if actual_showup <= capacity:
            profit = (capacity + extra) * ticket_price
        else:
            denied = actual_showup - capacity
            profit = (capacity + extra) * ticket_price - denied * denied_boarding_cost
        total_profit.append(profit)

    avg_profit = np.mean(total_profit)
    if avg_profit > max_profit:
        max_profit = avg_profit
        best_extra = extra

print(f"Optimal Overbooking: +{best_extra} tickets")
print(f"Estimated Max Profit: ₹{int(max_profit):,}")
