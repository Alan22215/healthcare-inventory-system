# 📊 Phase 1 – Automated MIS Reporting & Sales Forecasting (Prototype)

## 📌 Overview

Phase 1 focuses on building a **data analytics and forecasting prototype** for healthcare inventory data.

The objective was to transform raw transactional data into **meaningful insights, dashboards, and demand forecasts** to support decision-making.

---

## 🎯 Objectives

* Understand and process healthcare sales data
* Build automated MIS reporting system
* Analyze product-level performance
* Develop forecasting model for demand prediction
* Evaluate model accuracy and reliability

---

## 🗂️ Data Description

The system uses transactional healthcare data including:

* Item-wise sales consumption
* Patient-level billing data
* Batch and expiry information
* Cost and pricing details

### 📌 Data Characteristics

* High-volume transactional data
* Multiple product categories:

  * Drugs
  * Medical consumables
  * Generic miscellaneous items
* Time-series nature

---

## ⚙️ System Architecture

```text id="p1flow"
Raw Data → ETL Pipeline → SQLite Database → Power BI Dashboards → Forecast Model
```

---

## 🔄 Data Pipeline (ETL)

The ETL pipeline performs:

### 🔹 Data Extraction

* Load raw Excel-based reports
* Handle multiple monthly files

### 🔹 Data Transformation

* Data cleaning and preprocessing
* Handling missing values
* Standardizing formats
* Aggregating item-wise sales

### 🔹 Data Loading

* Store processed data in SQLite database

---

## 📊 Dashboards (Power BI)

Interactive dashboards were developed to provide insights:

### 🔹 1. Sales Performance Dashboard

* Net sales, cost, and margin analysis
* Monthly revenue trends
* Forecast vs actual comparison

---

### 🔹 2. Financial Trend Analysis

* Margin trends over time
* Rolling average analysis
* Profit stability indicators

---

### 🔹 3. SKU Analysis Dashboard

* Top revenue-generating products
* ABC classification
* Dependency and risk analysis

---

### 🔹 4. Forecast Intelligence Dashboard

* Model accuracy (MAPE)
* Walk-forward validation
* Bias tracking
* Model comparison

---

### 🔹 5. Forecast Performance Tracking

* Actual vs forecast visualization
* Confidence interval analysis
* Future projections

---

### 🔹 6. Residual Analysis

* Residual mean and variance
* Model diagnostic checks
* Error distribution over time

---

## 📈 Forecasting Model

### 🔹 Model Used:

* SARIMA (Seasonal AutoRegressive Integrated Moving Average)

---

### 🔹 Why SARIMA?

* Suitable for time-series data
* Handles seasonality and trends
* Works well with structured healthcare data

---

### 🔹 Model Evaluation

The model was evaluated using:

* **MAPE (Mean Absolute Percentage Error)**
* Walk-forward validation
* Residual diagnostics

---

### 🔹 Results

* Achieved ~4–5% MAPE
* Stable and consistent predictions
* Good performance across multiple products

---

## 📊 Key Insights

* Identified high-revenue and high-risk SKUs
* Detected seasonal demand patterns
* Provided visibility into profitability trends
* Highlighted model strengths and limitations

---

## ⚠️ Limitations

* Forecast output not directly linked to decision-making
* No inventory optimization logic
* No automated purchase order generation
* Limited to analytical insights

---

## 🔄 Transition to Phase 2

Phase 1 highlighted the need to move from:

```text id="p1shift"
Forecast → Insight
```

to:

```text id="p1shift2"
Forecast → Decision → Action
```

---

## 🚀 Outcome

Phase 1 successfully delivered:

* Automated reporting system
* Insightful dashboards
* Reliable forecasting model

This phase forms the **foundation for Phase 2**, where the system evolves into a **decision-support engine for inventory and procurement**.
