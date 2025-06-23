import random

# Simulate overbooking for one flight route
capacity = 650
predicted_noshow = 7.5  # You can update this with your model output
buffer = 0.9

tickets_sold = int(capacity / (1 - buffer * predicted_noshow / 100))

denied_boarding = 0
total_empty_seats = 0

for _ in range(10000):
    # Simulate no-show % with Gaussian noise (mean = predicted, std = 1%)
    actual_noshow = random.gauss(predicted_noshow, 1.0)
    actual_showup = tickets_sold * (1 - actual_noshow / 100)

    if actual_showup > capacity:
        denied_boarding += 1
    else:
        total_empty_seats += capacity - actual_showup

print(f"\n📊 Overbooking Simulation Results (10,000 flights):")
print(f"➤ Denied Boarding Cases: {denied_boarding}")
print(f"➤ Avg Empty Seats: {total_empty_seats / 10000:.2f}")
