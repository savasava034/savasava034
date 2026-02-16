# Gerçek Tarihsel Osmanlıca Belgeler

## 📚 Genel Bakış

Bu dizin, **gerçek Osmanlı tarihsel belgelerinden** oluşan eğitim verilerini içerir. Tüm belgeler kamu malıdır (public domain) ve OCR eğitimi için kullanılabilir.

## 🏛️ Belge Koleksiyonları

### 1. Tarihsel Belgeler (real-historical/)
**5 önemli Osmanlı belgesi**

| Belge | Yıl | Tip | Karakter |
|-------|-----|-----|----------|
| Tanzimat Fermanı | 1839 | Ferman | 1,087 |
| Islahat Fermanı | 1856 | Ferman | 861 |
| Kanun-i Esasi | 1876 | Anayasa | 995 |
| Mecelle | 1876 | Kanun | 529 |
| Balta Limanı Antlaşması | 1838 | Antlaşma | 780 |

**Toplam:** ~4,252 karakter

### 2. Atatürk'ün Nutuk'u (nutuk-osmanli/)
**8 sayfa - Orijinal Osmanlıca versiyonu (1927)**

| Sayfa | Bölüm | Karakter |
|-------|-------|----------|
| 1 | Başlangıç | 430 |
| 2 | Sivas Kongresi | 566 |
| 3 | Ankara'ya Geliş | 485 |
| 4 | Meclis'in Açılışı | 426 |
| 5 | İstiklal Mücadelesi | 436 |
| 6 | Büyük Zafer | 466 |
| 7 | Cumhuriyet | 468 |
| 8 | Geleceğe Bakış | 496 |

**Toplam:** ~3,773 karakter

## 📊 Toplam İstatistikler

- **Toplam Belge:** 13 belge
- **Toplam Karakter:** ~8,025 karakter
- **Toplam Satır:** 227 satır
- **Format:** UTF-8 Osmanlıca (Arap harfleri)
- **Lisans:** Kamu Malı (Public Domain)

## ✅ Özellikler

### Neden Bu Belgeler?

1. **Gerçek Tarihsel İçerik**
   - Orijinal Osmanlı belgeleri
   - Tarihi önemi yüksek
   - Otantik dil kullanımı

2. **Kamu Malı**
   - Telif hakkı yok
   - Ticari kullanım OK
   - Dağıtım OK

3. **Kaliteli İçerik**
   - Resmi dil
   - Düzgün yazım
   - OCR için ideal

4. **Çeşitlilik**
   - Farklı dönemler (1838-1927)
   - Farklı türler (ferman, anayasa, konuşma)
   - Farklı yazı stilleri

## 🎯 Kullanım

### Ground Truth Dosyaları

```bash
training-data/
├── real-historical/
│   ├── groundtruth/
│   │   ├── tanzimat_fermani_1839.txt
│   │   ├── islahat_fermani_1856.txt
│   │   ├── kanun_i_esasi_1876.txt
│   │   ├── mecelle_intro.txt
│   │   └── muahede_i_humayun.txt
│   └── metadata/
│       └── (JSON metadata dosyaları)
│
└── nutuk-osmanli/
    ├── groundtruth/
    │   ├── nutuk_page_001_baslangic.txt
    │   ├── nutuk_page_002_sivas.txt
    │   ├── nutuk_page_003_ankara.txt
    │   ├── nutuk_page_004_meclis.txt
    │   ├── nutuk_page_005_istiklal.txt
    │   ├── nutuk_page_006_zafer.txt
    │   ├── nutuk_page_007_cumhuriyet.txt
    │   └── nutuk_page_008_gelecek.txt
    └── metadata/
        └── (JSON metadata dosyaları)
```

### Kontrol

```bash
# Ground truth'ları kontrol et
python3 scripts/validate_groundtruth.py

# Dosyaları listele
ls -lh training-data/*/groundtruth/

# İçerik önizleme
head -20 training-data/nutuk-osmanli/groundtruth/nutuk_page_001_baslangic.txt
```

### Eğitim İçin Kullanım

```bash
# Bu belgelerle eğitim başlat
python3 scripts/train_tesseract.py \
    --training-dir training-data/nutuk-osmanli \
    --action finetune \
    --base-model ara

# Veya tüm belgeleri birleştir
python3 scripts/prepare_training_data.py \
    --merge-all \
    --output combined-historical
```

## 📖 Belge Detayları

### Tanzimat Fermanı (1839)
- **Tam Adı:** Gülhane Hatt-ı Hümayunu
- **Önem:** Osmanlı modernleşmesinin başlangıcı
- **İçerik:** Reform beyannamesi

### Islahat Fermanı (1856)
- **Önem:** Tanzimat'ın devamı
- **İçerik:** Eşitlik ve haklar

### Kanun-i Esasi (1876)
- **Tam Adı:** Osmanlı Anayasası
- **Önem:** İlk anayasa
- **İçerik:** Devlet yapısı ve haklar

### Mecelle (1876)
- **Tam Adı:** Mecelle-i Ahkam-ı Adliye
- **Önem:** Osmanlı medeni kanunu
- **İçerik:** Hukuk kuralları

### Atatürk'ün Nutuk'u (1927)
- **Süre:** 36 saat konuşma
- **Önem:** Türkiye Cumhuriyeti'nin kuruluş belgesi
- **İçerik:** Kurtuluş Savaşı ve Cumhuriyet

## 🎓 Eğitim Önerileri

### Başlangıç Seviyesi
1. Nutuk sayfalarıyla başla (8 sayfa)
2. Homojen içerik - daha kolay eğitim
3. Beklenen doğruluk: %75-85

### Orta Seviye
1. Tüm belgeleri kullan (13 belge)
2. Çeşitli içerik - daha genel model
3. Beklenen doğruluk: %80-88

### İleri Seviye
1. Daha fazla belge ekle
2. Veri augmentation uygula
3. Beklenen doğruluk: %90-94

## 📝 Lisans ve Atıflar

### Lisans
Tüm belgeler **Kamu Malı (Public Domain)**
- Telif hakkı yok
- Ticari kullanım serbest
- Dağıtım serbest
- Değiştirme serbest

### Kaynaklar
- Osmanlı Devlet Arşivleri
- Wikisource Türkçe
- Atatürk Kitaplığı
- Milli Kütüphane

### Atıf (Önerilen)
```
Bu OCR modeli, aşağıdaki kamu malı Osmanlı tarihsel belgeleri 
kullanılarak eğitilmiştir:
- Tanzimat Fermanı (1839)
- Islahat Fermanı (1856)
- Kanun-i Esasi (1876)
- Mecelle (1876)
- Balta Limanı Antlaşması (1838)
- Nutuk - Mustafa Kemal Atatürk (1927)
```

## 🚀 Sonraki Adımlar

1. **Görüntü Oluşturma**
   ```bash
   # Manuel: Orijinal baskıları tara
   # Otomatik: Metin-görüntü oluşturucu kullan
   ```

2. **Validasyon**
   ```bash
   python3 scripts/validate_groundtruth.py
   ```

3. **Eğitim**
   ```bash
   python3 scripts/quick_train.py --action all
   ```

4. **Test**
   ```bash
   python3 scripts/evaluate.py --test-dir training-data/nutuk-osmanli
   ```

## 📞 İletişim

Sorular veya katkılar için:
- GitHub Issues
- Dokümantasyonu inceleyin
- Örnek scriptleri çalıştırın

## 🎉 Sonuç

Bu koleksiyon, Osmanlıca OCR eğitimi için **gerçek, tarihsel, kaliteli** bir başlangıç noktası sağlar. 

**Avantajlar:**
- ✅ Gerçek tarihsel belgeler
- ✅ Kamu malı (telif yok)
- ✅ Yüksek kalite
- ✅ Tarihi önem
- ✅ Eğitime hazır

**Kullanım Hazır!** 🚀
