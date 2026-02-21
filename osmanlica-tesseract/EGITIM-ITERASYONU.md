# Eğitim İterasyonu Takip Belgesi

## 📋 Genel Bakış

Bu belge, Osmanlıca Tesseract OCR modelinin eğitim iterasyonlarını ve iyileştirme sürecini takip eder.

**Hedef:** %90+ doğruluk oranı

---

## 🎯 İterasyon Stratejisi

### Aşama 1: Baseline (Başlangıç Noktası)
**Model:** Arapça (ara.traineddata)  
**Eğitim:** Yok (pre-trained kullanım)  
**Hedef:** Mevcut durumu ölç

### Aşama 2: Ön İşleme Optimizasyonu
**Odak:** Görüntü kalitesini artır  
**Yöntemler:**
- CLAHE kontrast artırma
- Otsu binarization
- Denoise (fastNlMeans)
- Deskewing

### Aşama 3: Fine-Tuning
**Model:** ara → osmanlica  
**Veri:** 30-50 kaliteli sayfa  
**İterasyon:** 5,000-10,000

### Aşama 4: Full Training (İsteğe Bağlı)
**Model:** Sıfırdan eğitim  
**Veri:** 200-500 sayfa  
**İterasyon:** 50,000+

---

## 📊 İterasyon Kayıtları

### İterasyon #0: Proje Başlangıcı
**Tarih:** 2026-02-16  
**Durum:** Test altyapısı kuruldu

**Yapılan:**
- ✅ 57 test eklendi
- ✅ Test coverage %75.4
- ✅ Preprocessing testleri %100 geçti
- ✅ Training yapılandırma testleri %100 geçti

**Test Sonuçları:**
```
Toplam Test: 57
Başarılı: 43 (%75.4)
Başarısız: 2 (API uyumsuzluğu)
Hata: 12 (Tesseract gerekli)
```

**Eksikler:**
- ❌ Tesseract kurulu değil
- ❌ Arapça model yok
- ❌ Eğitim yapılmadı
- ❌ Baseline doğruluk bilinmiyor

**Sonraki Adım:** Tesseract kurulumu ve baseline ölçümü

---

### İterasyon #1: Baseline Ölçümü (Planlanıyor)
**Tarih:** TBD  
**Model:** ara.traineddata (Arapça)  
**Ön İşleme:** Varsayılan

**Planlanan Metrikler:**
- Character Accuracy: ? %
- Word Accuracy: ? %
- CER (Character Error Rate): ? %
- WER (Word Error Rate): ? %

**Beklenen Sonuç:** %60-75 doğruluk

**Test Edilecek Örnekler:**
1. sample001_besmele.png - بسم الله الرحمن الرحیم
2. sample002_hamd.png - العالمین رب لله الحمد
3. sample003_rahman.png - الرحیم الرحمن
4. sample004_malik.png - الدین یوم مالک
5. sample005_iyyake.png - نعبد إیاک

**Komutlar:**
```bash
# Tesseract kur
sudo apt-get install tesseract-ocr tesseract-ocr-ara

# Baseline değerlendirme
python3 scripts/quick_train.py --action evaluate --lang ara

# Sonuçları kaydet
python3 scripts/quick_train.py --action evaluate --save-results
```

---

### İterasyon #2: Ön İşleme Optimizasyonu (Planlanıyor)
**Tarih:** TBD  
**Model:** ara.traineddata  
**Ön İşleme:** Optimize edilmiş

**Planlanan İyileştirmeler:**
- CLAHE kontrast artırma
- Adaptif binarization yerine Otsu
- Deskewing etkin
- Denoise güç artırımı

**Hedef İyileştirme:** +5-10% doğruluk

**Test Edilecek Parametreler:**
```python
preprocess_params = {
    'denoise': True,
    'denoise_strength': [7, 10, 15],  # Test edilecek
    'binarize': True,
    'binarize_method': ['otsu', 'adaptive'],  # Karşılaştır
    'enhance_contrast': True,
    'enhance_method': 'clahe',
    'deskew': True
}
```

**Beklenen Sonuç:** %70-80 doğruluk

---

### İterasyon #3: İlk Fine-Tuning (Planlanıyor)
**Tarih:** TBD  
**Model:** ara → osmanlica_v1  
**Veri:** 30-50 sayfa (Wikisource)

**Eğitim Parametreleri:**
```json
{
  "base_model": "ara",
  "max_iterations": 5000,
  "learning_rate": 0.0001,
  "target_error_rate": 0.15
}
```

**Hedef:** %80-85 doğruluk

**Veri Kaynakları:**
- Tanzimat Fermanı (5 sayfa)
- Gülhane Hatt-ı Hümayunu (3 sayfa)
- Kanun-i Esasi (20 sayfa)

**Komutlar:**
```bash
# Eğitim verilerini hazırla
python3 scripts/prepare_training_data.py

# Fine-tuning başlat
python3 scripts/train_tesseract.py \
    --action finetune \
    --base-model ara \
    --model-name osmanlica_v1 \
    --max-iterations 5000

# Değerlendir
python3 scripts/evaluate.py --model osmanlica_v1
```

---

### İterasyon #4: Parametre Optimizasyonu (Planlanıyor)
**Tarih:** TBD  
**Model:** osmanlica_v2  
**Fokus:** Learning rate ve iterasyon sayısı

**Test Edilecek Kombinasyonlar:**
```
Senaryo A: lr=0.0001, iter=10000
Senaryo B: lr=0.00005, iter=15000
Senaryo C: lr=0.0002, iter=7500
```

**Hedef:** %85-90 doğruluk

---

### İterasyon #5: Hedef Doğruluk (Planlanıyor)
**Tarih:** TBD  
**Model:** osmanlica_v3  
**Hedef:** %90-94 doğruluk

**İyileştirmeler:**
- En iyi ön işleme parametreleri
- En iyi eğitim parametreleri
- Veri artırma (augmentation)
- Hard negative mining

---

## 📈 Doğruluk Takibi

### Hedef Doğruluk Seviyeleri

| Seviye | Char Acc | Word Acc | CER | WER | Kullanım |
|--------|----------|----------|-----|-----|----------|
| Baseline | 60-75% | 50-65% | 25-40% | 35-50% | Test |
| İyi | 75-85% | 65-75% | 15-25% | 25-35% | Gelişim |
| Çok İyi | 85-90% | 75-85% | 10-15% | 15-25% | Kullanılabilir |
| Mükemmel | 90-95% | 85-90% | 5-10% | 10-15% | Üretim |
| Süper | 95%+ | 90%+ | <5% | <10% | Profesyonel |

### İlerleme Grafiği (Planlanıyor)

```
%100 |                                         * (Hedef)
 %95 |                                       *
 %90 |                                     *
 %85 |                                   *
 %80 |                                 *
 %75 |                               *
 %70 |                             *
 %65 |                           * (İlk fine-tuning)
 %60 |                         * (Baseline)
     +--------------------------------------------------------
      #0    #1    #2    #3    #4    #5    #6    #7    #8
       (Şimdi)                              (Hedef)
```

---

## 🔬 Detaylı Analiz Şablonu

### Her İterasyon İçin Doldurulacak

#### 1. Temel Bilgiler
- **Tarih:**
- **İterasyon No:**
- **Model:**
- **Veri Seti Boyutu:**
- **Süre:**

#### 2. Metrikler
```
Character Accuracy: ___%
Word Accuracy: ___%
Character Error Rate (CER): ___%
Word Error Rate (WER): ___%
Levenshtein Distance (avg): ___
```

#### 3. Örnek Bazlı Sonuçlar
```
sample001: Char=___%, Word=___%, CER=___%
sample002: Char=___%, Word=___%, CER=___%
sample003: Char=___%, Word=___%, CER=___%
sample004: Char=___%, Word=___%, CER=___%
sample005: Char=___%, Word=___%, CER=___%
```

#### 4. Karşılaştırma
```
Önceki İterasyona Göre:
  Character Acc: +___% veya -___%
  Word Acc: +___% veya -___%
  CER: +___% veya -___%
```

#### 5. Gözlemler
- En iyi sonuç veren örnek:
- En kötü sonuç veren örnek:
- Ortak hatalar:
- Başarılı yönler:

#### 6. Sonraki Adımlar
- [ ] Yapılacak iyileştirme 1
- [ ] Yapılacak iyileştirme 2
- [ ] Test edilecek parametre 1
- [ ] Test edilecek parametre 2

---

## 📝 Hata Analizi

### Yaygın Hata Türleri

#### 1. Karakter Karışıklıkları
```
Karıştırılan: ك ↔ ک
Karıştırılan: ی ↔ ي
Karıştırılan: ه ↔ ة
```

#### 2. Noktalama İşaretleri
```
Eksik: .
Eksik: ،
Yanlış: : → ؛
```

#### 3. Boşluklar
```
Eksik boşluk: "الله" → "ال له"
Fazla boşluk: "بسم" → "ب سم"
```

---

## 🎯 İyileştirme Stratejileri

### 1. Veri Kalitesi
- ✅ Yüksek DPI (300-600)
- ✅ Net görüntüler
- ✅ Doğru ground truth
- ✅ Çeşitlilik (farklı dönemler, stiller)

### 2. Ön İşleme
- Denoise güç ayarı
- Binarization threshold
- Kontrast optimizasyonu
- Deskewing hassasiyeti

### 3. Eğitim
- Learning rate fine-tuning
- İterasyon sayısı artırma
- Batch size optimizasyonu
- Regularization

### 4. Post-Processing
- Sözlük kontrolü
- Dil modeli
- N-gram düzeltme
- Context-aware corrections

---

## 📊 Sonuç Raporlama

### JSON Format
```json
{
  "iteration": 1,
  "date": "2026-02-16",
  "model": "ara",
  "preprocessing": {
    "denoise": true,
    "binarize": true,
    "enhance_contrast": true
  },
  "results": {
    "character_accuracy": 68.5,
    "word_accuracy": 55.2,
    "cer": 31.5,
    "wer": 44.8
  },
  "samples": [
    {
      "file": "sample001_besmele.png",
      "accuracy": 72.1
    }
  ],
  "notes": "Baseline ölçümü tamamlandı"
}
```

---

## 🚀 Hızlı Komutlar

### Tam Test Döngüsü
```bash
# 1. Testleri çalıştır
python3 run_tests.py

# 2. Baseline değerlendir
python3 scripts/quick_train.py --action evaluate

# 3. Ön işleme test et
python3 scripts/quick_train.py --action preprocess

# 4. Karşılaştırma yap
python3 scripts/quick_train.py --action compare

# 5. Sonuçları kaydet
python3 scripts/quick_train.py --action all --save-results
```

### Eğitim Başlat
```bash
# Fine-tuning
python3 scripts/train_tesseract.py --action finetune --base-model ara

# Değerlendir
python3 scripts/evaluate.py --test-dir sample-data/images --gt-dir sample-data/ground-truth
```

---

## 📌 Notlar

- Her iterasyonda sonuçları `training_results.json` dosyasına kaydet
- Önemli bulguları bu belgede dokümante et
- Grafikleri ve görselleştirmeleri ekle
- Başarılı parametreleri işaretle

---

**Son Güncelleme:** 2026-02-16  
**Durum:** İterasyon #0 tamamlandı, #1 planlama aşamasında  
**Hedef:** %90-94 doğruluk
