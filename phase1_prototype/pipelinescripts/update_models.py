import sqlite3
import pandas as pd
import numpy as np
from prophet import Prophet
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

# ======================================
# DATABASE CONNECTION
# ======================================

db_path = r"C:\backups alan\Sales_Project\sales_database.db"
conn = sqlite3.connect(db_path)

# ======================================
# LOAD DATA
# ======================================

query = """
SELECT Date, Net_Sales
FROM monthly_drug_sales
ORDER BY Date
"""

df = pd.read_sql(query, conn)

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna()
df = df.sort_values("Date")

if len(df) < 12:
    raise ValueError("Need at least 12 months of data.")

df.set_index("Date", inplace=True)

# Ensure continuous monthly frequency
df = df.resample("ME").sum()

# ======================================
# TRAIN / TEST SPLIT (80 / 20)
# ======================================

train_size = int(len(df) * 0.8)
train = df.iloc[:train_size]
test = df.iloc[train_size:]
y_true = test["Net_Sales"].values

# ======================================
# SAFE MAPE FUNCTION
# ======================================

def safe_mape(actual, predicted):
    actual = np.array(actual)
    predicted = np.array(predicted)
    return np.mean(
        np.abs((actual - predicted) / np.where(actual == 0, 1, actual))
    ) * 100

# =====================================================
# ===================== PROPHET =======================
# =====================================================

prophet_train = train.reset_index().rename(
    columns={"Date": "ds", "Net_Sales": "y"}
)

model_p = Prophet(
    yearly_seasonality=True,
    seasonality_mode="multiplicative",
    changepoint_prior_scale=0.15
)

model_p.fit(prophet_train)

future = model_p.make_future_dataframe(
    periods=len(test),
    freq="ME"
)

forecast_p = model_p.predict(future)
y_pred_p = forecast_p["yhat"].iloc[-len(test):].values

prophet_MAE = mean_absolute_error(y_true, y_pred_p)
prophet_RMSE = np.sqrt(mean_squared_error(y_true, y_pred_p))
prophet_MAPE = safe_mape(y_true, y_pred_p)

pd.DataFrame({
    "Model": ["Prophet"],
    "MAE": [prophet_MAE],
    "RMSE": [prophet_RMSE],
    "MAPE_Percentage": [prophet_MAPE]
}).to_sql("prophet_model_evaluation", conn, if_exists="replace", index=False)

# =====================================================
# ===================== SARIMA ========================
# =====================================================

model_s = SARIMAX(
    train["Net_Sales"],
    order=(1, 1, 1),
    enforce_stationarity=False,
    enforce_invertibility=False
)

fit_s = model_s.fit(disp=False)

forecast_s = fit_s.forecast(steps=len(test))
y_pred_s = forecast_s.values

sarima_MAE = mean_absolute_error(y_true, y_pred_s)
sarima_RMSE = np.sqrt(mean_squared_error(y_true, y_pred_s))
sarima_MAPE = safe_mape(y_true, y_pred_s)

pd.DataFrame({
    "Model": ["SARIMA"],
    "MAE": [sarima_MAE],
    "RMSE": [sarima_RMSE],
    "MAPE_Percentage": [sarima_MAPE]
}).to_sql("sarima_model_evaluation", conn, if_exists="replace", index=False)

# =====================================================
# ============ STORE SARIMA TEST RESIDUALS ============
# =====================================================

residuals = y_true - y_pred_s

residual_df = pd.DataFrame({
    "Date": test.index,
    "Actual": y_true,
    "Predicted": y_pred_s,
    "Residual": residuals
})

residual_df.to_sql(
    "sarima_residual_analysis",
    conn,
    if_exists="replace",
    index=False
)

# =====================================================
# ===================== NAIVE =========================
# =====================================================

naive_last_value = train["Net_Sales"].iloc[-1]
naive_predictions = np.repeat(naive_last_value, len(test))

naive_MAE = mean_absolute_error(y_true, naive_predictions)
naive_RMSE = np.sqrt(mean_squared_error(y_true, naive_predictions))
naive_MAPE = safe_mape(y_true, naive_predictions)

pd.DataFrame({
    "Model": ["Naive"],
    "MAE": [naive_MAE],
    "RMSE": [naive_RMSE],
    "MAPE_Percentage": [naive_MAPE]
}).to_sql("naive_model_evaluation", conn, if_exists="replace", index=False)

# =====================================================
# ============== WALK FORWARD VALIDATION ==============
# =====================================================

walk_mape = []
walk_residuals = []

for i in range(train_size, len(df) - 1):

    train_wf = df.iloc[:i]
    test_wf = df.iloc[i:i+1]

    model_wf = SARIMAX(
        train_wf["Net_Sales"],
        order=(1, 1, 1),
        enforce_stationarity=False,
        enforce_invertibility=False
    )

    fit_wf = model_wf.fit(disp=False)
    pred_wf = fit_wf.forecast(steps=1)

    actual = test_wf["Net_Sales"].values[0]
    predicted = pred_wf.values[0]

    mape_step = abs((actual - predicted) / (actual if actual != 0 else 1))
    walk_mape.append(mape_step)

    walk_residuals.append(actual - predicted)

walk_forward_mape = np.mean(walk_mape) * 100
bias_correction = np.mean(walk_residuals)

# =====================================================
# ============ FINAL 12M SARIMA FORECAST =============
# =====================================================

model_s_full = SARIMAX(
    df["Net_Sales"],
    order=(1, 1, 1),
    enforce_stationarity=False,
    enforce_invertibility=False
)

fit_s_full = model_s_full.fit(disp=False)

forecast_object = fit_s_full.get_forecast(steps=12)
future_s = forecast_object.predicted_mean
conf_int = forecast_object.conf_int()

future_s_corrected = future_s + bias_correction

future_dates = pd.date_range(
    start=df.index.max(),
    periods=13,
    freq="ME"
)[1:]

sarima_output = pd.DataFrame({
    "Date": future_dates,
    "Original_Forecast": future_s.values,
    "Lower_CI": conf_int.iloc[:, 0].values,
    "Upper_CI": conf_int.iloc[:, 1].values,
    "Bias_Adjustment": bias_correction,
    "Bias_Corrected_Forecast": future_s_corrected.values
})

sarima_output.to_sql(
    "sarima_forecast_12m",
    conn,
    if_exists="replace",
    index=False
)

# =====================================================
# ================ MODEL COMPARISON ===================
# =====================================================

comparison = pd.DataFrame({
    "Model": ["Prophet", "SARIMA", "Naive"],
    "MAPE_Percentage": [prophet_MAPE, sarima_MAPE, naive_MAPE],
    "RMSE": [prophet_RMSE, sarima_RMSE, naive_RMSE],
    "MAE": [prophet_MAE, sarima_MAE, naive_MAE]
})

comparison.to_sql("model_comparison", conn, if_exists="replace", index=False)

# =====================================================
# ========== STORE MODEL RUN SUMMARY ==================
# =====================================================

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS model_run_summary (
    run_date TEXT,
    model_name TEXT,
    mape_80_20 REAL,
    walk_forward_mape REAL,
    bias REAL,
    data_points INTEGER
)
""")

conn.commit()

data_points = len(df)
run_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cursor.execute("""
INSERT INTO model_run_summary
(run_date, model_name, mape_80_20, walk_forward_mape, bias, data_points)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    run_date,
    "SARIMA",
    sarima_MAPE,
    walk_forward_mape,
    bias_correction,
    data_points
))

conn.commit()
conn.close()

print("\n--------------------------------------------------")
print("INDUSTRIAL FORECAST PIPELINE COMPLETED")
print("--------------------------------------------------")
print(f"Prophet MAPE (80/20): {prophet_MAPE:.2f}%")
print(f"SARIMA  MAPE (80/20): {sarima_MAPE:.2f}%")
print(f"Naive   MAPE (80/20): {naive_MAPE:.2f}%")
print(f"SARIMA Walk-Forward MAPE: {walk_forward_mape:.2f}%")
print("--------------------------------------------------")