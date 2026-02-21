# 🚀 Hızlı Başlangıç Kılavuzu

Osmanlıca Tesseract OCR'i 15 dakikada çalıştırın!

## ⚡ 3 Adımda Kurulum

### 1. Tesseract'ı Kurun

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-ara tesseract-ocr-tur

# macOS
brew install tesseract tesseract-lang

# Windows
# https://github.com/UB-Mannheim/tesseract/wiki adresinden indirin
```

### 2. Python Paketlerini Kurun

```bash
pip install -r requirements.txt
```

### 3. İlk OCR'ınızı Yapın

```python
from scripts.osmanlica_ocr import OsmanlicaOCR

ocr = OsmanlicaOCR()
text = ocr.extract_text('ornek-belge.jpg')
print(text)
```

## 📝 Temel Kullanım

### Tek Görüntü

```python
from scripts.osmanlica_ocr import OsmanlicaOCR

ocr = OsmanlicaOCR()

# Basit kullanım
text = ocr.extract_text('belge.jpg')

# Güven skoru ile
text, confidence = ocr.extract_text('belge.jpg', return_confidence=True)
print(f"Güven: {confidence:.2f}%")
```

### Birden Fazla Görüntü

```python
results = ocr.batch_process(
    image_dir='belgeler/',
    output_dir='metinler/'
)

print(f"{len(results)} belge işlendi!")
```

### Komut Satırından

```bash
# Tek dosya
python scripts/osmanlica_ocr.py belge.jpg

# Ön işleme
python scripts/preprocess.py girdi.jpg cikti.jpg
```

## 🎯 İlk Model Eğitimi

### Hazırlık

```bash
# Dizin yapısını oluştur
mkdir -p training-data/{images,ground-truth,fonts}

# Görüntülerinizi ve metinleri yerleştirin
# training-data/images/sample001.png
# training-data/ground-truth/sample001.gt.txt
```

### Eğitim Başlat

```bash
# Konfigürasyon oluştur
python scripts/train_tesseract.py --action config

# Fine-tuning (önerilir)
python scripts/train_tesseract.py \
    --action finetune \
    --base-model ara \
    --iterations 10000
```

### Model Değerlendir

```bash
python scripts/evaluate.py \
    --test-dir test-set/images \
    --gt-dir test-set/ground-truth \
    --model models/osmanlica.traineddata
```

## 🔧 Yaygın Sorunlar ve Çözümler

### Tesseract Bulunamadı

```bash
# Yolu kontrol et
which tesseract

# Ortam değişkenini ayarla
export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/
```

### Düşük Doğruluk

```python
# Ön işleme ekleyin
from scripts.preprocess import preprocess_image

processed = preprocess_image(
    'belge.jpg',
    'islenmis.jpg',
    denoise=True,
    deskew=True,
    binarize=True
)

text = ocr.extract_text('islenmis.jpg')
```

### Model Yüklenemedi

```bash
# Model dosyasını doğru dizine kopyalayın
sudo cp models/osmanlica.traineddata /usr/share/tesseract-ocr/4.00/tessdata/
```

## 📚 Sonraki Adımlar

1. **Dokümantasyonu okuyun**: [EGITIM.md](docs/EGITIM.md)
2. **Örnekleri deneyin**: [basic_usage.py](examples/basic_usage.py)
3. **Optimizasyon yapın**: [OPTIMIZASYON.md](docs/OPTIMIZASYON.md)
4. **API'yi keşfedin**: [API.md](docs/API.md)

## 💡 İpuçları

- ✅ En az 300 DPI görüntü kullanın
- ✅ Görüntüleri ön işlemeye tabi tutun
- ✅ Kendi verilerinizle model eğitin
- ✅ Test edin ve optimize edin

## 🆘 Yardım

Sorun mu yaşıyorsunuz?

1. [Dokümantasyonu](docs/) kontrol edin
2. [Örneklere](examples/) bakın
3. GitHub Issues açın

---

**Kolay gelsin!** 🎉
