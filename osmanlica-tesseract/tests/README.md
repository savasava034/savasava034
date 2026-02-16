# Test Paketi

Bu dizin, Osmanlıca Tesseract OCR sisteminin test dosyalarını içerir.

## Test Dosyaları

- `test_preprocess.py` - Ön işleme fonksiyonları testleri
- `test_evaluate.py` - Değerlendirme fonksiyonları testleri

## Testleri Çalıştırma

### Tüm testler

```bash
python run_tests.py
```

### Tek bir test dosyası

```bash
python -m unittest tests.test_preprocess
```

### Belirli bir test sınıfı

```bash
python -m unittest tests.test_preprocess.TestPreprocessFunctions
```

### Belirli bir test

```bash
python -m unittest tests.test_preprocess.TestPreprocessFunctions.test_denoise_image_fastNlMeans
```

## Test Kapsamı

### Ön İşleme Testleri (`test_preprocess.py`)

- ✅ Görüntü yeniden boyutlandırma
- ✅ Gürültü temizleme (3 yöntem)
- ✅ İkili görüntüye çevirme (3 yöntem)
- ✅ Eğrilik düzeltme
- ✅ Kontrast artırma (2 yöntem)
- ✅ Kenar kaldırma
- ✅ Keskinleştirme
- ✅ Gölge kaldırma
- ✅ Tam ön işleme pipeline

### Değerlendirme Testleri (`test_evaluate.py`)

- ✅ Doğruluk hesaplama
- ✅ Levenshtein mesafesi
- ✅ Word Error Rate (WER)
- ✅ Unicode/Arapça desteği
- ✅ Sınır durumları

## Test Çıktısı Örneği

```
==============================================================
  OSMANICA TESSERACT OCR - TEST SÜİTİ
==============================================================

test_binarize_adaptive (tests.test_preprocess.TestPreprocessFunctions) ... ok
test_binarize_otsu (tests.test_preprocess.TestPreprocessFunctions) ... ok
test_binarize_simple (tests.test_preprocess.TestPreprocessFunctions) ... ok
...

----------------------------------------------------------------------
Ran 25 tests in 2.345s

OK

==============================================================
  TEST SONUÇLARI
==============================================================
Çalıştırılan: 25
Başarılı: 25
Başarısız: 0
Hata: 0
==============================================================
```

## Yeni Test Ekleme

1. `tests/` dizininde yeni bir `test_*.py` dosyası oluşturun
2. `unittest.TestCase` sınıfından türeyin
3. Test metotlarını `test_` ile başlayarak yazın
4. `run_tests.py` otomatik olarak bulacaktır

Örnek:

```python
import unittest

class TestYeniOzellik(unittest.TestCase):
    def test_ozellik(self):
        # Test kodu
        self.assertEqual(1 + 1, 2)
```

## Bağımlılıklar

Testler için ek bağımlılık gerekmez. Sadece ana `requirements.txt` dosyasındaki paketler yeterlidir.

Geliştirme için:

```bash
pip install pytest pytest-cov
```

---

**Not**: Testler, gerçek Tesseract OCR motoru olmadan da çalışabilir. OCR fonksiyonları için mock testler eklenebilir.
