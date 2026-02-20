# 📥 Kurulum ve İndirme Kılavuzu - Atatürk Arşiv Sistemi

## ✅ Evet, Uygulama Tamamlandı!

Atatürk Arşiv Sistemi **tam fonksiyonel** ve **kullanıma hazır** durumda! 🎉

## 📋 İçindekiler

1. [Sistem Gereksinimleri](#-sistem-gereksinimleri)
2. [İndirme Yöntemleri](#-indirme-yöntemleri)
3. [Kurulum Adımları](#-kurulum-adımları)
4. [İlk Kullanım](#-ilk-kullanım)
5. [Sorun Giderme](#-sorun-giderme)

---

## 💻 Sistem Gereksinimleri

### Minimal Gereksinimler:
- **Python**: 3.7 veya üzeri
- **İşletim Sistemi**: Windows, macOS veya Linux
- **Disk Alanı**: 10 MB
- **RAM**: 512 MB
- **İnternet**: Sadece indirme için (kullanım için gerekli değil)

### Python Kurulumu Kontrolü:

```bash
# Python versiyonunu kontrol edin
python --version
# veya
python3 --version
```

**Eğer Python yüklü değilse:**
- **Windows**: https://www.python.org/downloads/ adresinden indirin
- **macOS**: Terminal'de `brew install python3` (Homebrew ile)
- **Linux**: `sudo apt install python3` (Ubuntu/Debian)

---

## 📥 İndirme Yöntemleri

### Yöntem 1: ZIP Dosyası İndirme (En Kolay)

1. **GitHub'da repository sayfasına gidin:**
   ```
   https://github.com/savasava034/savasava034
   ```

2. **Yeşil "Code" butonuna tıklayın**

3. **"Download ZIP" seçeneğini seçin**

4. **İndirilen dosyayı çıkartın:**
   - Windows: Sağ tık → "Extract All"
   - macOS: Çift tıklayın
   - Linux: `unzip savasava034-main.zip`

### Yöntem 2: Git ile Klonlama (Önerilen)

```bash
# Repository'yi klonlayın
git clone https://github.com/savasava034/savasava034.git

# Dizine girin
cd savasava034
```

### Yöntem 3: Sadece Atatürk Arşivi Klasörünü İndirme

Eğer sadece Atatürk Arşiv sistemini istiyorsanız:

1. GitHub'da `ataturk-arsivi` klasörüne gidin
2. Her dosyayı manuel olarak indirin
3. Veya yukarıdaki yöntemlerden birini kullanıp sadece bu klasörü kullanın

---

## 🚀 Kurulum Adımları

### Adım 1: Dosyaları İndirin

Yukarıdaki yöntemlerden birini kullanarak dosyaları indirin.

### Adım 2: Atatürk Arşivi Klasörüne Gidin

```bash
cd savasava034/ataturk-arsivi
```

### Adım 3: Python'un Çalıştığını Doğrulayın

```bash
python3 --version
```

Bu komut Python versiyonunu göstermelidir (örn: Python 3.9.7)

### Adım 4: Hiçbir Ek Kurulum Gerekmez! 🎉

Bu sistem **herhangi bir dış kütüphane gerektirmez**. Python'un standart kütüphaneleri ile çalışır.

---

## 🎯 İlk Kullanım

### Seçenek 1: Örnek Verilerle Başlama (Önerilen)

```bash
# Atatürk arşivi klasörüne gidin
cd ataturk-arsivi/araclar

# Örnek verileri yükleyin (20+ Atatürk sözü)
python3 ornek_veri_yukle.py
```

**Çıktı:**
```
✅ Başarıyla eklenen: 20
⚠️  Tekrarlı (atlandı): 0
❌ Hata: 0
```

### Seçenek 2: İnteraktif Menü ile Kullanma

```bash
# Hala araclar klasöründeyseniz
python3 interaktif_arayuz.py
```

**Menü görünümü:**
```
🇹🇷  ATATÜRK ARŞİVİ YÖNETİM SİSTEMİ
======================================================================

📋 Menü:
  1. 📝 Yeni söz ekle
  2. 🔍 Arşivde ara
  3. 📊 İstatistikleri görüntüle
  4. 📖 Tüm sözleri listele
  5. 🏷️  Kategoriye göre listele
  6. 💾 Dışa aktar (JSON/TXT/MD)
  7. 📥 Örnek verileri yükle
  0. 🚪 Çıkış
======================================================================

👉 Seçiminiz:
```

### Seçenek 3: Python Kodu ile Kullanma

```python
# Python yorumlayıcısını başlatın
python3

# Kodu çalıştırın
from arsiv_yoneticisi import AtaturkArsivi

arsiv = AtaturkArsivi()
arsiv.soz_ekle(
    metin="Hayatta en hakiki mürşit ilimdir, fendir.",
    kategori=["Bilim", "Eğitim"]
)

# Arama yapın
sonuclar = arsiv.ara(kategori="Eğitim")
print(f"Bulunan: {len(sonuclar)} söz")
```

---

## 📖 Temel Kullanım Örnekleri

### 1️⃣ Yeni Söz Ekleme

İnteraktif menüde **1** seçin:
```
💬 Söz/Cümle/Paragraf: [Atatürk sözünü girin]
🏷️  Kategoriler: Eğitim, Gençlik
📅 Tarih: 1923-10-29
📚 Kaynak: Nutuk
```

### 2️⃣ Arama Yapma

İnteraktif menüde **2** seçin:
```
🔎 Anahtar kelime: gençlik
```

### 3️⃣ İstatistikleri Görüntüleme

İnteraktif menüde **3** seçin:
```
📊 Arşiv İstatistikleri
   Toplam Kayıt: 20
   Toplam Kelime: 212
   Ortalama Kelime/Söz: 10
```

### 4️⃣ Dışa Aktarma

İnteraktif menüde **6** seçin ve format seçin:
- **JSON**: Yapılandırılmış veri
- **TXT**: Düz metin
- **MD**: Markdown (GitHub için ideal)

---

## 🔍 Klasör Yapısı

İndirdikten sonra göreceğiniz yapı:

```
savasava034/
├── ataturk-arsivi/              ← ANA KLASÖR
│   ├── README.md                ← Kullanım kılavuzu
│   ├── KURULUM.md              ← Bu dosya
│   ├── HIZLI-BASLANGIC.md      ← 5 dakikalık rehber
│   ├── TEST-SONUCLARI.md       ← Test raporları
│   ├── araclar/                ← BURADAN ÇALIŞTIRIN
│   │   ├── arsiv_yoneticisi.py
│   │   ├── interaktif_arayuz.py  ← ANA PROGRAM
│   │   ├── ornek_veri_yukle.py   ← ÖRNEK VERİLER
│   │   └── veriler/
│   │       └── sozler.json       ← VERİ DOSYASI
│   ├── dokumantasyon/
│   │   ├── README.md
│   │   └── MIMARI.md
│   └── veriler/
│       └── sozler.json
```

---

## ❗ Sorun Giderme

### Sorun: "python: command not found"

**Çözüm:**
```bash
# python3 kullanmayı deneyin
python3 --version

# Eğer bu da çalışmazsa Python'u kurun
# Windows: https://www.python.org/downloads/
# macOS: brew install python3
# Linux: sudo apt install python3
```

### Sorun: "ModuleNotFoundError"

**Çözüm:**
```bash
# Doğru klasörde olduğunuzdan emin olun
cd ataturk-arsivi/araclar

# Scripti bu klasörden çalıştırın
python3 interaktif_arayuz.py
```

### Sorun: "Permission denied"

**Çözüm (Linux/macOS):**
```bash
# Çalıştırma yetkisi verin
chmod +x interaktif_arayuz.py

# Veya python3 ile çalıştırın
python3 interaktif_arayuz.py
```

### Sorun: Türkçe karakterler düzgün görünmüyor

**Çözüm:**
```bash
# Windows için PowerShell kullanın veya
# Terminal kodlamasını UTF-8 yapın

# Linux/macOS: Terminal ayarlarından UTF-8 seçin
```

### Sorun: Veri dosyası bulunamıyor

**Çözüm:**
```bash
# Veriler otomatik oluşturulur, ama emin olmak için:
cd ataturk-arsivi/araclar

# İlk kez çalıştırıldığında otomatik oluşur
python3 ornek_veri_yukle.py
```

---

## 📱 Farklı Platformlarda Kullanım

### Windows

```cmd
# Command Prompt veya PowerShell kullanın
cd C:\Users\[KullaniciAdi]\Downloads\savasava034\ataturk-arsivi\araclar
python interaktif_arayuz.py
```

### macOS

```bash
# Terminal kullanın
cd ~/Downloads/savasava034/ataturk-arsivi/araclar
python3 interaktif_arayuz.py
```

### Linux

```bash
# Terminal kullanın
cd ~/Downloads/savasava034/ataturk-arsivi/araclar
python3 interaktif_arayuz.py
```

---

## 🎓 Öğrenme Yolu

### Yeni Başlayanlar İçin (15 dakika)

1. **0-5 dk**: Dosyaları indirin
2. **5-10 dk**: Örnek verileri yükleyin
3. **10-15 dk**: İnteraktif menüyü keşfedin

### Deneyimli Kullanıcılar İçin (5 dakika)

1. Repository'yi klonlayın
2. Python API'sini kullanın
3. Kendi scriptlerinizi yazın

---

## 💡 İpuçları

### ✅ Başarı İçin:
- Python 3.7+ kullanın
- `ataturk-arsivi/araclar` klasöründen çalıştırın
- İlk önce örnek verileri yükleyin
- Dokümantasyonu okuyun

### ❌ Yapmayın:
- Python 2 kullanmayın
- Dosyaları taşımayın (klasör yapısını koruyun)
- Veri dosyasını manuel olarak düzenlemeyin

---

## 📚 Daha Fazla Yardım

- **Hızlı Başlangıç**: [HIZLI-BASLANGIC.md](HIZLI-BASLANGIC.md)
- **Detaylı Kullanım**: [README.md](README.md)
- **Teknik Detaylar**: [dokumantasyon/MIMARI.md](dokumantasyon/MIMARI.md)
- **Test Sonuçları**: [TEST-SONUCLARI.md](TEST-SONUCLARI.md)

---

## 🎉 Başarıyla Kuruldu!

Eğer bu adımları tamamladıysanız, artık Atatürk Arşiv Sistemi'ni kullanmaya hazırsınız!

```bash
# Şimdi çalıştırın:
cd ataturk-arsivi/araclar
python3 interaktif_arayuz.py
```

---

## 📞 Destek

Sorun yaşıyorsanız:
1. Bu dosyayı tekrar okuyun
2. [Sorun Giderme](#-sorun-giderme) bölümüne bakın
3. GitHub Issues'da soru sorun

---

<div align="center">

**🇹🇷 Atatürk Arşiv Sistemi**

"Hayatta en hakiki mürşit ilimdir, fendir."  
— Mustafa Kemal Atatürk

**Kullanıma Hazır! Hemen başlayın!** ✨

</div>
