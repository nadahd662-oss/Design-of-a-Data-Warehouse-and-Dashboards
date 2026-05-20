import os
import pandas as pd

# 🎯 UPDATED PATHS: Pointing to your new folder name packages
from analytics_pipeline.staging_test import run_staging
from analytics_pipeline.cleaning_test import run_data_cleaning  # Adjusted for cleaning_test.py
from analytics_pipeline.features_test import run_feature_engineering

# 🎯 UPDATED PATH: Pointing to your renamed warehouse folder package
from warehouse_modeling.bi_schema import load_star_schema

if __name__ == "__main__":
    print("🚀 Running the complete automated end-to-end pipeline...")
    
    # 1. Extraction Layer (Staging)
    df_raw = run_staging()
    
    # 2. Transformation Layer (Cleaning)
    df_clean = run_data_cleaning(df_raw)
    
    # 3. Optimization Layer (Feature Engineering)
    df_features = run_feature_engineering(df_clean)
    
    # 4. Save flat data backup for safety
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    output_dir = os.path.join(project_root, "data")
    final_path = os.path.join(output_dir, "listings_features.csv")
    df_features.to_csv(final_path, index=False, encoding='utf-8')
    print(f"💾 Flat file features matrix saved to local cache.")
    
    # 5. Load Layer (Dimensional Modeling into pgAdmin Warehouse schema)
    load_star_schema(df_features)
    
    print("\n🎉 ALL PHASES COMPLETED SUCCESSFULLY! Your Star Schema is live and optimized for Power BI.")