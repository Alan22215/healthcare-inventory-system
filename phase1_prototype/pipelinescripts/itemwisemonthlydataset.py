import sqlite3
import pandas as pd

# DATABASE PATH
db_path = r"C:\backups alan\Sales_Project\sales_database.db"

conn = sqlite3.connect(db_path)

# -------- READ DATA --------
query = """
SELECT
    Date,
    ItemName,
    MAP_Value,
    Amount,
    Selling_Amount,
    Quantity
FROM consolidated_sales
"""

df = pd.read_sql(query, conn)

# -------- DATE FIX (IMPORTANT) --------
df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce",
    dayfirst=True,
    format="mixed"
)

print("Invalid Date Rows :", df["Date"].isna().sum())

# Remove bad rows if any
df = df.dropna(subset=["Date"])

# -------- MONTH COLUMN --------
df["YearMonth"] = df["Date"].dt.to_period("M")

# -------- SALES --------
sales = (
    df[df["MAP_Value"] == "S"]
    .groupby(["YearMonth", "ItemName"])["Selling_Amount"]
    .sum()
)

# -------- RETURNS --------
returns = (
    df[df["MAP_Value"] == "R"]
    .groupby(["YearMonth", "ItemName"])["Selling_Amount"]
    .sum()
)

# -------- COGS --------
cogs = (
    df[df["MAP_Value"] == "S"]
    .groupby(["YearMonth", "ItemName"])["Amount"]
    .sum()
)

# -------- QUANTITY --------
qty = (
    df.groupby(["YearMonth", "ItemName"])["Quantity"]
    .sum()
)

# -------- COMBINE --------
monthly_item_df = pd.DataFrame({
    "Net_Sales": sales,
    "Returns": returns,
    "Net_COGS": cogs,
    "Quantity": qty
}).fillna(0)

# -------- MARGIN --------
monthly_item_df["Margin"] = (
    monthly_item_df["Net_Sales"] -
    monthly_item_df["Net_COGS"]
)

# -------- FINAL FORMAT --------
monthly_item_df.reset_index(inplace=True)
monthly_item_df["Date"] = monthly_item_df["YearMonth"].dt.to_timestamp()
monthly_item_df.drop(columns=["YearMonth"], inplace=True)

monthly_item_df = monthly_item_df.sort_values(["ItemName", "Date"])

# -------- SAVE --------
monthly_item_df.to_sql(
    "monthly_item_sales",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("\n✅ Item-wise monthly dataset created successfully.")
