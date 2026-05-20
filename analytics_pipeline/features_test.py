import numpy as np
import pandas as pd

def run_feature_engineering(clean_df):
    """
    Executes advanced feature engineering on the cleaned real estate dataset.
    Adds derived business metrics, localized price tiers, and structural dimensions.
    """
    # Work on a copy to protect the clean dataset state
    df = clean_df.copy()
    print("✨ Starting Feature Engineering Phase...")
    
    # ----------------------------------------------------
    # 1. Price per Square Meter (Prix Métrique)
    # ----------------------------------------------------
    print("   ↳ 📐 Calculating price per square meter metrics...")
    df['prix_m2'] = df['prix'] / df['surface']
    
    # ----------------------------------------------------
    # 2. Estimated Property Age (Relative to current year 2026)
    # ----------------------------------------------------
    print("   ↳ 🏗️ Calculating estimated property age...")
    df['age_bien_estime'] = 2026 - df['annee_construction']
    
    # ----------------------------------------------------
    # 3. Time Dimensions (Calendar Table Mapping for Power BI)
    # ----------------------------------------------------
    print("   ↳ 📅 Deconstructing publication timestamps...")
    df['annee_publication'] = df['date_publication'].dt.year
    df['mois_publication'] = df['date_publication'].dt.month
    df['trimestre_publication'] = df['date_publication'].dt.quarter
    df['nom_mois_publication'] = df['date_publication'].dt.strftime('%B')
    
    # ----------------------------------------------------
    # 4. FIXED: Size Categories (Matching Your Exact Rules)
    #    Small (< 80 m²), Medium (80-150 m²), Large (> 150 m²)
    # ----------------------------------------------------
    print("   ↳ 🏠 Engineering exact property size brackets...")
    surface_bins = [0, 80, 150, np.inf]
    surface_labels = ['Petit (< 80 m²)', 'Moyen (80-150 m²)', 'Grand (> 150 m²)']
    df['categorie_surface'] = pd.cut(df['surface'], bins=surface_bins, labels=surface_labels, right=False)
    
    # ----------------------------------------------------
    # 5. ADDED: Price Categories (Economy, Medium, High Standard, Luxury)
    #    Uses group-aware quartiles so a 'luxury apartment' price threshold
    #    is calculated separately from a 'luxury villa' price threshold.
    # ----------------------------------------------------
    print("   ↳ 💎 Creating group-aware market price segments...")
    def _determine_price_tier(group):
        q1 = group.quantile(0.25)
        q2 = group.quantile(0.50)
        q3 = group.quantile(0.75)
        
        conditions = [
            group < q1,
            (group >= q1) & (group < q2),
            (group >= q2) & (group < q3),
            group >= q3
        ]
        choices = ['Economy', 'Medium', 'High standard', 'Luxury']
        return np.select(conditions, choices, default='Medium')

    df['categorie_prix'] = df.groupby('type_bien')['prix'].transform(_determine_price_tier)
    
    # ----------------------------------------------------
    # 6. Market Segmentation (Translating Outlier Flags)
    # ----------------------------------------------------
    print("   ↳ 🏷️ Generating market exception tags...")
    if 'est_outlier' in df.columns:
        df['segment_marche'] = np.where(df['est_outlier'], 'Exception (Luxury/Grand)', 'Market Standard')
        df = df.drop(columns=['est_outlier'])
    else:
        df['segment_marche'] = 'Market Standard'
        
    print(f"✅ Feature engineering complete! Matrix shape with all new attributes: {df.shape}")
    return df