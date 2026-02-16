# 🚀 Optimizasyon İpuçları

Bu dokümanda, Osmanlıca OCR doğruluğunu artırmak için çeşitli optimizasyon teknikleri bulunmaktadır.

## 📋 İçindekiler

1. [Görüntü Kalitesi Optimizasyonu](#görüntü-kalitesi-optimizasyonu)
2. [Ön İşleme Optimizasyonu](#ön-i̇şleme-optimizasyonu)
3. [Tesseract Parametreleri](#tesseract-parametreleri)
4. [Model Optimizasyonu](#model-optimizasyonu)
5. [Post-Processing](#post-processing)
6. [Performans İyileştirme](#performans-i̇yileştirme)

---

## Görüntü Kalitesi Optimizasyonu

### 1. DPI (Çözünürlük)

**Minimum**: 300 DPI
**Önerilen**: 400-600 DPI
**Optimum**: 600 DPI

```python
from scripts.preprocess import resize_image

# Görüntüyü 600 DPI'ya yükselt
image = cv2.imread('input.jpg')
high_res = resize_image(image, target_dpi=600, current_dpi=72)
```

### 2. Görüntü Boyutu

Tesseract en iyi şu boyutlarda çalışır:
- **Minimum harf yüksekliği**: 20 piksel
- **Optimal harf yüksekliği**: 30-40 piksel
- **Maksimum görüntü boyutu**: 10,000 x 10,000 piksel

```python
import cv2

def optimize_size(image, target_height=40):
    """Metin yüksekliğini optimize et"""
    # Ortalama harf yüksekliğini tahmin et
    # Gerekirse yeniden boyutlandır
    pass
```

### 3. Kontrast ve Parlaklık

```python
from scripts.preprocess import enhance_contrast

# CLAHE ile kontrast artırma
enhanced = enhance_contrast(image, method='clahe')
```

**Öneriler**:
- Arka plan ile metin arasında net kontrast
- Çok koyu veya çok açık değil
- Gölge ve yansıma yok

### 4. Gürültü Azaltma

```python
from scripts.preprocess import denoise_image

# Gürültü temizleme
clean = denoise_image(image, method='fastNlMeans')
```

**Ne zaman gerekli:**
- Eski, yıpranmış belgeler
- Düşük kaliteli taramalar
- Dijital gürültü

---

## Ön İşleme Optimizasyonu

### Kapsamlı Ön İşleme Pipeline

```python
from scripts.preprocess import preprocess_image

# En iyi sonuç için tüm adımlar
processed = preprocess_image(
    'input.jpg',
    'output.jpg',
    denoise=True,           # Gürültü temizle
    deskew=True,            # Eğriliği düzelt
    binarize=True,          # İkili görüntüye çevir
    enhance_contrast=True,  # Kontrastı artır
    sharpen=False,          # Keskinleştirme (dikkatli!)
    remove_shadow=True      # Gölgeleri kaldır
)
```

### Binarizasyon Yöntemleri

```python
from scripts.preprocess import binarize_image

# Yöntem 1: Otsu (genel amaçlı)
binary = binarize_image(gray, method='otsu')

# Yöntem 2: Adaptive (değişken aydınlatma)
binary = binarize_image(gray, method='adaptive')

# Yöntem 3: Simple (düz arka plan)
binary = binarize_image(gray, method='simple')
```

**Hangi yöntemi seçmeli:**
- **Otsu**: Düzgün aydınlatmalı belgeler
- **Adaptive**: Değişken aydınlatma, gölgeler
- **Simple**: Çok temiz, yüksek kontrastlı belgeler

### Eğrilik Düzeltme (Deskewing)

```python
from scripts.preprocess import deskew_image

# Otomatik eğrilik düzeltme
straightened = deskew_image(image)
```

**Kritik durumlar:**
- Telefon ile çekilmiş fotoğraflar
- Tarayıcıda yanlış yerleştirilmiş belgeler
- El ile tutulan kamera görüntüleri

### Morfolojik İşlemler

```python
import cv2
import numpy as np

# İnce çizgileri kalınlaştırma (dilation)
kernel = np.ones((2, 2), np.uint8)
dilated = cv2.dilate(binary, kernel, iterations=1)

# Gürültü noktalarını temizleme (erosion)
eroded = cv2.erode(binary, kernel, iterations=1)

# Closing (küçük boşlukları doldurma)
closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

# Opening (küçük gürültüleri temizleme)
opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
```

---

## Tesseract Parametreleri

### Page Segmentation Mode (PSM)

```python
# PSM değerleri ve kullanım alanları
psm_modes = {
    0: "Yalnızca yönlendirme ve script tespiti",
    1: "Otomatik sayfa segmentasyonu (OSD ile)",
    3: "Otomatik sayfa segmentasyonu (OSD yok) - VARSAYILAN",
    4: "Tek sütun metin",
    5: "Dikey hizalanmış tek tekdüze metin bloğu",
    6: "Tek düzgün metin bloğu",          # OSMANICA İÇİN EN İYİ
    7: "Tek metin satırı",
    8: "Tek kelime",
    9: "Daire içinde tek kelime",
    10: "Tek karakter",
    11: "Seyrek metin (rastgele sıra)",
    12: "OSD ile seyrek metin",
    13: "Ham satır (bypass)"
}

# Osmanlıca için önerilen
ocr = OsmanlicaOCR()
ocr.config = '--oem 3 --psm 6'  # LSTM + Tek metin bloğu
```

### OCR Engine Mode (OEM)

```python
oem_modes = {
    0: "Sadece eski motor",
    1: "Sadece sinir ağı",
    2: "Eski + LSTM motorları",
    3: "Varsayılan (LSTM)"  # EN İYİ
}

# Osmanlıca için
config = '--oem 3'  # LSTM motor kullan
```

### Whitelist ve Blacklist

```python
# Osmanlıca karakterleri
osmanli_chars = 'ابتثجحخدذرزسشصضطظعغفقكلمنهويءآأؤإئةىپچژگ'
rakamlar = '۰۱۲۳۴۵۶۷۸۹0123456789'
noktalama = '.,;:!?-()[]{}"\' '

# Sadece belirli karakterleri tanı
config = f'--oem 3 --psm 6 -c tessedit_char_whitelist={osmanli_chars}{rakamlar}{noktalama}'

# Belirli karakterleri hariç tut
config = f'--oem 3 --psm 6 -c tessedit_char_blacklist=@#$%^&*'
```

### Tesseract Konfigürasyon Değişkenleri

```python
# Gelişmiş konfigürasyon
config = """
--oem 3 --psm 6
-c textord_heavy_nr=1
-c textord_min_linesize=2.5
-c tosp_threshold_bias2=0
-c classify_enable_learning=0
-c classify_enable_adaptive_matcher=0
-c edges_use_new_outline_complexity=1
"""
```

---

## Model Optimizasyonu

### Dil Kombinasyonları

```python
# Tek dil
ocr = OsmanlicaOCR(language='ara')  # Sadece Arapça

# Çoklu dil (öncelik sırasına göre)
ocr = OsmanlicaOCR(language='ara+tur')  # Arapça + Türkçe
ocr = OsmanlicaOCR(language='osmanlica+ara+tur')  # Özel + Arapça + Türkçe
```

### Özel Model Kullanımı

```python
# Eğittiğiniz özel modeli kullan
ocr = OsmanlicaOCR(custom_model='models/osmanlica.traineddata')
```

### Model Toplama (Ensemble)

```python
def ensemble_ocr(image_path, models):
    """Birden fazla modelin sonuçlarını birleştir"""
    results = []
    
    for model in models:
        ocr = OsmanlicaOCR(language=model)
        text = ocr.extract_text(image_path)
        results.append(text)
    
    # En sık görülen sonucu seç (voting)
    from collections import Counter
    words = [r.split() for r in results]
    
    # Kelime bazında voting
    # (implementasyon detayı)
    
    return best_result

# Kullanım
models = ['ara', 'tur', 'osmanlica']
text = ensemble_ocr('input.jpg', models)
```

---

## Post-Processing

### Yaygın Hataları Düzelt

```python
def post_process(text):
    """OCR sonuçlarını iyileştir"""
    
    # 1. Yaygın karakter hatalarını düzelt
    replacements = {
        '0': '۰',  # Sıfır yerine Arap sıfırı
        '1': '۱',
        # ... diğer düzeltmeler
    }
    
    for wrong, right in replacements.items():
        text = text.replace(wrong, right)
    
    # 2. Sağdan sola hizalama işaretlerini ekle
    text = '\u202B' + text + '\u202C'  # RLE + text + PDF
    
    # 3. Gereksiz boşlukları temizle
    text = ' '.join(text.split())
    
    # 4. Noktalama düzeltmeleri
    # ...
    
    return text
```

### Sözlük Tabanlı Düzeltme

```python
def dictionary_correction(text, dictionary_file):
    """Sözlük kullanarak kelimeleri düzelt"""
    
    # Osmanlıca sözlük yükle
    with open(dictionary_file, 'r', encoding='utf-8') as f:
        valid_words = set(f.read().split())
    
    words = text.split()
    corrected = []
    
    for word in words:
        if word in valid_words:
            corrected.append(word)
        else:
            # En yakın geçerli kelimeyi bul
            closest = find_closest_word(word, valid_words)
            corrected.append(closest)
    
    return ' '.join(corrected)
```

### N-gram Dil Modeli

```python
def language_model_correction(text, lm_file):
    """Dil modeli ile cümle düzeyi düzeltme"""
    # KenLM veya benzeri bir dil modeli kullan
    pass
```

---

## Performans İyileştirme

### Paralel İşleme

```python
from multiprocessing import Pool
from functools import partial

def process_single_image(image_path, ocr):
    """Tek görüntü işle"""
    return ocr.extract_text(image_path)

def batch_process_parallel(image_paths, n_workers=4):
    """Paralel toplu işleme"""
    ocr = OsmanlicaOCR()
    
    with Pool(n_workers) as pool:
        func = partial(process_single_image, ocr=ocr)
        results = pool.map(func, image_paths)
    
    return results
```

### Önbellekleme (Caching)

```python
import hashlib
import pickle
import os

def cached_ocr(image_path, ocr, cache_dir='cache'):
    """Sonuçları önbellekle"""
    
    # Görüntü hash'i oluştur
    with open(image_path, 'rb') as f:
        image_hash = hashlib.md5(f.read()).hexdigest()
    
    cache_file = os.path.join(cache_dir, f'{image_hash}.pkl')
    
    # Önbellekte var mı?
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    
    # Yoksa işle ve kaydet
    result = ocr.extract_text(image_path)
    
    os.makedirs(cache_dir, exist_ok=True)
    with open(cache_file, 'wb') as f:
        pickle.dump(result, f)
    
    return result
```

### Batch İşleme Optimizasyonu

```python
def smart_batch_process(image_dir, batch_size=10):
    """Akıllı toplu işleme"""
    ocr = OsmanlicaOCR()
    
    images = [f for f in os.listdir(image_dir) 
              if f.endswith(('.jpg', '.png'))]
    
    results = {}
    
    for i in range(0, len(images), batch_size):
        batch = images[i:i+batch_size]
        
        for image in batch:
            path = os.path.join(image_dir, image)
            results[image] = ocr.extract_text(path)
        
        # Belleği temizle
        import gc
        gc.collect()
    
    return results
```

---

## Doğruluk İyileştirme Kontrol Listesi

### ✅ Görüntü Kalitesi
- [ ] DPI en az 300
- [ ] Net odaklama
- [ ] İyi aydınlatma
- [ ] Düz, temiz arka plan
- [ ] Gölge ve yansıma yok

### ✅ Ön İşleme
- [ ] Gürültü temizleme
- [ ] Eğrilik düzeltme
- [ ] İkili görüntüye çevirme
- [ ] Kontrast optimizasyonu

### ✅ Tesseract Ayarları
- [ ] Doğru PSM modu (6)
- [ ] LSTM motor (OEM 3)
- [ ] Uygun karakter seti
- [ ] Dil kombinasyonu

### ✅ Model
- [ ] Özel eğitilmiş model
- [ ] Yeterli eğitim verisi
- [ ] İyi değerlendirme skoru

### ✅ Post-Processing
- [ ] Karakter düzeltmeleri
- [ ] Sözlük kontrolü
- [ ] Format düzeltmeleri

---

## Doğruluk Benchmarks

| Optimizasyon Seviyesi | Karakter Doğruluğu | Kelime Doğruluğu |
|----------------------|-------------------|------------------|
| Temel (ham görüntü)  | %70-80            | %60-70           |
| Ön işleme            | %85-90            | %75-85           |
| Özel model           | %90-95            | %85-90           |
| Tam optimizasyon     | %95-98            | %90-95           |

---

**Son Güncelleme**: 2026-02-16
