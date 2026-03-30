# 🚀 Phase 2 – Inventory Intelligence & Purchase Order Decision System

## 📌 Overview

Phase 2 focuses on transforming forecasting insights into a **decision-driven inventory management system**.

Unlike Phase 1, which provided analytical insights, Phase 2 introduces a **business logic layer** that enables automated procurement decisions through purchase order (PO) generation.

---

## 🎯 Objectives

* Convert demand forecasts into actionable decisions
* Optimize inventory levels
* Prevent stock-outs and overstocking
* Automate purchase order (PO) recommendations
* Build a scalable system for real-world deployment

---

## 🧠 Core Concept

Phase 2 shifts the system from:

```text id="shift1"
Forecast → Insight
```

to:

```text id="shift2"
Forecast → Inventory Logic → PO → Decision
```

---

## 🏗️ System Architecture

```text id="p2flow"
Sales Data → Forecast Engine → Inventory Analysis → Decision Engine → PO Generation
```

---

## 🔄 Workflow

```text id="p2workflow"
Input Data → Forecast → Reorder Check → Safety Stock → PO Calculation → Final Decision
```

---

## 📊 Key Components

---

### 🔹 1. Item-wise Demand Forecasting

* Forecast demand for each item independently
* Uses weighted moving average approach
* Adapts to latest data using sliding window

#### Formula:

[
\hat{D} = 0.5D_n + 0.3D_{n-1} + 0.2D_{n-2}
]

---

### 🔹 2. Reorder Level Calculation

Ensures timely replenishment based on demand rate.

#### Formula:

[
D_d = \frac{D_m}{30}
]

[
R = D_d \times 7
]

---

### 🔹 3. Safety Stock

Maintains buffer to handle demand uncertainty.

#### Formula:

[
SS = 0.2 \times D_m
]

---

### 🔹 4. Purchase Order (PO) Generation

Determines optimal order quantity.

#### Formula:

[
Q = \max(0,\ (D_m + SS) - S)
]

---

### 🔹 5. Decision Engine

Final business logic for procurement:

* If stock ≤ reorder level → **Generate PO**
* If demand ≈ 0 → **No Order (Non-moving)**
* Else → **Stock is sufficient**

---

## ⚠️ Advanced Inventory Considerations (Designed)

The system design includes handling of real-world constraints:

* Near-expiry stock detection
* Batch-level tracking
* Complaint batch exclusion
* Batch exchange handling
* Non-moving stock identification

👉 These features are part of the **system design and planned enhancements**.

---

## ⚡ Implementation Status

* Core logic implemented (forecast + PO calculation)
* Basic working script available (`main.py`)
* Modular pipeline design completed
* Full automation and UI under development

---

## 📁 Module Structure

```text id="p2structure"
phase2_system/

├── main.py           # Core logic implementation
├── pipeline/         # Planned ETL pipeline
├── models/           # Forecasting models
├── app/              # Planned web dashboard
├── utils/            # Helper functions
```

---

## 💡 Example Output

```text id="p2example"
Item: Drug A
Stock: 600
Forecast: 3000

Reorder Level: 700
PO Quantity: 3000

Status: 🔴 Order Required
```

---

## 🧠 Key Insights

* Forecast alone is not sufficient for decision-making
* Inventory logic is critical for real-world systems
* Combining forecasting with business rules enables automation
* Simple models + strong logic can outperform complex systems

---

## 🔄 Integration with Phase 1

Phase 2 builds on Phase 1 outputs:

* Uses forecast data from Phase 1
* Enhances system with decision-making capability
* Bridges gap between analytics and operations

---

## 🚀 Future Enhancements

* Real-time data ingestion from database
* Automated pipeline execution (cron/jobs)
* Web-based dashboard (Streamlit)
* Cloud deployment
* Multi-location inventory optimization

---

## 🏆 Outcome

Phase 2 transforms the system into:

> 💼 **A practical decision-support system for healthcare inventory management**

It demonstrates the ability to move beyond analytics and build **business-ready solutions**.
