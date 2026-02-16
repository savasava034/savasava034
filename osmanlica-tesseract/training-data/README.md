# Eğitim Verileri

Bu dizin, Tesseract model eğitimi için gerekli verileri içerir.

## Dizin Yapısı

```
training-data/
├── images/              # Osmanlıca metin görüntüleri
│   ├── sample001.png
│   ├── sample002.png
│   └── ...
├── ground-truth/        # Her görüntü için doğru metin
│   ├── sample001.gt.txt
│   ├── sample002.gt.txt
│   └── ...
├── fonts/               # Osmanlıca fontlar
│   ├── Amiri-Regular.ttf
│   ├── ScheherazadeNew-Regular.ttf
│   └── ...
└── training_config.json # Eğitim yapılandırması
```

## Görüntü Gereksinimleri

- **Format**: PNG, TIFF (tercih edilen)
- **Çözünürlük**: En az 300 DPI
- **Boyut**: Harf yüksekliği en az 20 piksel
- **Kalite**: Net, iyi aydınlatılmış, gölgesiz

## Ground Truth Formatı

Her görüntü için bir `.gt.txt` dosyası:

**Örnek**: `sample001.gt.txt`
```
بسم الله الرحمن الرحیم
```

## Veri Toplama İpuçları

1. **Çeşitli Kaynaklar**: Farklı kitaplar, belgeler
2. **Farklı Fontlar**: Matbu ve el yazısı
3. **Çeşitli Durumlar**: Temiz ve eskimiş belgeler
4. **Dengeli Dağılım**: Her karakter için yeterli örnek

## Minimum Gereksinimler

- **Fine-tuning için**: 500-1000 görüntü
- **Sıfırdan eğitim için**: 10,000+ görüntü

## Veri Hazırlama

```bash
# Eğitim verilerini hazırla
python scripts/train_tesseract.py \
    --action prepare \
    --images-dir training-data/images \
    --gt-dir training-data/ground-truth
```

## Font Kaynakları

- [Amiri](https://github.com/aliftype/amiri)
- [Scheherazade New](https://software.sil.org/scheherazade/)
- [Noto Naskh Arabic](https://fonts.google.com/noto/specimen/Noto+Naskh+Arabic)

---

**Not**: Eğitim verilerini ekledikten sonra bu dosyayı güncelleyin.
