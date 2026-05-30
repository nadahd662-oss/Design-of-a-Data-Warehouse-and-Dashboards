# 🏠 Darkom Data Warehouse & Business Intelligence Project

## 📌 Project Overview

This project aims to build an end-to-end data pipeline for real estate market analysis using property listings from **Darkom.ma**, a Moroccan real estate platform.

The objective is to transform raw property advertisements into a structured and analysis-ready Data Warehouse that supports Business Intelligence reporting and interactive dashboards in Power BI.

The project follows a modern data architecture:

```text
CSV Source
    ↓
Staging Layer
    ↓
Clean Layer
    ↓
Data Warehouse (PostgreSQL)
    ↓
Power BI Dashboards
```

---

## 🎯 Objectives

* Import and store raw real estate data.
* Clean and standardize inconsistent records.
* Apply feature engineering techniques.
* Design a dimensional Data Warehouse.
* Build analytical dashboards in Power BI.
* Generate business insights about the Moroccan real estate market.

---

## 🛠️ Technologies Used

* Python
* Pandas
* PostgreSQL
* SQLAlchemy
* Power BI
* Power Query
* DAX

---

## 📂 Project Structure

```text
darkom-project/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── scripts/
│   ├── staging/
│   ├── cleaning/
│   ├── warehouse/
│
├── sql/
│   ├── staging_schema.sql
│   ├── warehouse_schema.sql
│
├── dashboards/
│
├── requirements.txt
│
└── README.md
```

---

## 📥 Data Source

Dataset: `darkom_annonces.csv`

### Available Attributes

| Column             | Description          |
| ------------------ | -------------------- |
| annonce_id         | Listing identifier   |
| date_publication   | Publication date     |
| titre              | Listing title        |
| ville              | Property city        |
| quartier           | Neighborhood         |
| type_bien          | Property type        |
| transaction        | Sale or Rental       |
| prix               | Property price (MAD) |
| surface            | Area (m²)            |
| nb_chambres        | Number of bedrooms   |
| nb_salles_bain     | Number of bathrooms  |
| etage              | Floor number         |
| annee_construction | Construction year    |

---

# ⚙️ ETL Pipeline

## 1. Staging Layer

The raw CSV file is loaded into PostgreSQL without modifications.

### Tasks

* Import CSV data
* Verify successful loading
* Log loading operations
* Preserve original source data

---

## 2. Clean Layer

Data quality improvements are applied.

### Data Cleaning

* Remove duplicates
* Handle missing values
* Correct data types
* Standardize city names
* Standardize property types
* Standardize transaction values

### Outlier Treatment

* Price
* Surface
* Number of bedrooms

---

## 3. Feature Engineering

Several analytical attributes are created:

### Price per Square Meter

```text
price_per_m2 = prix / surface
```

### Property Age

```text
property_age = current_year - annee_construction
```

### Price Categories

* Economic
* Medium
* High Standing
* Luxury

### Surface Categories

* Small (< 80 m²)
* Medium (80 - 150 m²)
* Large (> 150 m²)

### Time Dimensions

* Publication Year
* Publication Month
* Publication Quarter

---

# 🏗️ Data Warehouse Design

The warehouse is implemented inside the **bi_schema** PostgreSQL schema.

## Dimensional Model

### Fact Table

**fact_annonces**

Contains business metrics:

* Price
* Surface
* Bedrooms
* Bathrooms
* Price per m²

### Dimension Tables

#### dim_date

* Date
* Year
* Month
* Quarter

#### dim_location

* City
* Neighborhood

#### dim_property

* Property Type
* Transaction Type
* Surface Category
* Price Category

---

## Optimization

* Primary Keys
* Foreign Keys
* Indexes
* Referential Integrity Checks

---

# 📊 Power BI Dashboards

## Dashboard 1 — Market Overview

* Total Listings
* Average Price
* Average Surface
* Listings by City
* Listings by Property Type
* Sale vs Rental Distribution

---

## Dashboard 2 — Price Analysis

* Price Distribution
* Average Price per m²
* Price by Property Type
* Price Segment Analysis

---

## Dashboard 3 — Geographic Analysis

* Listings by City
* Average Price by City
* Top Neighborhoods
* Geographic Price Distribution

---

## Dashboard 4 — Market Trends

* Listing Growth Over Time
* Price Evolution
* Seasonal Analysis
* Period-over-Period Comparison

---

# 📈 Key DAX Measures

### Total Listings

```DAX
Total Listings = COUNT(fact_annonces[annonce_id])
```

### Average Price

```DAX
Average Price = AVERAGE(fact_annonces[prix])
```

### Average Price per m²

```DAX
Average Price m² = AVERAGE(fact_annonces[price_per_m2])
```

### Average Surface

```DAX
Average Surface = AVERAGE(fact_annonces[surface])
```

---

# 🔎 Interactive Filters

The dashboards support dynamic filtering by:

* City
* Neighborhood
* Property Type
* Transaction Type
* Price Range
* Surface Range
* Publication Period

All visualizations automatically update according to the selected filters.

---

# 🚀 Expected Outcomes

This project demonstrates the complete lifecycle of a Business Intelligence solution:

* Data Ingestion
* Data Cleaning
* Feature Engineering
* Data Warehousing
* Data Modeling
* Business Intelligence Reporting

The final solution provides decision-makers with reliable insights into the Moroccan real estate market.

---

## 👤 Author

**Nada EL HAIDARI**

Data Analyst Trainee | Educational Sciences Background | Business Intelligence & Data Engineering Enthusiast
