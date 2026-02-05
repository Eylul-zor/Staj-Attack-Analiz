# ==============================
# ATTACK LOG VISUALIZATION
# ==============================
# Analiz sonuçlarını görselleştirir
# ve grafikleri output/ klasörüne kaydeder
# ==============================

import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# ------------------------------
# 1. OUTPUT KLASÖRÜ (EN ÜSTTE!)
# ------------------------------
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------
# 2. VERİTABANI BAĞLANTISI
# ------------------------------
engine = create_engine(
    "postgresql://eluluser:q1w2e3r4t5@localhost:5433/eluldb"
)

# ------------------------------
# 3. VERİYİ YÜKLE
# ------------------------------
query = """
SELECT
    created_at,
    attack,
    category,
    route,
    http_method
FROM logs;
"""

df = pd.read_sql(query, engine)

# ------------------------------
# 4. VERİ TEMİZLEME
# ------------------------------
df['attack'] = (
    df['attack']
    .astype(str)
    .str.strip()
    .str.upper()
)

df['created_at'] = pd.to_datetime(df['created_at'])

df_attack = df[df['attack'] == 'ATTACK'].copy()

# ------------------------------
# 5. GRAFİK 1: ATTACK TÜRLERİ
# ------------------------------
df_attack['category_clean'] = (
    df_attack['category']
    .astype(str)
    .str.replace('{', '', regex=False)
    .str.replace('}', '', regex=False)
    .str.replace('"', '', regex=False)
)

attack_types = (
    df_attack['category_clean']
    .str.split(',')
    .explode()
    .str.strip()
)

attack_type_counts = attack_types.value_counts()

plt.figure()
attack_type_counts.plot(kind='bar')
plt.title("Attack Türlerinin Dağılımı")
plt.xlabel("Attack Türü")
plt.ylabel("Sayı")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/attack_types.png")
plt.close()

# ------------------------------
# 6. GRAFİK 2: SAATLİK ATTACK YOĞUNLUĞU
# ------------------------------
df_attack['hour'] = df_attack['created_at'].dt.hour
hourly_attacks = df_attack.groupby('hour').size()

plt.figure()
hourly_attacks.plot(kind='line', marker='o')
plt.title("Saatlik Attack Yoğunluğu")
plt.xlabel("Saat")
plt.ylabel("Attack Sayısı")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/hourly_attacks.png")
plt.close()

# ------------------------------
# 7. GRAFİK 3: HTTP METHOD vs ATTACK ORANI
# ------------------------------
method_risk = (
    df.groupby('http_method')['attack']
    .apply(lambda x: (x == 'ATTACK').mean())
)

plt.figure()
(method_risk * 100).plot(kind='bar')
plt.title("HTTP Method Bazlı Attack Oranı (%)")
plt.xlabel("HTTP Method")
plt.ylabel("Attack Oranı (%)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/method_risk.png")
plt.close()

# ------------------------------
# 8. TAMAMLANDI
# ------------------------------
print("Grafikler başarıyla oluşturuldu:")
print(f"- {OUTPUT_DIR}/attack_types.png")
print(f"- {OUTPUT_DIR}/hourly_attacks.png")
print(f"- {OUTPUT_DIR}/method_risk.png")


