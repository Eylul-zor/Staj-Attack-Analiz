# ==============================
# ATTACK LOG VISUALIZATION
# ==============================
# Analiz sonuçlarını görselleştirir
# ve grafikleri output/ klasörüne kaydeder
# ==============================

import os
import matplotlib.pyplot as plt
import seaborn as sns
from data_loader import load_data, clean_data

# ------------------------------
# 1. OUTPUT KLASÖRÜ (EN ÜSTTE!)
# ------------------------------
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------
# 2. VERİYİ YÜKLE
# ------------------------------
df_raw = load_data()
df = clean_data(df_raw)


# ------------------------------
# 3. VERİ HAZIRLAMA (DF_ATTACK)
# ------------------------------
df_attack = df[df["attack"] == "ATTACK"].copy()

# ------------------------------
# 4. GRAFİK 1: ATTACK TÜRLERİ
# ------------------------------
# category_clean zaten clean_data fonksiyonunda halledildi
# yine de null kontrolü yapmak iyi olabilir ama junior style devam

# çoklu kategorileri ayır
attack_types = (
    df_attack["category_clean"]
    .str.split(",")
    .explode()
    .str.strip()
)

attack_type_counts = attack_types.value_counts()

plt.figure()
attack_type_counts.plot(kind="bar")
plt.title("Attack Türlerinin Dağılımı")
plt.xlabel("Attack Türü")
plt.ylabel("Sayı")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/attack_types.png")
plt.close()

# ------------------------------
# 5. GRAFİK 2: SAATLİK ATTACK YOĞUNLUĞU
# ------------------------------
df_attack["hour"] = df_attack["created_at"].dt.hour
hourly_attacks = df_attack.groupby("hour").size()

plt.figure()
hourly_attacks.plot(kind="line", marker="o")
plt.title("Saatlik Attack Yoğunluğu")
plt.xlabel("Saat")
plt.ylabel("Attack Sayısı")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/hourly_attacks.png")
plt.close()

# ------------------------------
# 6. GRAFİK 3: HTTP METHOD vs ATTACK ORANI
# ------------------------------
method_risk = (
    df.groupby("http_method")["attack"]
    .apply(lambda x: (x == "ATTACK").mean())
)

plt.figure()
(method_risk * 100).plot(kind="bar")
plt.title("HTTP Method Bazlı Attack Oranı (%)")
plt.xlabel("HTTP Method")
plt.ylabel("Attack Oranı (%)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/method_risk.png")
plt.close()

# ------------------------------
# 7. GRAFİK 4: RESPONSE TIME vs ATTACK (LOGARİTMİK)
# ------------------------------
plt.figure(figsize=(10, 6))

# Grafiği çiziyoruz
sns.boxplot(x="attack", y="responsetime", data=df, palette="Set2")


plt.yscale("log")

plt.title("Attack Durumuna Göre Response Time Dağılımı (Logaritmik Ölçek)")
plt.xlabel("İstek Durumu (NORMAL vs ATTACK)")
plt.ylabel("Response Time (ms) - Log Scale")
plt.grid(True, which="both", ls="-", alpha=0.2)  # Izgaraları logaritmik için açmak iyidir

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/response_time_comparison_log.png")
plt.close()


# ------------------------------
# 8. TAMAMLANDI
# ------------------------------
print("Grafikler başarıyla oluşturuldu:")
print(f"- {OUTPUT_DIR}/attack_types.png")
print(f"- {OUTPUT_DIR}/hourly_attacks.png")
print(f"- {OUTPUT_DIR}/method_risk.png")
print(f"- {OUTPUT_DIR}/response_time_comparison_log.png")
