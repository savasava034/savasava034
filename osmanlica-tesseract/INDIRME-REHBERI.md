# 📥 İNDİRME VE KURULUM REHBERİ

**Osmanlıca Tesseract OCR Projesi**

---

## 🎯 HIZLI BAŞLANGIÇ

Projeyi indirmek ve kullanmaya başlamak için **3 adım**:

```bash
# 1. İndir
git clone https://github.com/savasava034/savasava034.git

# 2. Klasöre gir
cd savasava034/osmanlica-tesseract

# 3. Gereksinimleri kur
pip install -r requirements.txt
```

**HAZIR!** Artık kullanabilirsiniz! 🎉

---

## 📥 İNDİRME YÖNTEMLERİ

### YÖNTEM 1: ZIP Dosyası (En Kolay) 💚

**GitHub'dan direkt indirme:**

1. Şu adrese gidin: https://github.com/savasava034/savasava034
2. Yeşil **"Code"** butonuna tıklayın
3. **"Download ZIP"** seçeneğini tıklayın
4. İndirilen ZIP dosyasını açın
5. `osmanlica-tesseract` klasörüne girin

**Avantajları:**
- ✅ En basit yöntem
- ✅ Git bilgisi gerektirmez
- ✅ Tek tıkla indirilir

**Dezavantajları:**
- ❌ Güncellemeleri manuel indirmeniz gerekir
- ❌ Git geçmişi dahil değil

---

### YÖNTEM 2: Git Clone (Önerilen) 🚀

**Terminal/Komut İstemi ile:**

```bash
# Repository'yi klonla
git clone https://github.com/savasava034/savasava034.git

# Proje klasörüne gir
cd savasava034/osmanlica-tesseract

# Dosyaları listele
ls -la
```

**Avantajları:**
- ✅ Güncellemeleri kolayca çekebilirsiniz (`git pull`)
- ✅ Git geçmişi dahil
- ✅ Daha profesyonel yaklaşım
- ✅ Katkı yapabilirsiniz

**Dezavantajları:**
- ❌ Git kurulu olmalı
- ❌ Terminal bilgisi gerekir (temel)

---

## 📦 NE İNDİRECEKSİNİZ?

### Dosya İçeriği

**Eğitim Verileri (200 sayfa):**
- `training-data/nutuk-osmanli/` - 35 sayfa Nutuk
- `training-data/nutuk-ek-sayfalar/` - 20 sayfa ek Nutuk
- `training-data/real-historical/` - 13 tarihi belge
- `training-data/edebiyat-metinleri/` - 15 edebiyat metni
- `training-data/kanun-metinleri/` - 10 kanun metni
- `training-data/dini-metinler/` - 10 dini metin
- `training-data/tarih-metinleri/` - 15 tarih metni
- `training-data/gazete-dergi/` - 19 gazete/dergi
- `training-data/tip-metinleri/` - 10 tıp metni
- `training-data/mimari-metinler/` - 10 mimari metin
- `training-data/mektuplar/` - 12 mektup
- `training-data/bilim-metinleri/` - 16 bilim metni
- `training-data/padisah-fermanlari/` - 15 ferman

**Python Scriptleri (17 dosya):**
- `osmanlica_ocr.py` - Ana OCR motoru
- `preprocess.py` - Ön işleme
- `train_tesseract.py` - Model eğitimi
- `evaluate.py` - Değerlendirme
- `auto_train_complete.py` - Otomatik eğitim
- `continuous_training.py` - Sürekli eğitim
- Ve diğerleri...

**Test Dosyaları (60+ test):**
- `tests/test_preprocess.py`
- `tests/test_evaluate.py`
- `tests/test_ocr.py`
- `tests/test_training.py`
- `tests/test_integration.py`

**Dokümantasyon (35+ belge):**
- README.md - Ana dokümantasyon
- HIZLI-BASLANGIC.md - Hızlı başlangıç
- EGITIM-KONFIGURASYONU.md - Eğitim ayarları
- TURKCE-OZET.md - Türkçe özet
- Ve 30+ diğer belge...

**Toplam:**
- **Dosya sayısı:** 450+ dosya
- **Boyut:** ~2 MB (sıkıştırılmamış)
- **Karakter:** 60,661 (ground truth)

---

## 💻 SİSTEM GEREKSİNİMLERİ

### Minimum Gereksinimler

**İşletim Sistemi:**
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Ubuntu 20.04+
- ✅ Diğer Linux dağıtımları

**Yazılım:**
- ✅ Python 3.8 veya üzeri
- ✅ pip (Python paket yöneticisi)
- ✅ Git (opsiyonel, ama önerilen)

**Donanım:**
- 💾 2 GB boş disk alanı
- 🧠 4 GB RAM (minimum)
- 🧠 8 GB RAM (önerilen)
- 🖥️ CPU: Modern işlemci (herhangi)

**Eğitim için ek:**
- ⏱️ 8-12 saat sürekli çalışma
- 🖥️ 8 GB RAM (önerilen)
- 💾 5 GB boş disk (model için)

---

## 🔧 KURULUM ADIMLARI

### Adım 1: Projeyi İndirin

**Yöntem A - ZIP:**
```bash
# ZIP'i indirip açtıktan sonra
cd savasava034/osmanlica-tesseract
```

**Yöntem B - Git:**
```bash
git clone https://github.com/savasava034/savasava034.git
cd savasava034/osmanlica-tesseract
```

### Adım 2: Python Bağımlılıklarını Kurun

```bash
# requirements.txt'ten kur
pip install -r requirements.txt
```

**İçerikler:**
- pytesseract
- Pillow
- opencv-python
- numpy
- ve diğerleri...

### Adım 3: Tesseract OCR'ı Kurun

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-ara
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
1. https://github.com/UB-Mannheim/tesseract/wiki adresine gidin
2. Installer'ı indirin
3. Kurun
4. PATH'e ekleyin

### Adım 4: Kurulumu Doğrulayın

```bash
# Python sürümü
python3 --version
# Çıktı: Python 3.8.0 veya üzeri

# Tesseract sürümü
tesseract --version
# Çıktı: tesseract 4.0.0 veya üzeri

# Paketleri kontrol et
pip list | grep tesseract
pip list | grep opencv
```

---

## ✅ DOĞRULAMA VE TEST

### Temel Testler

```bash
# Test suite'i çalıştır
python3 run_tests.py

# Demo çalıştır
python3 demo.py

# Örnek OCR testi
python3 scripts/osmanlica_ocr.py sample-data/images/sample001_besmele.png
```

**Beklenen çıktı:**
```
Tests: 60+
Passed: 43+ (Tesseract olmadan)
Failed: Tesseract gerekli testler

Demo: Menü gösterilmeli
OCR: Tesseract gerekli
```

---

## 🚀 İLK ÇALIŞTIRMA

### Demo Modu

```bash
# İnteraktif demo
python3 demo.py

# Seçenekler:
# 1. Örnek görüntüleri tanı
# 2. Kendi görüntünüzü test edin
# 3. Toplu işleme
# 4. Model eğitimi
```

### Manuel OCR Testi

```bash
# Tek görüntü
python3 scripts/osmanlica_ocr.py resim.jpg

# Toplu işleme
python3 scripts/osmanlica_ocr.py --batch klasor/
```

### Model Eğitimi

```bash
# Otomatik eğitim (8-12 saat)
python3 scripts/auto_train_complete.py --mode full

# Hızlı test (5 dakika)
python3 scripts/auto_train_complete.py --mode test
```

---

## ❓ SIK SORULAN SORULAR (SSS)

### S1: İndirme süresi ne kadar?
**C:** İnternet hızınıza bağlı:
- Hızlı (100 Mbps): 10-20 saniye
- Orta (10 Mbps): 1-2 dakika
- Yavaş (1 Mbps): 10-15 dakika

### S2: Tüm dosyalar geliyor mu?
**C:** EVET! 200 sayfa veri, tüm kodlar, tüm belgeler dahil. 450+ dosya.

### S3: Lisans var mı?
**C:** Evet, MIT License. Özgürce kullanabilirsiniz.

### S4: İnternet olmadan kullanabilir miyim?
**C:** Evet! İndirdikten sonra offline çalışır.

### S5: Güncellemeleri nasıl alırım?
**C:** Git kullanıyorsanız: `git pull`
ZIP kullanıyorsanız: Yeniden indirin

### S6: Hangi işletim sisteminde çalışır?
**C:** Windows, macOS, Linux - hepsinde çalışır!

### S7: Eğitim verilerini değiştirebilir miyim?
**C:** Evet! Kendi verilerinizi ekleyebilirsiniz.

### S8: Ticari kullanım yapabilir miyim?
**C:** Evet! MIT lisansı ticari kullanıma izin verir.

### S9: Kurulum ne kadar sürer?
**C:** 2-5 dakika (Python paketleri için)

### S10: Yardıma ihtiyacım olursa?
**C:** Belgelere bakın veya issue açın GitHub'da.

---

## 🔧 SORUN GİDERME

### Hata: "Git bulunamadı"
**Çözüm:** Git'i kurun: https://git-scm.com/downloads

### Hata: "Python bulunamadı"
**Çözüm:** Python 3.8+ kurun: https://www.python.org/downloads/

### Hata: "pip bulunamadı"
**Çözüm:** 
```bash
python3 -m ensurepip --upgrade
```

### Hata: "Tesseract bulunamadı"
**Çözüm:** Tesseract OCR kurun (yukarıdaki adımlara bakın)

### Hata: "Permission denied"
**Çözüm:** 
```bash
chmod +x scripts/*.py
# veya
python3 scripts/script_adi.py
```

### Hata: "Module not found"
**Çözüm:**
```bash
pip install -r requirements.txt
```

---

## 📞 DESTEK VE YARDIM

### Belgeler

**Ana belgeler:**
- README.md - Genel bakış
- TURKCE-OZET.md - Basit Türkçe özet
- HIZLI-BASLANGIC.md - Hızlı başlangıç
- EGITIM-DURUM-SSS.md - Eğitim durumu

**Eğitim belgeleri:**
- 5-GUNLUK-PLAN.md - 5 günlük eğitim planı
- YUZDE-90-PLUS-REHBER.md - %90+ doğruluk rehberi
- EGITIM-KONFIGURASYONU.md - Eğitim ayarları

**Teknik belgeler:**
- docs/API.md - API dokümantasyonu
- docs/EGITIM.md - Eğitim rehberi
- docs/OPTIMIZASYON.md - Optimizasyon

### İletişim

**GitHub:**
- Repository: https://github.com/savasava034/savasava034
- Issues: Sorun bildirin veya soru sorun

**Belgeler:**
- 35+ Türkçe belge mevcut
- Her konuda detaylı açıklama

---

## 🎓 EK KAYNAKLAR

### Video Öğreticiler (Planlanıyor)

1. İndirme ve kurulum
2. İlk çalıştırma
3. Model eğitimi
4. Kullanım örnekleri

### İlgili Projeler

- **Tesseract OCR:** https://github.com/tesseract-ocr/tesseract
- **Python:** https://www.python.org/
- **Git:** https://git-scm.com/

### Önerilen Okuma

1. README.md - İlk okumanız gereken
2. TURKCE-OZET.md - Basit açıklama
3. HIZLI-BASLANGIC.md - 15 dakikada başlangıç
4. 5-GUNLUK-PLAN.md - Kapsamlı eğitim

---

## 🎉 ÖZET

### Hızlı Özet

**İNDİRME:**
- GitHub: https://github.com/savasava034/savasava034
- ZIP veya Git Clone

**KURULUM:**
```bash
pip install -r requirements.txt
sudo apt-get install tesseract-ocr tesseract-ocr-ara
```

**ÇALIŞTIRMA:**
```bash
python3 demo.py
```

**SONUÇ:**
- ✅ Tüm dosyalar indirildi
- ✅ Kurulum tamamlandı
- ✅ Kullanıma hazır!

---

## 💚 TEŞEKKÜRLER

Bu projeyi indirdiğiniz ve kullandığınız için teşekkürler!

**İyi eğitimler!** 🚀📥

---

**Tarih:** 2026-02-21  
**Versiyon:** 1.0  
**Durum:** Güncel ve kullanıma hazır ✅  
**Boyut:** ~2 MB, 450+ dosya  
**Link:** https://github.com/savasava034/savasava034
