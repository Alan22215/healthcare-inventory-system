import pandas as pd
import sqlite3
import os

# ---------------- SETTINGS ----------------
folder_path = r"C:\backups alan\Sales_Project\Monthly_Data"
database_path = r"C:\backups alan\Sales_Project\sales_database.db"

main_table = "consolidated_sales"
log_table = "loaded_files"
# ------------------------------------------

conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Create log table
cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {log_table} (
    file_name TEXT PRIMARY KEY
)
""")
conn.commit()

loaded_files = pd.read_sql(
    f"SELECT file_name FROM {log_table}", conn
)["file_name"].tolist()

# -------- MAP VALUE DICTIONARY --------
map_dict = {
    "IP Issue(Sales Consumption)": "S",
    "Pharmacy IP Issue": "S",
    "ER Issue(Sales Consumption)": "S",
    "Pharmacy Sales": "S",
    "Pharmacy IP Return": "R",
    "OP Consumption": "C",
    "Pharmacy Return": "R",
    "Store Consumption": "C",
    "Pharmacy Emergency Issue": "S",
    "IP Issue(Sales Consumption Return)": "R",
    "Pharmacy Emergency Return": "R",
    "IP Issue(Sales Consumption Return) ": "R"
}

print("Files found:", os.listdir(folder_path))

# -------- PROCESS FILES --------
for file in os.listdir(folder_path):

    if file.endswith(".xlsx") and file not in loaded_files:

        print(f"Processing: {file}")

        file_path = os.path.join(folder_path, file)

        # ✅ READ EVERYTHING AS STRING
        df = pd.read_excel(file_path, dtype=str)

        # Clean column names
        df.columns = df.columns.str.strip()

        # ---------- CONVERT ONLY REQUIRED NUMERIC COLUMNS ----------
        numeric_cols = [
            "Quantity",
            "PRate",
            "CGST",
            "SGST",
            "IGST",
            "SellingPrice"
        ]

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Remove negative quantity
        df["Quantity"] = df["Quantity"].abs()

        # MAP VALUE
        df["MAP_Value"] = df["Transaction Type"].map(map_dict)

        # RATE WITH GST
        df["Rate_WGST"] = df["PRate"] + (
            (df["CGST"] + df["SGST"] + df["IGST"]) /
            df["Quantity"].replace(0, 1)
        )

        # AMOUNT
        df["Amount"] = df["Rate_WGST"] * df["Quantity"]

        # SELLING AMOUNT
        df["Selling_Amount"] = df["SellingPrice"] * df["Quantity"]

        # HANDLE RETURNS
        df.loc[df["MAP_Value"] == "R", "Selling_Amount"] *= -1

        # Track source file
        df["Source_File"] = file

        # SAVE TO DATABASE
        df.to_sql(
            main_table,
            conn,
            if_exists="append",
            index=False
        )
                # ---- FINAL SAFETY FIX FOR SQLITE ----
        # convert very large numeric columns to string
        for col in df.columns:
            if df[col].dtype in ["int64", "float64"]:
                try:
                    if df[col].max() > 9_000_000_000_000_000:
                        df[col] = df[col].astype(str)
                except:
                    pass


        cursor.execute(
            f"INSERT INTO {log_table} VALUES (?)",
            (file,)
        )
        conn.commit()
    

print("✅ Data loaded and transformed successfully.")

conn.close()
