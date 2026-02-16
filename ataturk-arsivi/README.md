# 🇹🇷 Atatürk Arşiv Sistemi

> Mustafa Kemal Atatürk'ün sözlerini, cümlelerini ve paragraflarını mükerrer olmayan bir şekilde arşivleyen kapsamlı sistem.

## ✅ Durum: TAM FONKSİYONEL VE KULLANIMA HAZIR! 🎉

## 📥 Hızlı İndirme ve Kurulum

### Yöntem 1: ZIP İndirme (En Kolay)
1. [Buradan ZIP dosyasını indirin](https://github.com/savasava034/savasava034/archive/refs/heads/main.zip)
2. Dosyayı çıkartın
3. `ataturk-arsivi/araclar` klasörüne gidin
4. Başlatıcıyı çalıştırın:
   - **Windows**: `baslatici.bat` dosyasına çift tıklayın
   - **Linux/macOS**: Terminal'de `./baslatici.sh` yazın

### Yöntem 2: Git ile Klonlama
```bash
git clone https://github.com/savasava034/savasava034.git
cd savasava034/ataturk-arsivi/araclar
./baslatici.sh  # veya Windows'ta: baslatici.bat
```

📖 **[Detaylı Kurulum Kılavuzu](KURULUM.md)** - Tüm platformlar için adım adım rehber

---

## 🎯 Proje Amacı

Bu proje, **Mustafa Kemal Atatürk**'ün tüm sözlerini, cümlelerini ve paragraflarını:
- ✅ **Tekrarsız** (mükerrer olmayan) bir şekilde toplar
- 🏷️ **Kategorize ederek** düzenler
- 🔍 **Aranabilir** hale getirir
- 💾 **Yerel olarak** saklar
- 📊 **İstatistiklerle** analiz eder

## 🚀 Hızlı Başlangıç

### 1. İnteraktif Arayüzü Başlat

```bash
cd ataturk-arsivi/araclar
python3 interaktif_arayuz.py
```

**VEYA Basitleştirilmiş Başlatıcı Kullan:**

- **Windows**: `baslatici.bat` dosyasına çift tıklayın
- **Linux/macOS**: `./baslatici.sh` komutunu çalıştırın

Başlatıcı otomatik olarak:
- ✅ Python'u kontrol eder
- ✅ Örnek verileri yükleme seçeneği sunar
- ✅ İnteraktif menüyü başlatır
- ✅ Sistem bilgilerini gösterir

### 2. Örnek Verileri Yükle

```bash
cd ataturk-arsivi/araclar
python3 ornek_veri_yukle.py
```

### 3. Python'da Kullan

```python
from araclar.arsiv_yoneticisi import AtaturkArsivi

arsiv = AtaturkArsivi()
arsiv.soz_ekle(
    metin="Hayatta en hakiki mürşit ilimdir, fendir.",
    kategori=["Bilim", "Eğitim"]
)
```

## ✨ Ana Özellikler

| Özellik | Açıklama |
|---------|----------|
| 🔒 **Tekrar Engelleme** | Hash tabanlı sistem ile aynı söz iki kez eklenmez |
| 🏷️ **Kategorilendirme** | Eğitim, Bilim, Cumhuriyet gibi kategorilerle organize etme |
| 🔍 **Gelişmiş Arama** | Kelime, kategori, tarih ve kaynak bazlı arama |
| 📊 **İstatistikler** | Detaylı analiz ve raporlama |
| 💾 **Çoklu Format** | JSON, TXT ve Markdown dışa aktarma |
| 📅 **Tarih Takibi** | Her söz için tarih ve kaynak bilgisi |
| 🖥️ **Yerel Çalışma** | İnternet gerektirmez, laptop'ta çalışır |

## 📂 Dizin Yapısı

```
ataturk-arsivi/
│
├── veriler/                      # Veri dosyaları
│   └── sozler.json              # Ana arşiv (otomatik oluşur)
│
├── araclar/                      # Python araçları
│   ├── arsiv_yoneticisi.py      # Ana modül
│   ├── ornek_veri_yukle.py      # Örnek veri yükleyici
│   └── interaktif_arayuz.py     # Kullanıcı arayüzü
│
└── dokumantasyon/               # Dokümantasyon
    └── README.md                # Detaylı kullanım kılavuzu
```

## 📖 Kullanım Kılavuzu

### Menü Sistemi

İnteraktif arayüzde şu işlemleri yapabilirsiniz:

1. **Yeni söz ekle** - Arşive yeni kayıt ekleyin
2. **Arşivde ara** - Kelime, kategori veya tarihe göre arama
3. **İstatistikleri görüntüle** - Arşiv hakkında detaylı bilgi
4. **Tüm sözleri listele** - Tüm kayıtları görüntüle
5. **Kategoriye göre listele** - Belirli kategorideki sözleri görüntüle
6. **Dışa aktar** - JSON, TXT veya MD formatında kaydet
7. **Örnek verileri yükle** - Hazır 20+ Atatürk sözü yükle

### Python API

Programatik kullanım için:

```python
from araclar.arsiv_yoneticisi import AtaturkArsivi

# Arşiv oluştur
arsiv = AtaturkArsivi()

# Söz ekle
arsiv.soz_ekle(
    metin="Egemenlik kayıtsız şartsız milletindir.",
    kategori=["Cumhuriyet", "Demokrasi"],
    tarih="1920-04-23",
    kaynak="TBMM Açılış Konuşması"
)

# Ara
sonuclar = arsiv.ara(kategori="Eğitim")

# İstatistikler
istat = arsiv.istatistikler()
print(f"Toplam: {istat['toplam_kayit']} söz")

# Dışa aktar
arsiv.disa_aktar("ataturk_arsivi.md", format="md")
```

## 🏷️ Kategori Sistemi

Önerilen kategoriler:

- **Eğitim** - Eğitim ve öğretim
- **Bilim** - Bilim ve teknoloji  
- **Cumhuriyet** - Cumhuriyet rejimi
- **Demokrasi** - Demokrasi ve yönetim
- **Kadın Hakları** - Kadın hakları ve özgürlüğü
- **Gençlik** - Gençliğe hitaplar
- **Milli Mücadele** - Kurtuluş Savaşı
- **Barış** - Barış ve dış politika
- **Kültür** - Kültür ve sanat
- **Tarih** - Tarih bilinci
- **Vatan** - Vatan sevgisi
- **Çağdaşlaşma** - Modernleşme

## 📊 Veri Yapısı

Her kayıt şunları içerir:

```json
{
  "id": 1,
  "metin": "Hayatta en hakiki mürşit ilimdir, fendir.",
  "hash": "benzersiz_hash",
  "kategori": ["Bilim", "Eğitim"],
  "tarih": "1924-09-22",
  "kaynak": "Samsun'da Öğretmenlerle Konuşma",
  "yer": "Samsun",
  "notlar": "En ünlü sözlerinden",
  "eklenme_zamani": "2026-02-06 20:10:00",
  "kelime_sayisi": 7,
  "karakter_sayisi": 42
}
```

## 🔒 Tekrar Önleme Mekanizması

Sistem her metin için:
1. Noktalama işaretlerini kaldırır
2. Büyük/küçük harf dönüşümü yapar
3. Fazla boşlukları temizler
4. SHA-256 hash oluşturur
5. Mevcut hash'lerle karşılaştırır

Böylece aynı söz farklı formatlarda girilse bile sadece bir kez eklenir.

## 💾 Dışa Aktarma Formatları

### JSON Format
```bash
arsiv.disa_aktar("arsiv.json", format="json")
```
Yapılandırılmış veri, programatik kullanım için ideal.

### TXT Format
```bash
arsiv.disa_aktar("arsiv.txt", format="txt")
```
Düz metin, okunması kolay format.

### Markdown Format
```bash
arsiv.disa_aktar("arsiv.md", format="md")
```
GitHub ve dokümantasyon için ideal.

## 📈 İstatistikler

Arşiv şu istatistikleri sunar:

- Toplam söz sayısı
- Toplam kelime sayısı
- Ortalama söz uzunluğu
- En uzun/kısa söz
- Kategori dağılımı
- Tarihsel analiz

## 🔧 Gereksinimler

- **Python**: 3.7+
- **Kütüphaneler**: Standart Python (ek kurulum YOK)
- **Platform**: Windows, macOS, Linux
- **Disk**: Minimal (~1-10 MB arşiv için)

## 📝 Örnek Veriler

Sistem 20+ örnek Atatürk sözü ile gelir:

- Hayatta en hakiki mürşit ilimdir
- Egemenlik kayıtsız şartsız milletindir
- Yurtta sulh, cihanda sulh
- Gençliğe Hitabe
- Ve daha fazlası...

## 🎓 Kullanım Senaryoları

### Eğitimciler için
- Ders materyali hazırlama
- Öğrencilere alıntı kaynağı
- Tarih dersleri

### Araştırmacılar için
- Söz analizi
- Tarihsel araştırma
- İçerik analizi

### Kişisel Kullanım
- Atatürk sözleri koleksiyonu
- Günlük ilham kaynağı
- Bilgi arşivi

## 🤝 Katkıda Bulunma

Projeye katkıda bulunmak için:

1. Yeni Atatürk sözleri ekleyin
2. Mevcut kayıtları doğrulayın
3. Kategorileri iyileştirin
4. Hata bildirin
5. Özellik önerin

## 📚 Detaylı Dokümantasyon

Daha fazla bilgi için:
- [Detaylı Kullanım Kılavuzu](dokumantasyon/README.md)
- Kod içi dokümantasyon
- Örnek kullanımlar

## 🌟 Öne Çıkan Özellikler

### 1. Akıllı Tekrar Engelleme
Aynı anlamdaki farklı yazımları tespit eder:
- "ilimdir" = "ilim'dir" = "İLİMDİR"

### 2. Esnek Arama
```python
# Kelime araması
arsiv.ara(anahtar_kelime="gençlik")

# Kategori filtresi
arsiv.ara(kategori="Eğitim")

# Çoklu kriter
arsiv.ara(anahtar_kelime="cumhuriyet", kategori="Demokrasi")
```

### 3. Toplu İşlemler
```python
# Birden fazla söz ekle
sozler = [
    {"metin": "Söz 1", "kategori": ["Eğitim"]},
    {"metin": "Söz 2", "kategori": ["Bilim"]}
]
istatistik = arsiv.toplu_ekle(sozler)
```

## 🎯 Proje Hedefleri

- [x] Temel arşiv sistemi
- [x] Tekrar engelleme mekanizması
- [x] Kategorilendirme
- [x] Arama ve filtreleme
- [x] Dışa aktarma (JSON, TXT, MD)
- [x] İnteraktif kullanıcı arayüzü
- [x] Örnek veri seti
- [x] Detaylı dokümantasyon
- [ ] Web arayüzü (gelecek)
- [ ] Veritabanı entegrasyonu (gelecek)
- [ ] API sunucusu (gelecek)

## 💡 İpuçları

1. **İlk Kullanım**: Örnek verileri yükleyin (`ornek_veri_yukle.py`)
2. **Yedekleme**: Düzenli olarak dışa aktarma yapın
3. **Kategoriler**: Tutarlı kategori isimleri kullanın
4. **Tarihler**: YYYY-MM-DD formatını kullanın
5. **Kaynaklar**: Her söz için kaynak belirtin

## 📞 Destek

- GitHub Issues: Hata bildirimi ve öneriler
- Dokümantasyon: Detaylı kullanım bilgileri
- Örnek kodlar: `araclar/` dizininde

## 📄 Lisans

Bu proje eğitim amaçlıdır. Atatürk'ün sözleri kamu malıdır ve herkes tarafından kullanılabilir.

## 🙏 Önemli Not

Bu arşiv, Mustafa Kemal Atatürk'ün düşüncelerini ve vizyonunu gelecek nesillere aktarmak amacıyla oluşturulmuştur. Tüm sözler doğrulanmalı ve kaynak gösterilmelidir.

---

<div align="center">

**"Hayatta en hakiki mürşit ilimdir, fendir."**  
*— Mustafa Kemal Atatürk*

🇹🇷 **Türkiye Cumhuriyeti'nin Kurucusu**

</div>
