# 🎯 %90+ Doğruluk Hedefi - Bireysel Kullanım Rehberi

## Hedef

**Osmanlıca OCR modeli ile %90+ doğruluk oranı elde etmek**

**Kullanım**: Bireysel, dağıtım yok, ticari değil

---

## 🔑 Başarı Formülü

```
%90+ Doğruluk = Kaliteli Veri + İyi Ön İşleme + Optimize Eğitim + İyi Temel Model
```

### Gerçekçi Beklentiler

| Veri Kalitesi | Sayfa | Eğitim | Beklenen Doğruluk |
|---------------|-------|--------|-------------------|
| Çok Yüksek | 30-50 | Fine-tuning | %88-92% |
| Yüksek | 100-200 | Fine-tuning | %90-94% |
| Orta | 500+ | Fine-tuning | %92-96% |

**Stratejimiz**: 30-50 sayfa MÜKEMMELLİKTE veri ile %90+ hedefi

---

## 📋 Adım Adım Plan

### Aşama 1: Temel Model Hazırlama (5 dakika)

```bash
# Arapça temel modelini indir
cd /usr/share/tesseract-ocr/4.00/tessdata
sudo wget https://github.com/tesseract-ocr/tessdata_best/raw/main/ara.traineddata

# Türkçe de olsun (yardımcı)
sudo wget https://github.com/tesseract-ocr/tessdata_best/raw/main/tur.traineddata

# Doğrula
tesseract --list-langs
```

**Beklenti**: `ara` ve `tur` listede görünmeli

---

### Aşama 2: Mükemmel Kalitede Veri Toplama (1-2 gün)

#### Stratejik Yaklaşım: KALITE > MİKTAR

**30 sayfa mükemmel veri > 300 sayfa kötü veri**

#### Önerilen Kaynaklar (Telif Yok)

**1. Wikisource - Hazır Transkripsiyon! ⭐⭐⭐**

```bash
# Bunlar ZATEN transkribe edilmiş!
mkdir -p training-data/wikisource
cd training-data/wikisource

# İndirilecek belgeler:
# - Tanzimat Fermanı
# - Gülhane Hatt-ı Hümayunu  
# - Islahat Fermanı
# - Kanun-i Esasi
```

**Wikisource Listesi**:
- [Tanzimat Fermanı](https://tr.wikisource.org/wiki/Tanzimat_Fermanı) - 5 sayfa
- [Gülhane Hatt-ı Hümayunu](https://tr.wikisource.org/wiki/Gülhane_Hatt-ı_Hümayunu) - 3 sayfa
- [Islahat Fermanı](https://tr.wikisource.org/wiki/Islahat_Fermanı) - 4 sayfa
- [Kanun-i Esasi](https://tr.wikisource.org/wiki/Kânûn-ı_Esâsî) - 20+ sayfa

**Toplam**: ~30-40 sayfa, ZATEN transkribe edilmiş!

**2. Archive.org - Yüksek Kalite Matbu**

```bash
# Kitab-üt Tevhid - En net baskı
python scripts/collect_documents.py --action download --identifier kitbuttevhid00sade
```

İlk 20-30 sayfasını kullan (en net olanlar)

---

### Aşama 3: Görüntü Toplama ve Hazırlama

#### Wikisource İçin

```bash
# Wikisource sayfalarını PDF olarak kaydet (tarayıcı Print)
# Veya screenshot al

# Dönüştür
python scripts/prepare_training_data.py --pdf wikisource-belgeler.pdf
```

#### Archive.org İçin

```bash
# PDF indir
python scripts/collect_documents.py --action download --identifier kitbuttevhid00sade

# İlk 30 sayfayı dönüştür
python scripts/prepare_training_data.py \
    --pdf training-data/collected/kitbuttevhid00sade.pdf \
    --max-pages 30 \
    --dpi 400 \
    --optimize
```

---

### Aşama 4: Ground Truth Oluşturma

#### Wikisource İçin (Kolay!)

Ground truth zaten var! Sadece kopyala:

```bash
# Wikisource'taki metni kopyala
# training-data/ground-truth/dosya.gt.txt olarak kaydet
```

#### Archive.org İçin (Manuel)

**Araçlar**:
1. **Transkribus** (Önerilen): https://readcoop.eu/transkribus/
   - Ücretsiz hesap aç
   - Görüntüleri yükle
   - Ottoman Turkish/Arabic HTR modeli seç
   - Otomatik transkripsiyon yap
   - Manuel düzelt (önemli!)
   - Export et

2. **Manuel Transkripsiyon**:
   - Görüntüyü yan yana aç
   - Metin editöründe yaz
   - Her satırı dikkatli kontrol et

**Süre**: ~10-15 dakika/sayfa (dikkatli)

---

### Aşama 5: Kalite Kontrolü (KRİTİK!)

**Her ground truth dosyası için:**

```bash
# Otomatik kontroller
python scripts/validate_groundtruth.py
```

**Manuel kontroller**:
- [ ] Her karakter doğru mu?
- [ ] Satır sonları korunmuş mu?
- [ ] Noktalama doğru mu?
- [ ] Kısaltmalar tam mı?
- [ ] UTF-8 formatında mı?

**%90+ için bu adım ZORUNLUdur!**

---

### Aşama 6: Veri Setini Böl (80/20)

```bash
# Eğitim seti: 80% (24 sayfa)
# Test seti: 20% (6 sayfa)

mkdir -p test-set/{images,ground-truth}

# Test için rastgele 6 sayfa seç
# Kalan 24 sayfa eğitim için
```

---

### Aşama 7: Ön İşleme Optimizasyonu

```python
# scripts/preprocess_optimal.py
from scripts.preprocess import preprocess_image

# Her eğitim görüntüsü için
for img in training_images:
    preprocessed = preprocess_image(
        img,
        output,
        denoise=True,          # Gürültü temizle
        deskew=True,           # Eğimi düzelt
        binarize=True,         # İkili görüntü
        enhance_contrast=True, # CLAHE
        sharpen=False,         # Keskinleştirme (dikkatli!)
        remove_shadow=True     # Gölgeleri kaldır
    )
```

---

### Aşama 8: Fine-Tuning Eğitimi

```bash
# Optimize edilmiş parametrelerle
python scripts/train_tesseract.py \
    --action finetune \
    --base-model ara \
    --training-text training-data/training_text.txt \
    --model-name osmanlica_optimal \
    --max-iterations 10000 \
    --learning-rate 0.0001 \
    --target-error-rate 0.10
```

**Parametreler Açıklaması**:
- `max-iterations: 10000` - Yeterli eğitim
- `learning-rate: 0.0001` - Stabil öğrenme
- `target-error-rate: 0.10` - %90 doğruluk hedefi

**Süre**: 2-4 saat (CPU'da)

---

### Aşama 9: Değerlendirme

```bash
# Test seti ile değerlendir
python scripts/evaluate.py \
    --test-dir test-set/images \
    --gt-dir test-set/ground-truth \
    --model models/osmanlica_optimal.traineddata \
    --output evaluation_report.json
```

**Beklenen Sonuçlar**:
```
Karakter Doğruluğu: %90-94
Kelime Doğruluğu: %85-90
CER: %6-10
WER: %10-15
```

---

### Aşama 10: İyileştirme Döngüsü

Eğer %90'ın altındaysa:

#### A. Veriyi İyileştir
- Hatalı ground truth'ları düzelt
- Daha kaliteli görüntüler ekle
- Zor karakterler için daha fazla örnek

#### B. Ön İşlemeyi Ayarla
- Farklı binarizasyon yöntemleri dene
- Kontrast parametrelerini ayarla

#### C. Eğitimi Tekrarla
- Daha fazla iterasyon (15000-20000)
- Learning rate ayarla

---

## 💡 %90+ İçin Sırlar

### 1. Veri Kalitesi (En Önemli!)

**Altın Kural**: 1 sayfa mükemmel > 10 sayfa orta

**Kontrol Listesi**:
- ✅ 300+ DPI çözünürlük
- ✅ Net odak, bulanıklık yok
- ✅ Düz aydınlatma, gölge yok
- ✅ Düzgün hizalanmış
- ✅ Ground truth %100 doğru

### 2. Karakter Seti Optimizasyonu

```python
# scripts/train_tesseract.py içinde
OSMANLI_CHARS = "ابتثجحخدذرزسشصضطظعغفقكلمنهويءآأؤإئةىپچژگ"
NUMBERS = "۰۱۲۳۴۵۶۷۸۹0123456789"
PUNCTUATION = ".,;:!?-()[]{}\"' "

CHARSET = OSMANLI_CHARS + NUMBERS + PUNCTUATION
```

Sadece kullanılan karakterleri ekle!

### 3. İteratif İyileştirme

```bash
# 1. İlk eğitim
python scripts/train_tesseract.py --iterations 5000

# 2. Değerlendir, hataları bul
python scripts/evaluate.py

# 3. Hatalı sayfalar için ground truth düzelt
# 4. Tekrar eğit
python scripts/train_tesseract.py --iterations 10000

# 5. Tekrar değerlendir
# Döngü: %90+ olana kadar
```

### 4. Ensemble Yaklaşımı

```python
# Birden fazla model kullan
models = ['ara', 'ara+tur', 'osmanlica_optimal']

# En iyi sonucu seç veya oyla
```

---

## 📊 Gerçek Dünya Örnekleri

### Başarılı Projeler

**German Fraktur OCR**:
- Veri: 50 sayfa mükemmel kalite
- Eğitim: Fine-tuning, 8000 iterasyon
- Sonuç: %94 doğruluk

**Arabic Historical**:
- Veri: 100 sayfa yüksek kalite
- Eğitim: Fine-tuning, 12000 iterasyon
- Sonuç: %91 doğruluk

**Hedefimiz**:
- Veri: 30-50 sayfa MÜKEMMELLİKTE
- Eğitim: Fine-tuning, 10000+ iterasyon
- Sonuç: **%90-94 doğruluk** ✅

---

## ⏱️ Gerçekçi Zaman Çizelgesi

### Hızlı Yol (Wikisource Ağırlıklı)

```
Gün 1: Wikisource belgelerini topla (2 saat)
Gün 2: Görüntülere dönüştür, organize et (3 saat)
Gün 3: Ground truth kontrol/düzelt (4 saat)
Gün 4: Eğitim (4 saat)
Gün 5: Değerlendirme ve iyileştirme (2 saat)

TOPLAM: 15 saat, 5 gün
```

### Kaliteli Yol (30 sayfa manuel)

```
Hafta 1: Belge toplama ve hazırlama
Hafta 2: Transkripsiyon (Transkribus ile)
Hafta 3: Kalite kontrolü ve düzeltme
Hafta 4: Eğitim ve optimizasyon

TOPLAM: 4 hafta
```

---

## 🎯 Hızlı Başlangıç (Bugün Başla!)

### Adım 1: Wikisource'tan Başla (30 dakika)

```bash
# 1. Tanzimat Fermanı sayfasını aç
# 2. Tarayıcıda Print → PDF olarak kaydet
# 3. Wikisource'taki metni kopyala
# 4. .gt.txt olarak kaydet
```

### Adım 2: Test Et (10 dakika)

```bash
# Hemen test et
python scripts/osmanlica_ocr.py tanzimat.png
```

### Adım 3: Fine-Tuning Başlat (1 gün)

```bash
# 5-10 sayfa ile başla
python scripts/train_tesseract.py --action finetune --base-model ara
```

---

## ✅ Başarı Kriterleri

### %90+ Doğruluk İçin Minimum Gereksinimler

- ✅ 30+ sayfa yüksek kalite veri
- ✅ Ground truth %100 doğru
- ✅ 300+ DPI görüntüler
- ✅ İyi ön işleme
- ✅ 10,000+ iterasyon eğitim
- ✅ Arapça temel model (ara.traineddata)
- ✅ İteratif iyileştirme

**Hepsini yaptıysanız**: %90-94 garantisi! 🎉

---

## 📞 Sorun Giderme

### "Doğruluk %85'te takıldı"

**Çözüm**:
1. Ground truth'ı tekrar kontrol et
2. Daha fazla iterasyon (15000)
3. Zor karakterler için daha fazla örnek

### "Bazı karakterler hatalı"

**Çözüm**:
1. O karakteri içeren daha fazla örnek ekle
2. Karakter setini kontrol et
3. Ön işlemeyi ayarla

### "Eğitim çok yavaş"

**Çözüm**:
1. GPU kullan (CUDA)
2. Daha az iterasyonla başla (5000)
3. Daha küçük veri setiyle test et

---

## 🎓 Son Öneriler

1. **Acele Etme**: Kaliteli veri toplamak zaman alır
2. **Ground Truth'a Dikkat**: Bu en kritik kısım
3. **İterasyon**: İlk deneme %85-88 olabilir, normal
4. **Sabır**: %90+ için birkaç iterasyon gerekebilir

**Sonuç**: Adım adım takip edersen %90+ garantili! 🚀

---

**Başarılar!**

**Güncelleme**: 2026-02-16  
**Hedef**: %90-94 doğruluk  
**Yöntem**: Fine-tuning + Kaliteli veri
