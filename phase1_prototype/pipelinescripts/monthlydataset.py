import sqlite3
import pandas as pd

# ---------------- DATABASE PATH ----------------
db_path = r"C:\backups alan\Sales_Project\sales_database.db"

# CONNECT DATABASE
conn = sqlite3.connect(db_path)

# ---------------- READ DATA ----------------
query = """
SELECT
    Date,
    MAP_Value,
    Amount,
    Selling_Amount,
    Quantity
FROM consolidated_sales
"""

df = pd.read_sql(query, conn)

# ---------------- DATE CONVERSION (IMPORTANT FIX) ----------------
df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce",
    dayfirst=True,
    format="mixed"
)

# CHECK IF ANY DATE FAILED
invalid_dates = df["Date"].isna().sum()
print("Invalid Date Rows :", invalid_dates)

# REMOVE INVALID DATE ROWS (SAFETY)
df = df.dropna(subset=["Date"])

# ---------------- CREATE MONTH COLUMN ----------------
df["YearMonth"] = df["Date"].dt.to_period("M")

# ---------------- SALES (MAP = S) ----------------
sales = (
    df[df["MAP_Value"] == "S"]
    .groupby("YearMonth")["Selling_Amount"]
    .sum()
)

# ---------------- RETURNS (MAP = R) ----------------
returns = (
    df[df["MAP_Value"] == "R"]
    .groupby("YearMonth")["Selling_Amount"]
    .sum()
)

# ---------------- COGS ----------------
cogs = (
    df[df["MAP_Value"] == "S"]
    .groupby("YearMonth")["Amount"]
    .sum()
)

# ---------------- QUANTITY ----------------
qty = (
    df.groupby("YearMonth")["Quantity"]
    .sum()
)

# ---------------- COMBINE DATA ----------------
monthly_df = pd.DataFrame({
    "Net_Sales": sales,
    "Returns": returns,
    "Net_COGS": cogs,
    "Quantity": qty
}).fillna(0)

# ---------------- MARGIN ----------------
monthly_df["Margin"] = (
    monthly_df["Net_Sales"] -
    monthly_df["Net_COGS"]
)

# ---------------- FINAL FORMAT ----------------
monthly_df.reset_index(inplace=True)

monthly_df["Date"] = monthly_df["YearMonth"].dt.to_timestamp()
monthly_df.drop(columns=["YearMonth"], inplace=True)

# SORT BY DATE
monthly_df = monthly_df.sort_values("Date")

# ---------------- SAVE TO DATABASE ----------------
monthly_df.to_sql(
    "monthly_drug_sales",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("\n✅ Monthly dataset created successfully.")
