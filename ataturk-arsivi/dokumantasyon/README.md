# 🇹🇷 Mustafa Kemal Atatürk Arşiv Sistemi

## 📖 Genel Bakış

Bu proje, **Mustafa Kemal Atatürk**'ün sözlerini, cümlelerini ve paragraflarını kapsamlı bir şekilde arşivlemek için geliştirilmiş bir sistemdir. Sistem, tekrarlı kayıtları engelleyerek benzersiz bir koleksiyon oluşturur ve yerel bilgisayarınızda çalışır.

## ✨ Özellikler

- ✅ **Tekrarlı Kayıt Engelleme**: Hash tabanlı sistem ile aynı sözün birden fazla eklenmesi önlenir
- 🏷️ **Kategorilendirme**: Sözleri konu, tema veya bağlama göre kategorilere ayırma
- 🔍 **Gelişmiş Arama**: Anahtar kelime, kategori, tarih ve kaynak bazlı arama
- 📊 **İstatistikler**: Arşiv içeriği hakkında detaylı istatistiksel bilgiler
- 💾 **Dışa Aktarma**: JSON, TXT ve Markdown formatlarında dışa aktarma
- 📅 **Tarih ve Kaynak Takibi**: Her söz için tarih ve kaynak bilgisi saklama
- 🎯 **Kolay Kullanım**: Hem komut satırı hem de Python API desteği

## 📁 Dizin Yapısı

```
ataturk-arsivi/
├── veriler/
│   └── sozler.json              # Ana veri dosyası (otomatik oluşturulur)
├── araclar/
│   ├── arsiv_yoneticisi.py      # Ana arşiv yönetim modülü
│   ├── ornek_veri_yukle.py      # Örnek verileri yükleyen script
│   └── interaktif_arayuz.py     # Kullanıcı dostu komut satırı arayüzü
└── dokumantasyon/
    └── README.md                # Bu dosya
```

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Python 3.7 veya üzeri
- Standart Python kütüphaneleri (ek kurulum gerektirmez)

### Kurulum

1. Repository'yi klonlayın veya indirin
2. `ataturk-arsivi` dizinine gidin

```bash
cd ataturk-arsivi
```

### Kullanım Yöntemleri

#### 1. İnteraktif Arayüz (Önerilen)

En kolay kullanım yolu, interaktif menü sistemidir:

```bash
cd araclar
python3 interaktif_arayuz.py
```

Bu komut menü tabanlı bir arayüz açar ve şu işlemleri yapmanızı sağlar:
- Yeni söz ekleme
- Arşivde arama
- İstatistikleri görüntüleme
- Sözleri listeleme
- Dışa aktarma
- Örnek verileri yükleme

#### 2. Örnek Verileri Yükleme

Arşivi hızlıca doldurmak için örnek verileri yükleyin:

```bash
cd araclar
python3 ornek_veri_yukle.py
```

Bu komut 20+ ünlü Atatürk sözünü otomatik olarak arşive ekler.

#### 3. Python API Kullanımı

Kendi scriptlerinizde kullanmak için:

```python
from arsiv_yoneticisi import AtaturkArsivi

# Arşiv oluştur
arsiv = AtaturkArsivi()

# Yeni söz ekle
arsiv.soz_ekle(
    metin="Hayatta en hakiki mürşit ilimdir, fendir.",
    kategori=["Bilim", "Eğitim"],
    tarih="1924-09-22",
    kaynak="Samsun'da Öğretmenlerle Konuşma"
)

# Arama yap
sonuclar = arsiv.ara(anahtar_kelime="bilim")

# İstatistikleri görüntüle
istat = arsiv.istatistikler()
print(f"Toplam kayıt: {istat['toplam_kayit']}")

# Dışa aktar
arsiv.disa_aktar("ataturk_arsivi.md", format="md")
```

## 📚 Detaylı Kullanım

### Yeni Söz Ekleme

```python
arsiv.soz_ekle(
    metin="Eklenecek söz metni",
    kategori=["Kategori1", "Kategori2"],  # Opsiyonel
    tarih="YYYY-MM-DD",                   # Opsiyonel
    kaynak="Kaynak adı",                  # Opsiyonel
    yer="Söylendiği yer",                 # Opsiyonel
    notlar="Ek bilgiler"                  # Opsiyonel
)
```

### Toplu Ekleme

```python
sozler_listesi = [
    {
        "metin": "Söz 1",
        "kategori": ["Eğitim"],
        "tarih": "1923-01-01"
    },
    {
        "metin": "Söz 2",
        "kategori": ["Bilim", "Gençlik"]
    }
]

istatistik = arsiv.toplu_ekle(sozler_listesi)
print(f"Eklenen: {istatistik['eklenen']}")
print(f"Tekrar: {istatistik['tekrar']}")
```

### Arama ve Filtreleme

```python
# Anahtar kelime ile arama
sonuclar = arsiv.ara(anahtar_kelime="gençlik")

# Kategoriye göre filtreleme
sonuclar = arsiv.ara(kategori="Eğitim")

# Tarihe göre filtreleme
sonuclar = arsiv.ara(tarih="1923-10-29")

# Birden fazla kriter
sonuclar = arsiv.ara(
    anahtar_kelime="cumhuriyet",
    kategori="Demokrasi"
)
```

### Dışa Aktarma

```python
# JSON formatında
arsiv.disa_aktar("arsiv.json", format="json")

# Düz metin olarak
arsiv.disa_aktar("arsiv.txt", format="txt")

# Markdown formatında
arsiv.disa_aktar("arsiv.md", format="md")
```

## 🏷️ Önerilen Kategoriler

Sistem herhangi bir kategori kabul eder, ancak tutarlılık için şunlar önerilir:

- **Eğitim**: Eğitim ve öğretim ile ilgili
- **Bilim**: Bilim ve teknoloji
- **Cumhuriyet**: Cumhuriyet rejimi
- **Demokrasi**: Demokrasi ve yönetim
- **Kadın Hakları**: Kadın hakları ve özgürlüğü
- **Gençlik**: Gençliğe hitaplar
- **Milli Mücadele**: Kurtuluş Savaşı dönemi
- **Devrim**: İnkılaplar ve reformlar
- **Barış**: Barış ve dış politika
- **Kültür**: Kültür ve sanat
- **Tarih**: Tarih bilinci
- **Liderlik**: Liderlik ve yöneticilik
- **Vatan**: Vatan sevgisi
- **İnkılap**: Türk İnkılabı
- **Çağdaşlaşma**: Modernleşme

## 📊 Veri Yapısı

Her söz şu bilgileri içerir:

```json
{
  "id": 1,
  "metin": "Söz metni",
  "hash": "benzersiz_hash_degeri",
  "kategori": ["Kategori1", "Kategori2"],
  "tarih": "YYYY-MM-DD",
  "kaynak": "Kaynak adı",
  "yer": "Söylendiği yer",
  "notlar": "Ek bilgiler",
  "eklenme_zamani": "YYYY-MM-DD HH:MM:SS",
  "kelime_sayisi": 10,
  "karakter_sayisi": 65
}
```

## 🔒 Tekrarlı Kayıt Engelleme

Sistem, her sözün içeriğinden SHA-256 tabanlı bir hash değeri oluşturur. Bu hash değeri:

1. Noktalama işaretlerini ve büyük/küçük harf farklılıklarını göz ardı eder
2. Fazla boşlukları temizler
3. Aynı anlamdaki sözleri tespit eder

Bu sayede aynı söz farklı formatlarda bile girilse, yalnızca bir kez eklenir.

## 💡 Kullanım Örnekleri

### Örnek 1: Basit Kullanım

```python
from arsiv_yoneticisi import AtaturkArsivi

arsiv = AtaturkArsivi()
arsiv.soz_ekle(
    metin="Egemenlik kayıtsız şartsız milletindir.",
    kategori=["Cumhuriyet", "Demokrasi"]
)
```

### Örnek 2: Toplu Veri Girişi

```python
from arsiv_yoneticisi import AtaturkArsivi

arsiv = AtaturkArsivi()

# Bir dosyadan veya API'den alınan sözler
sozler = [
    {"metin": "Söz 1", "kategori": ["Eğitim"]},
    {"metin": "Söz 2", "kategori": ["Bilim"]},
    # ... daha fazla
]

istatistik = arsiv.toplu_ekle(sozler)
print(f"Başarıyla eklendi: {istatistik['eklenen']}")
```

### Örnek 3: Arama ve Raporlama

```python
from arsiv_yoneticisi import AtaturkArsivi

arsiv = AtaturkArsivi()

# Eğitim kategorisindeki tüm sözleri bul
egitim_sozleri = arsiv.ara(kategori="Eğitim")

# Her birini yazdır
for soz in egitim_sozleri:
    arsiv.yazdir_soz(soz)

# İstatistikler
istat = arsiv.istatistikler()
print(f"Eğitim kategorisinde {len(egitim_sozleri)} söz var")
```

### Örnek 4: Dışa Aktarma

```python
from arsiv_yoneticisi import AtaturkArsivi

arsiv = AtaturkArsivi()

# Markdown formatında dışa aktar
arsiv.disa_aktar("ataturk_sozleri.md", format="md")

# JSON olarak yedekle
arsiv.disa_aktar("yedek.json", format="json")
```

## 🛠️ Gelişmiş Özellikler

### Özel Veri Kaynağı

```python
# Farklı bir dosya kullan
arsiv = AtaturkArsivi(veri_dosyasi="ozel/yolum/veriler.json")
```

### İstatistik Analizi

```python
istat = arsiv.istatistikler()

print(f"Toplam söz: {istat['toplam_kayit']}")
print(f"Toplam kelime: {istat['toplam_kelime']}")
print(f"Ortalama uzunluk: {istat['ortalama_kelime']} kelime")

# En uzun söz
print(f"En uzun söz: {istat['en_uzun_soz']['metin']}")

# Kategori dağılımı
for kategori, sayi in istat['kategori_dagilimi'].items():
    print(f"{kategori}: {sayi} söz")
```

## 📝 Katkıda Bulunma

Arşivi geliştirmek için:

1. Yeni Atatürk sözleri ekleyin
2. Mevcut kayıtları doğrulayın (tarih, kaynak, vb.)
3. Kategorilendirmeyi iyileştirin
4. Yeni özellikler önerin

## 🔐 Veri Güvenliği

- Tüm veriler yerel olarak saklanır
- İnternet bağlantısı gerektirmez
- JSON formatında kolayca yedeklenebilir
- Otomatik hash kontrolü ile veri bütünlüğü

## 📞 Destek ve Sorular

Sorularınız veya önerileriniz için GitHub Issues kullanabilirsiniz.

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir. Mustafa Kemal Atatürk'ün sözleri kamu malıdır.

## 🙏 Teşekkürler

Bu arşiv, Mustafa Kemal Atatürk'ün düşüncelerini ve vizyonunu gelecek nesillere aktarmak amacıyla oluşturulmuştur.

---

**"Hayatta en hakiki mürşit ilimdir, fendir."**  
— Mustafa Kemal Atatürk
