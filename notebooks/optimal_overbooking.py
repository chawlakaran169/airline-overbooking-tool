import matplotlib.pyplot as plt
import numpy as np
import random

# ------------ Step 1: Simulate Net Profit by Overbooking Amount ------------

def simulate_net_profit(capacity, predicted_noshow, ticket_price, denied_boarding_cost, trials=1000):
    overbook_range = range(0, 100)  # test 0 to 99 extra tickets
    profits = []

    for extra_seats in overbook_range:
        total_profit = 0
        tickets_sold = capacity + extra_seats

        for _ in range(trials):
            # Simulate no-show % with small randomness
            actual_noshow = random.gauss(predicted_noshow, 1.0)
            show_ups = tickets_sold * (1 - actual_noshow / 100)

            # Revenue capped at capacity
            revenue = min(show_ups, capacity) * ticket_price

            # Penalty for overcapacity
            penalty = max(0, show_ups - capacity) * denied_boarding_cost

            total_profit += revenue - penalty

        avg_profit = total_profit / trials
        profits.append(avg_profit)

    return overbook_range, profits

# ------------ Step 2: Run Simulation & Plot Result ------------

# Example flight
capacity = 650
predicted_noshow = 7.5  # can plug in model output here
ticket_price = 30000 
denied_boarding_cost = 40000

overbook_range, profits = simulate_net_profit(
    capacity, predicted_noshow, ticket_price, denied_boarding_cost
)

# Plotting the profit curve
plt.figure(figsize=(10,6))
plt.plot(overbook_range, profits, marker='o')
plt.axvline(np.argmax(profits), color='red', linestyle='--', label='Optimal Overbooking Point')
plt.title("Overbooking Seats vs Net Revenue")
plt.xlabel("Extra Tickets Sold (Overbooked Seats)")
plt.ylabel("Average Net Revenue (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Print optimal point
optimal_extra_seats = np.argmax(profits)
print(f"🔺 Optimal Overbooking Point: {optimal_extra_seats} extra seats")
