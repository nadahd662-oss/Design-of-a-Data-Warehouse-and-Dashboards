import numpy as np
import pandas as pd

# ==========================================
# 🛑 SUB-FUNCTION 1: Data Integrity
# ==========================================
def _remove_invalid_records(df):
    """Handles duplicates and missing critical business data."""
    # 1. Deduplicate
    initial_len = len(df)
    df = df.drop_duplicates()
    
    # 2. Drop rows missing non-negotiable data
    critical_cols = ['type_bien', 'transaction', 'date_publication']
    df = df.dropna(subset=critical_cols)
    
    print(f"   ↳ 📋 Data Integrity: Removed {initial_len - len(df)} bad/duplicate rows.")
    return df


# ==========================================
# 🛑 SUB-FUNCTION 2: Data Standardization & Imputation
# ==========================================
def _impute_missing_metrics(df):
    """Standardizes text strings and handles missing numerical metrics."""
    print("   ↳ 🔤 Harmonizing text and imputing structural features...")
    
    # 1. Text Standardizing
    for col in ['ville', 'type_bien', 'transaction']:
        df[col] = df[col].astype(str).str.strip().str.lower()
        
    df['quartier'] = df['quartier'].fillna('inconnu').astype(str).str.strip().str.lower()
    df['quartier'] = df['quartier'].replace(['nan', 'none', '', ' '], 'inconnu')
    
    # 2. Advanced Median Imputation
    impute_cols = ['nb_chambres', 'nb_salles_bain', 'etage', 'annee_construction']
    for col in impute_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # Localized context-aware median
        grouped_median = df.groupby(['ville', 'type_bien'])[col].transform('median')
        df[col] = df[col].fillna(grouped_median).fillna(df[col].median())
        
    df[impute_cols] = df[impute_cols].round().astype(int)
    return df


# ==========================================
# 🛑 SUB-FUNCTION 3: Outlier Processing Matrix Bounds
# ==========================================
def _detect_market_outliers(df):
    """Calculates statistical fences to flag anomalies without altering data integrity."""
    print("   ↳ 📈 Analyzing Grouped IQR mathematical outlier boundaries...")
    df['est_outlier'] = False
    
    # Convert core metrics to real numbers
    for col in ['prix', 'surface']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['prix', 'surface'])
    
    # Grouped IQR Loop
    for col in ['prix', 'surface']:
        Q1 = df.groupby('type_bien')[col].transform('quantile', 0.25)
        Q3 = df.groupby('type_bien')[col].transform('quantile', 0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        df['est_outlier'] = df['est_outlier'] | (df[col] < lower_bound) | (df[col] > upper_bound)
        
    return df


# ==========================================
# 🎯 THE MAIN MASTER FUNCTION (Called by main.py)
# ==========================================
def run_data_cleaning(raw_df):
    """
    The orchestrator function. It takes the raw data and channels it 
    through our interactive notebook blocks sequentially.
    """
    print("🧹 Starting Comprehensive Data Cleaning Phase...")
    df = raw_df.copy()
    
    # Call Sub-Function 1 (Interactive Block 1)
    df = _remove_invalid_records(df)
    
    # Explicit conversion of date type here to bridge the steps
    df['date_publication'] = pd.to_datetime(df['date_publication'], errors='coerce')
    df = df.dropna(subset=['date_publication'])
    
    # Call Sub-Function 2 (Interactive Block 2)
    df = _impute_missing_metrics(df)
    
    # Call Sub-Function 3 (Interactive Block 3)
    df = _detect_market_outliers(df)
    
    print(f"✅ Cleaning complete! Operational matrix shape: {df.shape}")
    return df