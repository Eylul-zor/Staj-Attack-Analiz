# ==============================
# ATTACK LOG ANALYSIS
# ==============================

import pandas as pd
from sqlalchemy import create_engine

# ------------------------------
# 1. VERİTABANI BAĞLANTISI
# ------------------------------
engine = create_engine(
    "postgresql://eluluser:q1w2e3r4t5@localhost:5433/eluldb"
)

# ------------------------------
# 2. VERİYİ ÇEK
# ------------------------------
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

df = pd.read_sql(query, engine)

print("Veri yüklendi.")
print("Boyut:", df.shape)
print(df.head())

# ------------------------------
# 3. VERİ TEMİZLEME / STANDARDİZASYON
# ------------------------------
# Attack kolonunu standart hale getir
df['attack'] = (
    df['attack']
    .astype(str)
    .str.strip()
    .str.upper()
)

# Zaman kolonunu datetime yap
df['created_at'] = pd.to_datetime(df['created_at'])

print("\nAttack kolonundaki değerler:")
print(df['attack'].value_counts())

# ------------------------------
# 4. ANALİZ 1: ATTACK ORANI
# ------------------------------
attack_ratio = (df['attack'] == 'ATTACK').mean()

print("\n--- ATTACK ORANI ---")
print(f"Attack oranı: {attack_ratio:.4f} (%{attack_ratio*100:.2f})")

# ------------------------------
# 5. ANALİZ 2: ATTACK TÜRLERİ (CATEGORY)
# ------------------------------
df_attack = df[df['attack'] == 'ATTACK'].copy()

# Category temizleme
df_attack['category_clean'] = (
    df_attack['category']
    .astype(str)
    .str.replace('{', '', regex=False)
    .str.replace('}', '', regex=False)
    .str.replace('"', '', regex=False)
)

# Çoklu category'leri ayır
attack_types = (
    df_attack['category_clean']
    .str.split(',')
    .explode()
    .str.strip()
)

attack_type_counts = attack_types.value_counts()
attack_type_ratio = attack_type_counts / attack_type_counts.sum()

print("\n--- ATTACK TÜRLERİ (ADET) ---")
print(attack_type_counts)

print("\n--- ATTACK TÜRLERİ (ORAN %) ---")
print((attack_type_ratio * 100).round(2))

# ------------------------------
# 6. ANALİZ 3: ZAMAN DAVRANIŞI (SAATLİK)
# ------------------------------
df_attack['hour'] = df_attack['created_at'].dt.hour

hourly_attacks = df_attack.groupby('hour').size()

print("\n--- SAATLİK ATTACK DAĞILIMI ---")
print(hourly_attacks)

# ------------------------------
# 7. ANALİZ 4: ROUTE / ENDPOINT RİSK ANALİZİ
# ------------------------------
route_risk = (
    df.groupby('route')
    .agg(
        total_requests=('attack', 'count'),
        attack_count=('attack', lambda x: (x == 'ATTACK').sum())
    )
)

route_risk['risk_score'] = (
    route_risk['attack_count'] /
    route_risk['total_requests']
)

route_risk = route_risk.sort_values('risk_score', ascending=False)

print("\n--- ROUTE RİSK ANALİZİ (TOP 10) ---")
print(route_risk.head(10))

# ------------------------------
# 8. ANALİZ 5: HTTP METHOD vs ATTACK
# ------------------------------
method_risk = (
    df.groupby('http_method')['attack']
    .apply(lambda x: (x == 'ATTACK').mean())
    .sort_values(ascending=False)
)

print("\n--- HTTP METHOD RİSK ORANLARI ---")
print((method_risk * 100).round(2))

# ------------------------------
# 9. ANALİZ 6: RESPONSE TIME KARŞILAŞTIRMASI
# ------------------------------
response_time_analysis = df.groupby('attack')['responsetime'].mean()

print("\n--- RESPONSE TIME ORTALAMALARI ---")
print(response_time_analysis)

# ------------------------------
# 10. ÖZET
# ------------------------------
print("\n=== ANALİZ TAMAMLANDI ===")
print(f"Toplam kayıt: {len(df)}")
print(f"Attack sayısı: {(df['attack'] == 'ATTACK').sum()}")
print(f"Attack oranı: %{attack_ratio*100:.2f}")
