# 📖 API Dokümantasyonu

Osmanlıca Tesseract OCR - Programatik Kullanım Rehberi

## 📋 İçindekiler

1. [OsmanlicaOCR Sınıfı](#osmanlicaocr-sınıfı)
2. [Ön İşleme Fonksiyonları](#ön-i̇şleme-fonksiyonları)
3. [Eğitim API'si](#eğitim-apisi)
4. [Değerlendirme API'si](#değerlendirme-apisi)
5. [Örnekler](#örnekler)

---

## OsmanlicaOCR Sınıfı

### Sınıf: `OsmanlicaOCR`

Ana OCR sınıfı. Osmanlıca metinleri tanımak için optimize edilmiştir.

#### Başlatma

```python
from scripts.osmanlica_ocr import OsmanlicaOCR

ocr = OsmanlicaOCR(
    language='ara+tur',
    custom_model=None,
    preprocess=True
)
```

**Parametreler:**
- `language` (str): Tesseract dil kodu. Varsayılan: 'ara+tur'
- `custom_model` (str, optional): Özel model dosya yolu
- `preprocess` (bool): Otomatik ön işleme. Varsayılan: True

---

### Metod: `extract_text()`

Görüntüden metin çıkarır.

```python
text = ocr.extract_text(image_path, return_confidence=False)
```

**Parametreler:**
- `image_path` (str): Görüntü dosyası yolu
- `return_confidence` (bool): Güven skoru dönülsün mü? Varsayılan: False

**Dönüş:**
- `str`: Tanınan metin
- `tuple`: (metin, güven_skoru) - eğer `return_confidence=True`

**Örnek:**

```python
# Basit kullanım
text = ocr.extract_text('document.jpg')

# Güven skoru ile
text, confidence = ocr.extract_text('document.jpg', return_confidence=True)
print(f"Metin: {text}")
print(f"Güven: {confidence:.2f}%")
```

---

### Metod: `extract_text_with_boxes()`

Metin ve her kelimenin konumunu çıkarır.

```python
results = ocr.extract_text_with_boxes(image_path)
```

**Parametreler:**
- `image_path` (str): Görüntü dosyası yolu

**Dönüş:**
- `list`: Her kelime için dictionary listesi
  - `text` (str): Kelime
  - `confidence` (float): Güven skoru
  - `x` (int): X koordinatı
  - `y` (int): Y koordinatı
  - `width` (int): Genişlik
  - `height` (int): Yükseklik

**Örnek:**

```python
results = ocr.extract_text_with_boxes('document.jpg')

for result in results:
    print(f"Kelime: {result['text']}")
    print(f"Konum: ({result['x']}, {result['y']})")
    print(f"Güven: {result['confidence']:.1f}%")
    print("---")
```

---

### Metod: `batch_process()`

Birden fazla görüntüyü işler.

```python
results = ocr.batch_process(image_dir, output_dir=None)
```

**Parametreler:**
- `image_dir` (str): Görüntü dizini
- `output_dir` (str, optional): Çıktı dizini

**Dönüş:**
- `dict`: {dosya_adı: metin} dictionary'si

**Örnek:**

```python
results = ocr.batch_process(
    image_dir='images/',
    output_dir='texts/'
)

for filename, text in results.items():
    if text:
        print(f"✓ {filename}: {len(text)} karakter")
    else:
        print(f"✗ {filename}: Hata")
```

---

### Metod: `preprocess_image()`

Görüntüyü OCR için optimize eder.

```python
processed = ocr.preprocess_image(image)
```

**Parametreler:**
- `image` (np.ndarray): OpenCV formatında görüntü

**Dönüş:**
- `np.ndarray`: İşlenmiş görüntü

**Örnek:**

```python
import cv2

image = cv2.imread('document.jpg')
processed = ocr.preprocess_image(image)
cv2.imwrite('processed.jpg', processed)
```

---

## Ön İşleme Fonksiyonları

### `preprocess_image()`

Tam ön işleme pipeline'ı.

```python
from scripts.preprocess import preprocess_image

processed = preprocess_image(
    image_path,
    output_path=None,
    denoise=True,
    deskew=True,
    binarize=True,
    enhance_contrast=True,
    sharpen=False,
    remove_shadow=False
)
```

**Parametreler:**
- `image_path` (str): Giriş görüntü yolu
- `output_path` (str, optional): Çıkış yolu
- `denoise` (bool): Gürültü temizleme
- `deskew` (bool): Eğrilik düzeltme
- `binarize` (bool): İkili görüntüye çevirme
- `enhance_contrast` (bool): Kontrast artırma
- `sharpen` (bool): Keskinleştirme
- `remove_shadow` (bool): Gölge kaldırma

**Dönüş:**
- `np.ndarray`: İşlenmiş görüntü

---

### `denoise_image()`

Görüntüden gürültü temizler.

```python
from scripts.preprocess import denoise_image

denoised = denoise_image(image, method='fastNlMeans')
```

**Parametreler:**
- `image` (np.ndarray): Görüntü
- `method` (str): 'fastNlMeans', 'bilateral', 'gaussian'

**Dönüş:**
- `np.ndarray`: Temizlenmiş görüntü

---

### `binarize_image()`

İkili görüntüye çevirir.

```python
from scripts.preprocess import binarize_image

binary = binarize_image(image, method='adaptive')
```

**Parametreler:**
- `image` (np.ndarray): Gri tonlama görüntü
- `method` (str): 'otsu', 'adaptive', 'simple'

**Dönüş:**
- `np.ndarray`: İkili görüntü

---

### `deskew_image()`

Eğri görüntüyü düzeltir.

```python
from scripts.preprocess import deskew_image

straightened = deskew_image(image)
```

**Parametreler:**
- `image` (np.ndarray): Görüntü

**Dönüş:**
- `np.ndarray`: Düzeltilmiş görüntü

---

### `enhance_contrast()`

Kontrast artırır.

```python
from scripts.preprocess import enhance_contrast

enhanced = enhance_contrast(image, method='clahe')
```

**Parametreler:**
- `image` (np.ndarray): Gri tonlama görüntü
- `method` (str): 'clahe', 'histogram'

**Dönüş:**
- `np.ndarray`: Kontrastı artırılmış görüntü

---

## Eğitim API'si

### Sınıf: `TesseractTrainer`

Model eğitimi için yardımcı sınıf.

```python
from scripts.train_tesseract import TesseractTrainer

trainer = TesseractTrainer(
    language_code='osmanlica',
    training_data_dir='training-data',
    output_dir='models'
)
```

---

### Metod: `prepare_training_data()`

Eğitim verilerini hazırlar.

```python
trainer.prepare_training_data(
    images_dir='training-data/images',
    ground_truth_dir='training-data/ground-truth'
)
```

---

### Metod: `train_model()`

Modeli eğitir.

```python
trainer.train_model(
    font_name='OsmanlicaFont',
    start_model=None
)
```

---

### Metod: `fine_tune_model()`

Mevcut modeli fine-tune eder.

```python
trainer.fine_tune_model(
    base_model='ara',
    training_text='training_text.txt',
    iterations=10000
)
```

---

## Değerlendirme API'si

### `evaluate_model()`

Model performansını değerlendirir.

```python
from scripts.evaluate import evaluate_model

metrics = evaluate_model(
    test_dir='test-set/images',
    ground_truth_dir='test-set/ground-truth',
    model_path='models/osmanlica.traineddata'
)
```

**Parametreler:**
- `test_dir` (str): Test görüntüleri dizini
- `ground_truth_dir` (str): Ground truth dizini
- `model_path` (str, optional): Model yolu

**Dönüş:**
- `dict`: Değerlendirme metrikleri
  - `avg_char_accuracy`: Ortalama karakter doğruluğu
  - `avg_word_accuracy`: Ortalama kelime doğruluğu
  - `avg_cer`: Ortalama Character Error Rate
  - `avg_wer`: Ortalama Word Error Rate
  - `avg_confidence`: Ortalama güven skoru
  - `total_samples`: Toplam örnek sayısı

---

### `calculate_accuracy()`

İki metin arasındaki doğruluğu hesaplar.

```python
from scripts.evaluate import calculate_accuracy

accuracy = calculate_accuracy(predicted, ground_truth)
```

**Parametreler:**
- `predicted` (str): Tahmin edilen metin
- `ground_truth` (str): Gerçek metin

**Dönüş:**
- `dict`: Doğruluk metrikleri
  - `char_accuracy`: Karakter doğruluğu (%)
  - `word_accuracy`: Kelime doğruluğu (%)
  - `levenshtein_distance`: Levenshtein mesafesi
  - `cer`: Character Error Rate (%)
  - `wer`: Word Error Rate (%)

---

## Örnekler

### Örnek 1: Basit OCR

```python
from scripts.osmanlica_ocr import OsmanlicaOCR

ocr = OsmanlicaOCR()
text = ocr.extract_text('document.jpg')
print(text)
```

### Örnek 2: Özel Model ile OCR

```python
ocr = OsmanlicaOCR(
    custom_model='models/osmanlica.traineddata',
    preprocess=True
)

text, conf = ocr.extract_text('document.jpg', return_confidence=True)
print(f"Metin: {text}")
print(f"Güven: {conf:.2f}%")
```

### Örnek 3: Manuel Ön İşleme

```python
from scripts.preprocess import preprocess_image
from scripts.osmanlica_ocr import OsmanlicaOCR

# Önce görüntüyü işle
processed = preprocess_image(
    'input.jpg',
    'processed.jpg',
    denoise=True,
    deskew=True,
    binarize=True
)

# Sonra OCR uygula
ocr = OsmanlicaOCR(preprocess=False)  # Zaten işlenmiş
text = ocr.extract_text('processed.jpg')
```

### Örnek 4: Toplu İşleme

```python
ocr = OsmanlicaOCR()

results = ocr.batch_process(
    image_dir='documents/',
    output_dir='texts/'
)

for filename, text in results.items():
    print(f"{filename}: {len(text)} karakter")
```

### Örnek 5: Konum Bilgisi ile OCR

```python
ocr = OsmanlicaOCR()
results = ocr.extract_text_with_boxes('document.jpg')

# Sola hizalı kelimeler
left_words = [r for r in results if r['x'] < 100]

# Yüksek güvenli kelimeler
confident_words = [r for r in results if r['confidence'] > 90]
```

### Örnek 6: Model Eğitimi

```python
from scripts.train_tesseract import TesseractTrainer

trainer = TesseractTrainer()

# Veriyi hazırla
trainer.prepare_training_data(
    images_dir='training-data/images',
    ground_truth_dir='training-data/ground-truth'
)

# Fine-tuning yap
trainer.fine_tune_model(
    base_model='ara',
    training_text='training-data/training_text.txt',
    iterations=10000
)
```

### Örnek 7: Model Değerlendirme

```python
from scripts.evaluate import evaluate_model, print_evaluation_report

metrics = evaluate_model(
    test_dir='test-set/images',
    ground_truth_dir='test-set/ground-truth',
    model_path='models/osmanlica.traineddata'
)

print_evaluation_report(metrics)
```

### Örnek 8: Paralel İşleme

```python
from multiprocessing import Pool
from scripts.osmanlica_ocr import OsmanlicaOCR

def process_image(image_path):
    ocr = OsmanlicaOCR()
    return ocr.extract_text(image_path)

image_paths = ['img1.jpg', 'img2.jpg', 'img3.jpg']

with Pool(4) as pool:
    results = pool.map(process_image, image_paths)
```

### Örnek 9: Hata Yönetimi

```python
from scripts.osmanlica_ocr import OsmanlicaOCR

ocr = OsmanlicaOCR()

try:
    text = ocr.extract_text('document.jpg')
    print(f"Başarılı: {text}")
except ValueError as e:
    print(f"Görüntü yüklenemedi: {e}")
except Exception as e:
    print(f"OCR hatası: {e}")
```

### Örnek 10: Özel Konfigürasyon

```python
from scripts.osmanlica_ocr import OsmanlicaOCR

ocr = OsmanlicaOCR()

# Özel Tesseract config
ocr.config = '--oem 3 --psm 6 -c tessedit_char_whitelist=ابتثج'

text = ocr.extract_text('document.jpg')
```

---

## Hata Kodları

| Kod | Açıklama | Çözüm |
|-----|----------|-------|
| ValueError | Görüntü yüklenemedi | Dosya yolunu kontrol edin |
| ImportError | Modül bulunamadı | `pip install -r requirements.txt` |
| TesseractNotFound | Tesseract kurulu değil | Tesseract kurun |
| ModelNotFound | Model dosyası bulunamadı | Model yolunu kontrol edin |

---

## Performans İpuçları

1. **Önbellekleme**: Aynı görüntüyü tekrar işlemekten kaçının
2. **Batch İşleme**: Çok görüntü için `batch_process()` kullanın
3. **Paralel İşleme**: `multiprocessing` ile hızlandırın
4. **Ön İşleme**: Önceden işlenmiş görüntüler kullanın
5. **GPU**: Büyük veri setleri için GPU kullanın (CUDA)

---

## Versiyonlar

| Versiyon | Tarih | Değişiklikler |
|----------|-------|--------------|
| 1.0.0 | 2026-02-16 | İlk sürüm |

---

**Son Güncelleme**: 2026-02-16
