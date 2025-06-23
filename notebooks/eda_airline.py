import pandas as pd
df = pd.read_excel("../Data/MOCK_DATA.xlsx")

df['route'] = df['origin'] + ' -> ' + df['destination']
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['route_encoded'] = le.fit_transform(df['route'])

feature = df[['capacity', 'ticket_price (IN USD)', 'route_encoded']]
target = df['no_show_rate']

from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test = train_test_split(feature,target,test_size=0.2,random_state = 42)

from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train,y_train)

from sklearn.metrics import mean_absolute_error , mean_squared_error
import numpy as np
y_pred = model.predict(X_test)

mae = mean_squared_error(y_test,y_pred)
mse = mean_squared_error(y_test,y_pred)
rmse = np.sqrt(mse)

print(f"MAE : {mae:.4f}")
print(f"RMSE: {rmse:.4f}")

new_data = pd.DataFrame({
    'capacity' : [620],
    'ticket_price (IN USD)': [25000],
    'route_encoded':[le.transform(['DEL -> DXB'])[0]]
})

predicted_noshow = model.predict(new_data)
print(f"Predicted No-Show Rate : {predicted_noshow[0]:.2f}%")

