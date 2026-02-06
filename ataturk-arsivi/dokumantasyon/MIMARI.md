# 🏗️ Sistem Mimarisi - Atatürk Arşiv Sistemi

## 📐 Genel Mimari

```
┌─────────────────────────────────────────────────────────────┐
│                   ATATÜRK ARŞİV SİSTEMİ                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         Kullanıcı Arayüzleri            │
        ├─────────────────────────────────────────┤
        │  • interaktif_arayuz.py (CLI Menü)     │
        │  • Python API (Programatik)             │
        │  • ornek_veri_yukle.py (Toplu Yükleme) │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │      Ana Modül (arsiv_yoneticisi.py)   │
        ├─────────────────────────────────────────┤
        │  • AtaturkArsivi sınıfı                │
        │  • soz_ekle()                           │
        │  • ara()                                │
        │  • istatistikler()                      │
        │  • disa_aktar()                         │
        │  • Hash yönetimi                        │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │          Veri Katmanı                   │
        ├─────────────────────────────────────────┤
        │  • JSON dosya sistemi                   │
        │  • veriler/sozler.json                  │
        │  • Otomatik yedekleme                   │
        └─────────────────────────────────────────┘
```

## 🔧 Bileşen Detayları

### 1. Ana Modül: `arsiv_yoneticisi.py`

```python
class AtaturkArsivi:
    ├── __init__()           # Arşiv başlatma
    ├── soz_ekle()           # Tek söz ekleme
    ├── toplu_ekle()         # Çoklu söz ekleme
    ├── ara()                # Arama ve filtreleme
    ├── istatistikler()      # İstatistik hesaplama
    ├── yazdir_soz()         # Formatlanmış çıktı
    ├── disa_aktar()         # Dışa aktarma
    └── Private Methods:
        ├── _veri_yukle()
        ├── _veri_kaydet()
        ├── _hash_seti_olustur()
        └── _metin_hash_olustur()  # Tekrar kontrolü
```

### 2. İnteraktif Arayüz: `interaktif_arayuz.py`

```python
Menü Sistemi:
├── 1. Yeni söz ekle          → yeni_soz_ekle()
├── 2. Arşivde ara            → arama_yap()
├── 3. İstatistikleri göster  → istatistik_goster()
├── 4. Tüm sözleri listele    → tum_sozleri_listele()
├── 5. Kategoriye göre liste  → kategoriye_gore_listele()
├── 6. Dışa aktar             → disa_aktar()
├── 7. Örnek veri yükle       → ornek_veri_yukle()
└── 0. Çıkış
```

### 3. Veri Yapısı

```json
{
  "metadata": {
    "versiyon": "1.0",
    "olusturma_tarihi": "YYYY-MM-DD",
    "aciklama": "...",
    "toplam_kayit": 0,
    "son_guncelleme": "YYYY-MM-DD"
  },
  "sozler": [
    {
      "id": 1,
      "metin": "...",
      "hash": "sha256_hash",
      "kategori": ["Kat1", "Kat2"],
      "tarih": "YYYY-MM-DD",
      "kaynak": "...",
      "yer": "...",
      "notlar": "...",
      "eklenme_zamani": "YYYY-MM-DD HH:MM:SS",
      "kelime_sayisi": 10,
      "karakter_sayisi": 50
    }
  ],
  "kategoriler": ["Liste"]
}
```

## 🔐 Tekrar Engelleme Algoritması

```
Metin Girişi
    ↓
┌─────────────────────┐
│ Normalizasyon       │
│ • Küçük harfe çevir │
│ • Noktalama kaldır  │
│ • Fazla boşluk sil  │
└─────────────────────┘
    ↓
┌─────────────────────┐
│ SHA-256 Hash        │
│ Oluştur             │
└─────────────────────┘
    ↓
┌─────────────────────┐
│ Hash Seti           │
│ Kontrolü            │
└─────────────────────┘
    ↓
   / \
  /   \
 /     \
Var     Yok
 │       │
 ↓       ↓
Reddet  Ekle
```

### Hash Normalizasyon Örneği

```python
# Giriş 1
"Hayatta en hakiki mürşit ilimdir, fendir."

# Giriş 2
"HAYATTA EN HAKİKİ MÜRŞİT İLİMDİR FENDIR"

# Giriş 3
"hayatta    en   hakiki mürşit    ilimdir fendir"

# Normalizasyon sonrası (hepsi aynı)
"hayatta en hakiki mursit ilimdir fendir"
       ↓
# Aynı SHA-256 hash
"a1b2c3d4e5f6..."
       ↓
# Sonuç: Tekrar tespit edildi!
```

## 🔍 Arama Sistemi

```
Arama Kriteri
    ↓
┌──────────────────┐
│ Filtre Uygula    │
├──────────────────┤
│ • Anahtar kelime │
│ • Kategori       │
│ • Tarih          │
│ • Kaynak         │
└──────────────────┘
    ↓
┌──────────────────┐
│ Metinde Ara      │
│ (case-insensitive)│
└──────────────────┘
    ↓
┌──────────────────┐
│ Sonuçları Topla  │
└──────────────────┘
    ↓
Kullanıcıya Döndür
```

### Arama Örnekleri

```python
# Basit arama
ara(anahtar_kelime="gençlik")
# Sonuç: "gençlik" kelimesini içeren tüm sözler

# Kategori filtresi
ara(kategori="Eğitim")
# Sonuç: Eğitim kategorisindeki tüm sözler

# Çoklu filtre
ara(anahtar_kelime="ilim", kategori="Bilim")
# Sonuç: "ilim" içeren VE Bilim kategorisindeki sözler
```

## 💾 Dışa Aktarma Sistemi

```
Dışa Aktarma İsteği
    ↓
┌─────────────┐
│ Format Seç  │
├─────────────┤
│ • JSON      │
│ • TXT       │
│ • Markdown  │
└─────────────┘
    ↓
    ├─ JSON ──→ Yapılandırılmış veri
    │           (Tam metadata)
    │
    ├─ TXT ───→ Düz metin
    │           (Okunabilir format)
    │
    └─ MD ────→ Markdown
                (GitHub uyumlu)
```

### Çıktı Formatları

#### JSON
```json
{
  "metadata": {...},
  "sozler": [...]
}
```

#### TXT
```
==================================================
MUSTAFA KEMAL ATATÜRK SÖZLERİ ARŞİVİ
==================================================

ID: 1
Hayatta en hakiki mürşit ilimdir, fendir.
Kategori: Bilim, Eğitim
Tarih: 1924-09-22
--------------------------------------------------
```

#### Markdown
```markdown
# Mustafa Kemal Atatürk Sözleri Arşivi

## 1. Söz

> Hayatta en hakiki mürşit ilimdir, fendir.

**Kategori:** Bilim, Eğitim
**Tarih:** 1924-09-22
```

## 📊 İstatistik Hesaplama

```
Tüm Kayıtlar
    ↓
┌──────────────────────┐
│ Toplam Kayıt Sayısı  │
│ Toplam Kelime        │
│ Ortalama Uzunluk     │
└──────────────────────┘
    ↓
┌──────────────────────┐
│ Min/Max Analizi      │
│ • En uzun söz        │
│ • En kısa söz        │
└──────────────────────┘
    ↓
┌──────────────────────┐
│ Kategori Dağılımı    │
│ Her kategori için    │
│ söz sayısı           │
└──────────────────────┘
    ↓
Sonuç Dictionary
```

## 🔄 Veri Akışı

### Söz Ekleme Akışı

```
Kullanıcı Girişi
    ↓
Validasyon
    ↓
Hash Oluştur
    ↓
Hash Kontrolü
    │
    ├─ Var ─→ Reddet
    │
    └─ Yok ─→ Kayıt Oluştur
                    ↓
              Metadata Ekle
                    ↓
              JSON'a Kaydet
                    ↓
              Hash Set Güncelle
                    ↓
              Başarı Mesajı
```

### Arama Akışı

```
Arama Kriterleri
    ↓
Tüm Kayıtları Al
    ↓
Her Kayıt İçin:
    │
    ├─ Anahtar kelime kontrolü
    ├─ Kategori kontrolü
    ├─ Tarih kontrolü
    └─ Kaynak kontrolü
    ↓
Eşleşenleri Topla
    ↓
Sonuç Listesi
```

## 🎯 Performans Özellikleri

| Özellik | Performans |
|---------|------------|
| Hash hesaplama | O(n) - metin uzunluğu |
| Hash kontrolü | O(1) - set lookup |
| Ekleme | O(1) - ortalama |
| Arama (anahtar kelime) | O(n) - kayıt sayısı |
| Arama (hash) | O(1) - set lookup |
| Dışa aktarma | O(n) - kayıt sayısı |
| İstatistik | O(n) - kayıt sayısı |

## 🔧 Genişletilebilirlik

### Gelecek Özellikler

```
Mevcut Sistem
    ↓
Potansiyel Eklentiler:
    │
    ├─ Web Arayüzü (Flask/Django)
    ├─ Veritabanı (SQLite/PostgreSQL)
    ├─ RESTful API
    ├─ Tam metin arama (Elasticsearch)
    ├─ AI bazlı benzerlik tespiti
    ├─ Çoklu dil desteği
    ├─ Kullanıcı yönetimi
    └─ Bulut senkronizasyonu
```

### Modüler Yapı

```python
# Yeni özellik eklemek kolay
class AtaturkArsivi:
    def yeni_ozellik(self):
        # Mevcut API'yi bozmadan
        # yeni özellikler eklenebilir
        pass
```

## 🛡️ Güvenlik ve Veri Bütünlüğü

```
Veri Koruma Mekanizmaları:
├─ Hash tabanlı tekrar kontrolü
├─ Otomatik metadata yönetimi
├─ JSON şema validasyonu (implicit)
├─ Dosya yedekleme (dışa aktarma)
├─ Hata yakalama (try-except)
└─ Veri normalizasyonu
```

## 📝 Kod Organizasyonu

```
ataturk-arsivi/
│
├── veriler/
│   └── sozler.json              # Veri depolama
│
├── araclar/
│   ├── arsiv_yoneticisi.py      # Core logic
│   ├── ornek_veri_yukle.py      # Data seeding
│   └── interaktif_arayuz.py     # User interface
│
└── dokumantasyon/
    ├── README.md                # Usage guide
    ├── HIZLI-BASLANGIC.md      # Quick start
    └── MIMARI.md               # Bu dosya
```

## 🎓 Tasarım Kararları

### Neden JSON?
- ✅ İnsan tarafından okunabilir
- ✅ Python'da kolay kullanım
- ✅ Versiyon kontrolü uyumlu
- ✅ Taşınabilir
- ✅ Yedekleme kolay

### Neden Hash?
- ✅ Hızlı tekrar kontrolü (O(1))
- ✅ Farklı yazımları yakalar
- ✅ Güvenilir benzersizlik
- ✅ Minimal bellek kullanımı

### Neden Python?
- ✅ Kolay öğrenilir
- ✅ Zengin standart kütüphane
- ✅ Cross-platform
- ✅ Hızlı prototipleme

## 🔗 API Referansı

### Sınıf: AtaturkArsivi

```python
# Başlatma
arsiv = AtaturkArsivi(veri_dosyasi="veriler/sozler.json")

# Söz ekleme
arsiv.soz_ekle(metin, kategori, tarih, kaynak, yer, notlar)
→ bool (True: başarılı, False: tekrar)

# Toplu ekleme
arsiv.toplu_ekle(sozler_listesi)
→ dict {"eklenen": int, "tekrar": int, "hata": int}

# Arama
arsiv.ara(anahtar_kelime, kategori, tarih, kaynak)
→ list[dict] (eşleşen kayıtlar)

# İstatistikler
arsiv.istatistikler()
→ dict (kapsamlı istatistikler)

# Dışa aktarma
arsiv.disa_aktar(dosya_adi, format)
→ None (dosya oluşturur)
```

## 📈 Ölçeklenebilirlik

### Mevcut Limitler
- JSON dosya boyutu: ~10MB (10,000+ söz)
- Arama hızı: Linear O(n)
- Bellek kullanımı: Tüm veriler RAM'de

### Optimizasyon Önerileri
```python
# 10,000+ kayıt için
- Veritabanına geçiş (SQLite/PostgreSQL)
- İndeksleme (kategori, tarih)
- Sayfalama (pagination)
- Önbellekleme (caching)
```

---

<div align="center">

**Bu mimari, genişletilebilir ve sürdürülebilir bir sistem sağlar.**

Geliştiriciler için tasarlanmıştır 🇹🇷

</div>
