# Web Uygulaması Log Saldırı Analizi

PostgreSQL üzerinde tutulan web uygulaması loglarının Python kullanılarak saldırı davranışları açısından analiz edilmesi.

## 📋 Proje Hakkında

Bu proje, web uygulaması loglarını analiz ederek potansiyel saldırı davranışlarını tespit etmeyi amaçlamaktadır. Analiz kapsamında:

- **Saldırı Oranı**: Toplam istekler içindeki saldırı yüzdesi
- **Saldırı Türleri**: Kategori bazlı saldırı dağılımı
- **Zaman Davranışı**: Saatlik saldırı yoğunluğu analizi
- **Endpoint Riskleri**: Route bazlı risk skorlaması
- **Performans Etkileri**: Response time karşılaştırması

## 🛠️ Teknolojiler

- **Python 3.x**
- **PostgreSQL** - Veritabanı
- **pandas** - Veri analizi
- **SQLAlchemy** - Veritabanı bağlantısı
- **matplotlib** - Görselleştirme
- **Docker** - Veritabanı konteynerizasyonu

## 📁 Proje Yapısı

```
├── analiz.py           # Ana analiz scripti
├── grafikler.py        # Görselleştirme scripti
├── docker-compose.yml  # PostgreSQL container tanımı
├── output/             # Oluşturulan grafikler
│   ├── attack_types.png
│   ├── hourly_attacks.png
│   └── method_risk.png
└── README.md
```

## 🚀 Kurulum

### 1. Gerekli Kütüphaneleri Yükleyin

```bash
pip install pandas sqlalchemy psycopg2-binary matplotlib
```

### 2. PostgreSQL Veritabanını Başlatın

```bash
docker-compose up -d
```

Veritabanı `localhost:5433` portunda çalışacaktır.

## 💻 Kullanım

### Analiz Çalıştırma

```bash
python analiz.py
```

Bu script aşağıdaki analizleri gerçekleştirir:
- Saldırı oranı hesaplama
- Saldırı türlerinin dağılımı
- Saatlik saldırı dağılımı
- Route bazlı risk analizi
- HTTP method bazlı risk oranları
- Response time karşılaştırması

### Grafikleri Oluşturma

```bash
python grafikler.py
```

Grafikler `output/` klasörüne kaydedilir.

## 📊 Analiz Çıktıları

### 1. Saldırı Oranı
Toplam istek sayısı içindeki saldırı yüzdesini hesaplar.

### 2. Saldırı Türleri
Kategori bazında saldırı dağılımını analiz eder (SQL Injection, XSS, vb.).

### 3. Zaman Analizi
Saldırıların saatlik dağılımını gösterir, yoğun saldırı saatlerini tespit eder.

### 4. Endpoint Risk Analizi
Her endpoint için risk skoru hesaplar:
```
risk_score = attack_count / total_requests
```

### 5. HTTP Method Analizi
GET, POST, PUT, DELETE gibi HTTP metodlarının saldırı oranlarını karşılaştırır.

### 6. Performans Etkisi
Saldırı olan ve olmayan isteklerin ortalama response time değerlerini karşılaştırır.

## 📈 Örnek Grafikler

- `attack_types.png` - Saldırı türlerinin bar grafiği
- `hourly_attacks.png` - Saatlik saldırı yoğunluğu çizgi grafiği
- `method_risk.png` - HTTP method bazlı saldırı oranları

## 🗃️ Veritabanı Şeması

`logs` tablosu aşağıdaki sütunları içerir:

| Sütun | Açıklama |
|-------|----------|
| created_at | İstek zamanı |
| attack | Saldırı durumu (ATTACK/NORMAL) |
| category | Saldırı kategorisi |
| route | İstek yapılan endpoint |
| http_method | HTTP metodu |
| http_status_code | HTTP durum kodu |
| responsetime | Yanıt süresi |
| ip_address | İstemci IP adresi |
| country | Ülke bilgisi |

## 📝 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.