import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükle
load_dotenv()

def get_db_connection():
    """
    Veritabanı bağlantısı oluşturur (Engine).
    Bağlantı bilgilerini çevre değişkenlerinden (environment variables) alır.
    """
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "password")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "postgres")

    # PostgreSQL bağlantı cümlesi (connection string)
    db_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    
    engine = create_engine(db_url)
    return engine