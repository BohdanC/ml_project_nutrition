import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn import metrics
from sklearn.svm import SVC
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.ensemble import RandomForestRegressor

import warnings
warnings.filterwarnings('ignore')



df = pd.read_csv('combined_dataset.csv')
df.head()

df.replace({'male': 0, 'female': 1},
        inplace=True)
df.head()

features = df.drop(['User_ID', 'Calories'], axis=1)
target = df['Calories'].values

X_train, X_val, Y_train, Y_val = train_test_split(features, target,
                                                  test_size=0.2, random_state=2)
X_train.shape, X_val.shape

from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import r2_score

models = [LinearRegression(), XGBRegressor(), Lasso(), RandomForestRegressor(), Ridge()]

for model in models:
    model.fit(X_train, Y_train)
    model_name = str(model).split('(')[0]

    print(f'{model_name} : ')

    train_preds = model.predict(X_train)
    print('Training Error (MAE): ', mae(Y_train, train_preds))
    print('Training Error (MSE): ', mse(Y_train, train_preds))
    print('Training Error (RMSE): ', mse(Y_train, train_preds, squared=False))
    print('Training R-squared: ', r2_score(Y_train, train_preds))

    val_preds = model.predict(X_val)
    print('Validation Error (MAE): ', mae(Y_val, val_preds))
    print('Validation Error (MSE): ', mse(Y_val, val_preds))
    print('Validation Error (RMSE): ', mse(Y_val, val_preds, squared=False))
    print('Validation R-squared: ', r2_score(Y_val, val_preds))

    print()

xgb_model = models[1]
import numpy as np

# Приклад даних про тренування
data1 = [1, 20, 166, 60, 14, 94, 40.3]
data2 = [0, 68, 190, 94, 29, 105, 40.8]
# Перетворення даних у формат, що підходить для моделі
data1 = np.array(data1).reshape(1, -1)
print(data1)
data2 = np.array(data2).reshape(1, -1)
# Передбачення за допомогою моделі
predicted_calories1 = xgb_model.predict(data1)
predicted_calories2 = xgb_model.predict(data2)
print("Прогнозована кількість спалених калорій:", predicted_calories1[0])
print("Прогнозована кількість спалених калорій:", predicted_calories2[0])