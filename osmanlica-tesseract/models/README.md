# Eğitilmiş Modeller

Bu dizin, eğitilmiş Tesseract OCR modellerini içerir.

## Model Dosyaları

- `osmanlica.traineddata` - Osmanlıca için optimize edilmiş model

## Model Kullanımı

### Python'da

```python
from scripts.osmanlica_ocr import OsmanlicaOCR

# Özel modeli kullan
ocr = OsmanlicaOCR(custom_model='models/osmanlica.traineddata')
text = ocr.extract_text('belge.jpg')
```

### Sistem Genelinde Kurulum

```bash
# Modeli Tesseract dizinine kopyala
sudo cp osmanlica.traineddata /usr/share/tesseract-ocr/4.00/tessdata/

# Kullan
tesseract belge.jpg cikti -l osmanlica
```

## Model Eğitimi

Yeni bir model eğitmek için:

```bash
python scripts/train_tesseract.py \
    --action finetune \
    --base-model ara \
    --iterations 10000
```

## Model Bilgileri

| Model | Temel | İterasyonlar | Char Accuracy | Word Accuracy |
|-------|-------|--------------|---------------|---------------|
| osmanlica.traineddata | ara | 10000 | %95+ | %90+ |

## Model Boyutları

- Tipik boyut: 10-50 MB
- Fine-tuned model: 15-30 MB
- Sıfırdan eğitilmiş: 20-50 MB

## Versiyon Geçmişi

### v1.0.0 (Planlanan)
- İlk Osmanlıca modeli
- Arapça temel model üzerinden fine-tuning
- 1000 eğitim örneği

---

**Not**: Model dosyaları büyük olduğu için Git LFS kullanmanız önerilir.

```bash
git lfs track "*.traineddata"
```
