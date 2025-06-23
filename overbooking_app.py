# overbooking_app.py

import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

# Load data
data_path = os.path.join("Data", "MOCK_DATA.xlsx")
df = pd.read_excel(data_path)

# Prepare route column and label encoding
df['route'] = df['origin'] + ' -> ' + df['destination']
le = LabelEncoder()
df['route_encoded'] = le.fit_transform(df['route'])
df['route_encoded'] = le.transform(df['route'])

# Train model
model = LinearRegression()
features = df[['capacity', 'ticket_price (IN USD)', 'route_encoded']]
target = df['no_show_rate']
model.fit(features, target)

# UI
st.title("✈️ Airline Overbooking Optimization")
st.markdown("Predict no-show rate, optimize overbooking, and maximize revenue.")

origin = st.text_input("Enter Origin Airport Code (e.g., DEL)", max_chars=3)
destination = st.text_input("Enter Destination Airport Code (e.g., DXB)", max_chars=3)
capacity = st.number_input("Enter Flight Capacity", min_value=1, value=620)
ticket_price = st.number_input("Enter Ticket Price (in ₹)", min_value=1000, value=30000)

if st.button("Predict & Optimize"):
    route = origin.upper() + " -> " + destination.upper()
    try:
        input_route_encoded = le.transform([route])[0]

        new_data = pd.DataFrame([[capacity, ticket_price, input_route_encoded]],
                                columns=['capacity', 'ticket_price (IN USD)', 'route_encoded'])
        predicted_noshow = model.predict(new_data)[0]
        st.success(f"📉 Predicted No-Show Rate: {predicted_noshow:.2f}%")

        # Safe overbooking
        safe_extra = int(capacity / (1 - 0.9 * (predicted_noshow / 100)) - capacity)
        st.info(f"✅ Safe Overbooking Margin: +{safe_extra} seats (90% buffer)")

        # Simulation
        SIMULATIONS = 1000
        denied_boarding_cost = 2 * ticket_price
        max_profit = -float('inf')
        best_extra = 0

        for extra in range(0, 100):
            profits = []
            for _ in range(SIMULATIONS):
                actual_noshow_rate = np.random.normal(predicted_noshow, 1.0) / 100
                actual_showup = int((capacity + extra) * (1 - actual_noshow_rate))
                if actual_showup <= capacity:
                    profit = (capacity + extra) * ticket_price
                else:
                    denied = actual_showup - capacity
                    profit = (capacity + extra) * ticket_price - denied * denied_boarding_cost
                profits.append(profit)

            avg_profit = np.mean(profits)
            if avg_profit > max_profit:
                max_profit = avg_profit
                best_extra = extra

        st.success(f"🔺 Optimal Overbooking Point: +{best_extra} seats")
        st.success(f"💰 Estimated Max Profit: ₹{int(max_profit):,}")

    except ValueError:
        st.error("❌ Route not found in training data. Try a valid route like DEL -> DXB.")
