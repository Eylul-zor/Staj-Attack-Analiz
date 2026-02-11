# ==============================
# attack log analysis
# ==============================

import pandas as pd
from data_loader import load_data, clean_data

# ------------------------------
# 1. veriyi yükle ve hazırla
# ------------------------------
df_raw = load_data()
df = clean_data(df_raw)

print("veri yüklendi.")
print("boyut:", df.shape)
print(df.head())

print("\nattack kolonundaki değerler:")
print(df["attack"].value_counts())


# ------------------------------
# 2. analiz 1: attack orani
# ------------------------------
def attack_ratio():
    attack_ratio = (df["attack"] == "ATTACK").mean()

    print("\n--- attack orani ---")
    print(f"attack oranı: {attack_ratio:.4f} (%{attack_ratio * 100:.2f})")


# ------------------------------
# 3. analiz 2: attack türleri (category)
# ------------------------------
def attack_tipleri():
    df_attack = df[df["attack"] == "ATTACK"].copy()

    # clean_data fonksiyonunda halledildi ama yine de burda kontrol edelim
    # çoklu category'leri ayır
    attack_types = df_attack["category_clean"].str.split(",").explode().str.strip()

    attack_type_counts = attack_types.value_counts()
    attack_type_ratio = attack_type_counts / attack_type_counts.sum()

    print("\n--- attack türleri (adet) ---")
    print(attack_type_counts)

    print("\n--- attack türleri (oran %) ---")
    print((attack_type_ratio * 100).round(2))


# ------------------------------
# 4. analiz 3: zaman davranişi (saatlik)
# ------------------------------
def zaman_analizi():
    df_attack = df[df["attack"] == "ATTACK"].copy()
    df_attack["hour"] = df_attack["created_at"].dt.hour

    hourly_attacks = df_attack.groupby("hour").size()

    print("\n--- saatlik attack dağilimi ---")
    print(hourly_attacks)


# ------------------------------
# 5. analiz 4: route / endpoint risk analizi
# ------------------------------
def route_risk_analizi():
    route_risk = df.groupby("route").agg(
        total_requests=("attack", "count"),
        attack_count=("attack", lambda x: (x == "ATTACK").sum()),
    )

    route_risk["risk_score"] = route_risk["attack_count"] / route_risk["total_requests"]

    route_risk = route_risk.sort_values("risk_score", ascending=False)

    print("\n--- route risk analizi (top 10) ---")
    print(route_risk.head(10))


# ------------------------------
# 6. analiz 5: http method vs attack
# ------------------------------
def method_risk_analizi():
    method_risk = (
        df.groupby("http_method")["attack"]
        .apply(lambda x: (x == "ATTACK").mean())
        .sort_values(ascending=False)
    )

    print("\n--- http method risk oranlari ---")
    print((method_risk * 100).round(2))


# ------------------------------
# 7. analiz 6: response time karşilaştirmasi
# ------------------------------
def response_time_analizi():
    response_time_analysis = df.groupby("attack")["responsetime"].mean()

    print("\n--- response time ortalamalari ---")
    print(response_time_analysis)


# ------------------------------
# Çalıştır
# ------------------------------
if __name__ == "__main__":
    attack_ratio()
    attack_tipleri()
    zaman_analizi()
    route_risk_analizi()
    method_risk_analizi()
    response_time_analizi()

    # ------------------------------
    # Özet
    # ------------------------------
    print("\n=== analiz tamamlandi ===")
    print(f"toplam kayıt: {len(df)}")
    print(f"attack sayısı: {(df['attack'] == 'ATTACK').sum()}")
    ratio = (df["attack"] == "ATTACK").mean()
    print(f"attack oranı: %{ratio * 100:.2f}")
