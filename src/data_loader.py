import pandas as pd
from .db import get_db_connection

def load_data():
    """
    Veritabanından log verilerini çeker.
    """
    engine = get_db_connection()
    
    query = """
    SELECT
        created_at,
        attack,
        category,
        route,
        http_method,
        http_status_code,
        responsetime,
        ip_address,
        country
    FROM logs;
    """
    
    print("Veritabanından veri çekiliyor...")
    df = pd.read_sql(query, engine)
    return df

def clean_data(df):
    """
    Veriyi temizler ve analiz için hazırlar.
    """
    print("Veri temizleniyor...")
    
    # 1. Attack kolonunu standartlaştır
    # Boşlukları sil, büyük harfe çevir
    df["attack"] = df["attack"].astype(str).str.strip().str.upper()
    
    # 2. Zaman kolonunu datetime formatına çevir
    df["created_at"] = pd.to_datetime(df["created_at"])
    
    # 3. Kategori temizleme (süslü parantez ve tırnakları kaldır)
    # Eğer category kolonu varsa temizle
    if "category" in df.columns:
        df["category_clean"] = (
            df["category"]
            .astype(str)
            .str.replace("{", "", regex=False)
            .str.replace("}", "", regex=False)
            .str.replace('"', "", regex=False)
        )
        
    return df