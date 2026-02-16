# 🔤 Osmanlıca Tesseract OCR Projesi

## 📖 Proje Hakkında

Bu proje, **Osmanlıca** (Arap harfli Türkçe) metinleri yüksek doğrulukla tanıyabilen bir Tesseract OCR motoru oluşturmak için hazırlanmıştır. En az işlemle en yüksek doğruluk oranına ulaşmak hedeflenmiştir.

### 🎯 Özellikler

- ✅ **Açık Kaynak Altyapı**: Tesseract OCR tabanlı
- ✅ **Osmanlıca Desteği**: Arap harfli Türkçe için optimize edilmiş
- ✅ **Yüksek Doğruluk**: Görüntü ön işleme ve model optimizasyonu
- ✅ **Kolay Eğitim**: Otomatik eğitim scriptleri
- ✅ **Hızlı Kurulum**: Tek komutla kurulum

## 🚀 Hızlı Başlangıç

### Gereksinimler

```bash
# Sistem gereksinimleri (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-tur
sudo apt-get install -y python3 python3-pip
sudo apt-get install -y imagemagick
```

### Python Paketlerini Kurma

```bash
pip install -r requirements.txt
```

### Temel Kullanım

```python
from scripts.osmanlica_ocr import OsmanlicaOCR

# OCR nesnesini oluştur
ocr = OsmanlicaOCR()

# Görüntüden metin çıkar
text = ocr.extract_text("ornek-goruntu.jpg")
print(text)
```

## 📁 Proje Yapısı

```
osmanlica-tesseract/
├── README.md                 # Bu dosya
├── requirements.txt          # Python bağımlılıkları
├── training-data/           # Eğitim verileri
│   ├── images/              # Osmanlıca görüntüler
│   ├── ground-truth/        # Doğrulama metinleri
│   └── fonts/               # Osmanlıca fontlar
├── scripts/                 # Yardımcı scriptler
│   ├── osmanlica_ocr.py     # Ana OCR sınıfı
│   ├── preprocess.py        # Görüntü ön işleme
│   ├── train_tesseract.py   # Model eğitimi
│   └── evaluate.py          # Model değerlendirme
├── models/                  # Eğitilmiş modeller
│   └── osmanlica.traineddata
├── examples/                # Örnek kullanımlar
│   └── basic_usage.py
└── docs/                    # Detaylı dokümantasyon
    ├── EGITIM.md            # Eğitim rehberi
    ├── OPTIMIZASYON.md      # Optimizasyon ipuçları
    └── API.md               # API dokümantasyonu
```

## 📚 Detaylı Dokümantasyon

- **[Eğitim Rehberi](docs/EGITIM.md)** - Kendi modelinizi nasıl eğitirsiniz
- **[Optimizasyon İpuçları](docs/OPTIMIZASYON.md)** - Doğruluğu artırma yöntemleri
- **[API Dokümantasyonu](docs/API.md)** - Programatik kullanım

## 🎓 Tesseract Nedir?

Tesseract, Google tarafından geliştirilen ve desteklenen açık kaynaklı bir OCR (Optical Character Recognition) motorudur. 100'den fazla dili destekler ve yüksek doğruluk oranlarına sahiptir.

### Neden Tesseract?

1. **Açık Kaynak**: Tamamen ücretsiz ve açık kaynak
2. **Olgun Teknoloji**: 30+ yıllık geliştirme geçmişi
3. **Çok Dilli Destek**: 100+ dil desteği
4. **Özelleştirilebilir**: Kendi diliniz için eğitilebilir
5. **Aktif Topluluk**: Geniş kullanıcı ve geliştirici topluluğu
6. **Yüksek Doğruluk**: Modern LSTM tabanlı motor

## 🔧 Osmanlıca için Özel Optimizasyonlar

### 1. Görüntü Ön İşleme

```python
from scripts.preprocess import preprocess_image

# Görüntüyü optimize et
optimized = preprocess_image(
    "ornek.jpg",
    denoise=True,        # Gürültü temizleme
    deskew=True,         # Eğrilik düzeltme
    binarize=True,       # İkili görüntüye çevirme
    enhance_contrast=True # Kontrast artırma
)
```

### 2. Özel Karakter Setleri

Osmanlıca, standart Arapça'dan farklı bazı karakterler içerir:
- پ (pe)
- چ (çe)
- ژ (je)
- گ (gef)

### 3. Sağdan Sola Yazım Desteği

Osmanlıca metinler sağdan sola yazılır. Bu durum özel konfigürasyon gerektirir.

## 📊 Performans Metrikleri

Model doğruluğunu değerlendirmek için:

```bash
python scripts/evaluate.py --test-set training-data/test/
```

Tipik metrikler:
- **Character Accuracy**: %95+
- **Word Accuracy**: %90+
- **Processing Speed**: 100-500 karakter/saniye

## 🎯 Kullanım Senaryoları

1. **Tarihi Belge Dijitalleştirme**: Osmanlı dönemi arşivleri
2. **Akademik Araştırma**: Tarih ve edebiyat çalışmaları
3. **Kütüphane Dijitalleştirme**: Eski kitap ve yazmaların metne dönüştürülmesi
4. **Eğitim**: Osmanlıca öğrenim materyalleri

## 🤝 Katkıda Bulunma

Projeye katkıda bulunmak için:

1. Fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🔗 Yararlı Kaynaklar

- [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract)
- [Tesseract Dokümantasyonu](https://tesseract-ocr.github.io/)
- [Tesseract Eğitim Rehberi](https://tesseract-ocr.github.io/tessdoc/Training-Tesseract.html)
- [Osmanlıca Fontlar](https://github.com/osmanlica/fonts)

## 💡 İpuçları

1. **Yüksek Çözünürlük**: En az 300 DPI görüntü kullanın
2. **İyi Aydınlatma**: Net, iyi aydınlatılmış görüntüler
3. **Temiz Arka Plan**: Düz, tek renkli arka plan
4. **Doğru Yazı Tipi**: Eğitim verisi ile benzer font
5. **Ön İşleme**: Her zaman görüntü ön işleme uygulayın

## 📞 Destek

Sorularınız için:
- GitHub Issues
- Email: [your-email@example.com]

---

**Geliştirici**: savasava034
**Güncelleme Tarihi**: 2026-02-16
