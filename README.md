
# ------- Airline Overbooking Optimization Tool ---------- #

A data-driven tool to help airlines **maximize revenue** by safely overbooking flights based on predicted no-show rates using machine learning and simulation techniques.

---

## Project Structure

```bash
FlightOverbookingTool/
├── Data/
│   └── MOCK_DATA.xlsx              # Synthetic dataset of flights
├── notebooks/
│   ├── eda_airline.py              # Phase 1–3: EDA and ML model
│   ├── optimize_overbooking.py     # Phase 4–5: Safe overbooking calc
│   ├── optimal_overbooking.py      # Phase 6: Simulation-based max profit
│   ├── simulate_overbooking.py     # 10k run simulation (bonus check)
├── Output/
│   ├── Optimized_Overbooking_Output.xlsx   # Ticket plan per route
│   ├── Route_Risk_Summary.xlsx             # Risk vs reward analysis
├── Visuals/
│   └── Figure_1.png               # Graph of profit vs extra tickets
├── combine_result.py              #  Combined CLI pipeline
├── overbooking_app.py             #  Streamlit Web App
└── README.md                      #  You're reading this!
```

---

##  What It Does

->>  Predicts **no-show rate** based on:
- Route
- Ticket price
- Capacity

->> Computes:
- Safe number of tickets to **overbook**
- Route-wise **extra revenue**
- Optimal overbooking point using **Monte Carlo simulation**

->> Outputs:
- **MAE / RMSE**
- **Overbooking margin**
- **Maximized net revenue**

---

##  Inputs Required

-  **Route**: e.g. `"DEL -> DXB"`
-  **Flight Capacity**: e.g. `620`
-  **Ticket Price**: e.g. `30000`

---

##  How to Run

### 1. Run from Terminal as Output form 

```bash
python combine_result.py
```

You'll be prompted to enter:
- Origin
- Destination
- Capacity
- Ticket price

### 2. Run as Web App from 

```bash
streamlit run overbooking_app.py
```

A browser UI will open for easy interaction.

---

##  Sample Output

```
Predicted No-Show Rate: 7.44%
Safe Overbooking (buffered): +53 tickets
Optimal Overbooking: +61 tickets
Estimated Max Profit: ₹1,835,200
```

---

##  Techniques Used

-  **Linear Regression** (sklearn)
-  **Monte Carlo Simulation** (1000 trials)
-  **EDA & Risk Analysis**
-  **Profit Curve Visualization** (matplotlib)

---

##  Tech Stack

- Python 
- Pandas, NumPy
- scikit-learn
- Matplotlib
- Streamlit (for Web UI)
- Mockaroo (for generate dataset) 
---

## 🔮 Future Improvements

- Use **XGBoost or RandomForest** for improved prediction
- Integrate with **real-world API** for live route/ticket data
- Build REST API with **FastAPI** for airline backend integration

---

##  Author

**Karan Kumar** 


##  License

MIT License – Free to use, modify, and share.
