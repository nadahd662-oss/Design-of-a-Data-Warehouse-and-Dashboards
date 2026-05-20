import os
import pandas as pd
from sqlalchemy import create_engine

def get_db_connection():
    """Establishes an explicit connection engine to the Docker PostgreSQL container."""
    DB_USER = "postgres"
    DB_PASSWORD = "admin"       
    DB_HOST = "localhost"
    DB_PORT = "5439"            
    DB_NAME = "darkom_app"
    
    connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Crucial: Forces the system to talk via UTF-8, ignoring Windows path characters
    engine = create_engine(
        connection_string,
        connect_args={"client_encoding": "utf8"}
    )
    return engine

def run_staging():
    """
    Extracts raw real estate data from the database or raw CSV landing zone.
    Returns a raw pandas DataFrame.
    """
    print("📥 Starting Staging Phase: Extracting raw data...")
    
    # Option A: Extracting from your Docker Postgres setup
    try:
        engine = get_db_connection()
        query = 'SELECT * FROM "staging"."raw_listings";'
        df_raw = pd.read_sql(query, con=engine)
        print(f"✅ Staging complete! Extracted {len(df_raw)} rows from PostgreSQL.")
        return df_raw
    
    # Option B: Fallback to local raw CSV file if database is offline
    except Exception as e:
        print(f"⚠️ Database connection skipped ({e}). Falling back to local raw CSV file...")
        # Resolve path dynamically
        base_dir = os.getcwd()
        raw_path = os.path.join(base_dir, "data", "darkom-annonces.csv")
        return pd.read_csv(raw_path)