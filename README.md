# healthcare-inventory-system
# 🏥 Healthcare Inventory Optimization & Purchase Order System

## 📌 Overview

This project demonstrates the evolution of a healthcare data system into a **decision-driven inventory management solution**.

It is built in two phases:

* **Phase 1:** Analytics and forecasting prototype
* **Phase 2:** Inventory intelligence and purchase order (PO) decision system

The goal is to move from **data insights → actionable business decisions**.

---

## 🚀 Project Evolution

---

### 🟢 Phase 1 – Prototype (Analytics & Forecasting)

This phase focuses on understanding the data and generating insights.

**Key Components:**

* Python-based ETL pipeline
* SQLite database
* Power BI dashboards
* SARIMA forecasting model (~5% MAPE)
* Trend analysis and SKU performance
* Forecast validation (walk-forward, residual analysis)

**Outcome:**

* Provided visibility into sales trends and demand patterns
* Generated accurate forecasts
* Delivered analytical dashboards

---

### 🔥 Phase 2 – Inventory Decision System (Design + Partial Implementation)

This phase transforms forecasting into **real-world procurement decisions**.

**Designed Features:**

* Item-wise demand forecasting
* Reorder level calculation (7-day rule)
* Safety stock logic
* Automated purchase order (PO) generation
* Inventory decision engine

**Implementation Status:**

* Core mathematical logic implemented
* Basic working script available
* Full pipeline and UI planned

---

## 🔄 System Workflow

```text
Sales Data → Forecast → Inventory Analysis → PO Generation → Decision Output
```

---

## 🧠 Core Logic

---

### 🔹 Forecasting (Weighted Moving Average)

[
\hat{D} = 0.5D_n + 0.3D_{n-1} + 0.2D_{n-2}
]

---

### 🔹 Daily Demand

[
D_d = \frac{D_m}{30}
]

---

### 🔹 Reorder Level (7-Day Rule)

[
R = D_d \times 7
]

---

### 🔹 Safety Stock

[
SS = 0.2 \times D_m
]

---

### 🔹 Order Quantity

[
Q = \max(0,\ (D_m + SS) - S)
]

---

### 🔹 Decision Rule

* If stock ≤ reorder level → **Generate PO**
* If demand ≈ 0 → **No Order (Non-moving)**
* Else → **Stock is safe**

---

## 📊 Example Output

```text
Item: Paracetamol
Current Stock: 600
Forecast: 3000

Reorder Level: 700
Suggested Order: 3000 units
Status: 🔴 Reorder Required
```

---



---

## ⚙️ Technologies Used

* Python
* Pandas / NumPy
* Statsmodels (SARIMA)
* Scikit-learn
* SQLite
* Power BI

---

## ⚡ Key Highlights

* Transition from **forecasting → decision system**
* Real-world inventory logic implementation
* Reorder level and PO automation
* Designed for scalability to large datasets

---

## 🔐 Data Privacy Notice

Due to confidentiality and data protection policies, real healthcare data is not included in this repository.

This project contains:

* Code implementation
* System design
* Sample/mock data (where applicable)

The system is designed to work with real-world datasets in a secure environment.

---

## 📈 Future Enhancements

* Daily-level forecasting (if data available)
* Deep learning models (LSTM)
* Web-based dashboard (Streamlit)
* Cloud deployment (AWS/GCP)
* Multi-location inventory support

---

## 👨‍💻 Author

Alan Stephen


---

## ⭐ Final Note

This project demonstrates how data science can be extended beyond prediction to build a **practical, decision-support system** for real-world healthcare inventory management.
