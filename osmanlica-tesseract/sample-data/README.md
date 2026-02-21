# Örnek Veri Seti

## ⚠️ ÖNEMLİ: Bu Sentetik (Yapay) Örneklerdir

**Bu görüntüler gerçek Osmanlı belge taramaları DEĞİLDİR!**

- ✅ Programatik olarak oluşturulmuş (PIL kütüphanesi ile)
- ✅ Test ve demo amaçlıdır
- ❌ Gerçek tarihsel belge taraması değil
- ❌ Model eğitimi için yeterli değil

**Gerçek eğitim verisi için**: [`training-data/`](../training-data/) dizinine gerçek Osmanlıca belge taramalarını ekleyin.

📖 **Detaylı bilgi**: [TRAINING-DATA-STATUS.md](../TRAINING-DATA-STATUS.md)

---

Bu dizin, test ve demo amaçlı örnek Osmanlıca görüntüleri ve ground truth dosyalarını içerir.

## Dizin Yapısı

```
sample-data/
├── images/              # Osmanlıca metin görüntüleri
│   ├── sample001_besmele.png
│   ├── sample002_hamd.png
│   ├── sample003_rahman.png
│   ├── sample004_malik.png
│   └── sample005_iyyake.png
└── ground-truth/        # Doğru metinler
    ├── sample001_besmele.txt
    ├── sample002_hamd.txt
    ├── sample003_rahman.txt
    ├── sample004_malik.txt
    └── sample005_iyyake.txt
```

## Örnek Oluşturma

Yeni örnekler oluşturmak için:

```bash
python scripts/create_samples.py
```

Bu script, Fatiha suresinden alınan Osmanlıca metinlerle örnek görüntüler oluşturur.

## Örnek İçerikler

| Dosya | İçerik | Açıklama |
|-------|--------|----------|
| sample001 | بسم الله الرحمن الرحیم | Besmele |
| sample002 | العالمین رب لله الحمد | Hamd ayeti |
| sample003 | الرحیم الرحمن | Rahman Rahim |
| sample004 | الدین یوم مالک | Malik ayeti |
| sample005 | نعبد إیاک | İyyake na'büd |

## Kullanım

### Test İçin

```python
from scripts.osmanlica_ocr import OsmanlicaOCR

ocr = OsmanlicaOCR()
text = ocr.extract_text('sample-data/images/sample001_besmele.png')
print(text)
```

### Değerlendirme İçin

```bash
python scripts/evaluate.py \
    --test-dir sample-data/images \
    --gt-dir sample-data/ground-truth
```

### Toplu İşleme

```python
results = ocr.batch_process(
    'sample-data/images/',
    'sample-data/output/'
)
```

## Kendi Örneklerinizi Ekleyin

1. Osmanlıca metin görüntüsünü `images/` dizinine ekleyin
2. İlgili `.txt` dosyasını `ground-truth/` dizinine ekleyin
3. Dosya adları eşleşmeli (örn: `sample006.png` → `sample006.txt`)

## Öneriler

- **Görüntü Formatı**: PNG (tercih edilen) veya TIFF
- **Çözünürlük**: 300 DPI veya üzeri
- **Boyut**: Minimum 20 piksel harf yüksekliği
- **Kalite**: Net, iyi aydınlatılmış, gölgesiz

---

**Not**: Bu örnekler eğitim ve test amaçlıdır. Gerçek dünya uygulamalarında daha fazla ve çeşitli örnek kullanın.
