import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text

def get_warehouse_engine():
    """Establishes connection parameters for your active Docker Postgres container."""
    return create_engine("postgresql://postgres:admin@localhost:5439/darkom_app")

def load_star_schema(df_features):
    """
    Transforms flat engineered data into a normalized Star Schema
    and pushes the tables straight to the 'Warehouse' database schema layer.
    """
    print("🏗️ Initiating Data Warehouse Dimensional Modeling...")
    engine = get_warehouse_engine()
    df = df_features.copy()
    
    # ----------------------------------------------------
    # Step 1: Create dim_time
    # ----------------------------------------------------
    print("   ↳ Building dim_time...")
    dim_time = df[[
        'date_publication', 'annee_publication', 'mois_publication', 
        'trimestre_publication', 'nom_mois_publication'
    ]].drop_duplicates().reset_index(drop=True)
    dim_time.index.name = 'id_date'
    dim_time = dim_time.reset_index()
    
    # ----------------------------------------------------
    # Step 2: Create dim_location
    # ----------------------------------------------------
    print("   ↳ Building dim_location...")
    dim_location = df[['ville', 'quartier']].drop_duplicates().reset_index(drop=True)
    dim_location.index.name = 'id_emplacement'
    dim_location = dim_location.reset_index()
    
    # ----------------------------------------------------
    # Step 3: Create dim_transaction
    # ----------------------------------------------------
    print("   ↳ Building dim_transaction...")
    dim_transaction = df[['transaction', 'categorie_prix', 'segment_marche']].drop_duplicates().reset_index(drop=True)
    dim_transaction.index.name = 'id_transaction'
    dim_transaction = dim_transaction.reset_index()
    
    # ----------------------------------------------------
    # Step 4: Create dim_bien
    # ----------------------------------------------------
    print("   ↳ Building dim_bien...")
    dim_bien = df[['type_bien', 'categorie_surface']].drop_duplicates().reset_index(drop=True)
    dim_bien.index.name = 'id_caracteristique'
    dim_bien = dim_bien.reset_index()
    
    # ----------------------------------------------------
    # Step 5: Assemble fact_annonces (Mapping Keys)
    # ----------------------------------------------------
    print("   ↳ Assembling fact_annonces metric layer...")
    fact_annonces = df.merge(dim_time, on=['date_publication', 'annee_publication', 'mois_publication', 'trimestre_publication', 'nom_mois_publication'], how='left')
    fact_annonces = fact_annonces.merge(dim_location, on=['ville', 'quartier'], how='left')
    fact_annonces = fact_annonces.merge(dim_transaction, on=['transaction', 'categorie_prix', 'segment_marche'], how='left')
    fact_annonces = fact_annonces.merge(dim_bien, on=['type_bien', 'categorie_surface'], how='left')
    
    fact_cols = [
        'id_date', 'id_emplacement', 'id_transaction', 'id_caracteristique',
        'prix', 'surface', 'prix_m2', 'nb_chambres', 'nb_salles_bain', 'etage', 'age_bien_estime'
    ]
    fact_annonces = fact_annonces[fact_cols]
    
    # ----------------------------------------------------
    # Step 6: Pushing Tables to PostgreSQL (Warehouse Schema)
    # ----------------------------------------------------
    schema_name = "Warehouse"
    tables = {
        "dim_time": dim_time,
        "dim_location": dim_location,
        "dim_transaction": dim_transaction,
        "dim_bien": dim_bien,
        "fact_annonces": fact_annonces
    }
    
    print(f"   ↳ Pushing star schema tables to Postgres schema: '{schema_name}'...")
    for table_name, table_df in tables.items():
        table_df.to_sql(
            name=table_name,
            con=engine,
            schema=schema_name,
            if_exists='replace',
            index=False
        )
        
    # ----------------------------------------------------
    # Step 7: Optimizing Key Columns & Setting Primary Keys (SQL)
    # ----------------------------------------------------
    print("   ↳ Optimizing table relationships and indexing Key Columns...")
    with engine.connect() as conn:
        # Enforce Primary Keys on Dimensions (Updated table names match Step 6 exactly)
        conn.execute(text(f'ALTER TABLE "{schema_name}"."dim_time" ADD PRIMARY KEY (id_date);'))
        conn.execute(text(f'ALTER TABLE "{schema_name}"."dim_location" ADD PRIMARY KEY (id_emplacement);'))
        conn.execute(text(f'ALTER TABLE "{schema_name}"."dim_transaction" ADD PRIMARY KEY (id_transaction);'))
        conn.execute(text(f'ALTER TABLE "{schema_name}"."dim_bien" ADD PRIMARY KEY (id_caracteristique);'))
        
        # Performance Indexing on Fact Foreign Keys
        conn.execute(text(f'CREATE INDEX idx_fact_date ON "{schema_name}"."fact_annonces"(id_date);'))
        conn.execute(text(f'CREATE INDEX idx_fact_emp ON "{schema_name}"."fact_annonces"(id_emplacement);'))
        conn.execute(text(f'CREATE INDEX idx_fact_trans ON "{schema_name}"."fact_annonces"(id_transaction);'))
        conn.execute(text(f'CREATE INDEX idx_fact_carac ON "{schema_name}"."fact_annonces"(id_caracteristique);'))
        conn.commit()
        
    print(f"✅ DATA WAREHOUSE MODELING COMPLETE! Star schema successfully locked inside schema: '{schema_name}'")