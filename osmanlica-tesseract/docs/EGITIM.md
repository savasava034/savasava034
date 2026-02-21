# 📚 Tesseract Eğitim Rehberi

Bu rehber, Osmanlıca için özel Tesseract OCR modelinin nasıl eğitileceğini adım adım açıklar.

## 📋 İçindekiler

1. [Gereksinimler](#gereksinimler)
2. [Eğitim Verisi Hazırlama](#eğitim-verisi-hazırlama)
3. [Model Eğitimi](#model-eğitimi)
4. [Fine-Tuning](#fine-tuning)
5. [Model Değerlendirme](#model-değerlendirme)
6. [İpuçları ve En İyi Pratikler](#i̇puçları-ve-en-i̇yi-pratikler)

---

## Gereksinimler

### Sistem Gereksinimleri

```bash
# Ubuntu/Debian için
sudo apt-get update
sudo apt-get install -y tesseract-ocr
sudo apt-get install -y libtesseract-dev
sudo apt-get install -y tesseract-ocr-ara tesseract-ocr-tur

# Eğitim araçları
sudo apt-get install -y tesseract-ocr-all
```

### Python Paketleri

```bash
pip install -r requirements.txt
```

### Donanım Önerileri

- **RAM**: En az 8GB (16GB önerilir)
- **Depolama**: En az 10GB boş alan
- **İşlemci**: Çok çekirdekli işlemci önerilir
- **GPU**: Opsiyonel, ancak eğitimi hızlandırır

---

## Eğitim Verisi Hazırlama

### 1. Görüntü Toplama

Kaliteli eğitim verisi için:

- **En az 500-1000** farklı Osmanlıca metin görüntüsü
- **Yüksek çözünürlük**: 300 DPI veya daha yüksek
- **Çeşitli kaynaklar**: Farklı yazı stilleri, el yazısı, matbu
- **Temiz görüntüler**: İyi aydınlatma, net odaklama

### 2. Görüntü Formatları

Desteklenen formatlar:
- PNG (önerilir)
- TIFF
- JPEG (kayıpsız sıkıştırma)

```bash
# Görüntüleri uygun formata çevir
convert input.jpg -density 300 output.png
```

### 3. Ground Truth Oluşturma

Her görüntü için doğru metin dosyası:

```
training-data/
├── images/
│   ├── sample001.png
│   ├── sample002.png
│   └── ...
└── ground-truth/
    ├── sample001.gt.txt
    ├── sample002.gt.txt
    └── ...
```

**Örnek ground truth dosyası:**
```
بسم الله الرحمن الرحیم
```

### 4. Eğitim Verisi Yapısı

```
training-data/
├── images/              # Orijinal görüntüler
├── ground-truth/        # Doğru metinler (.gt.txt)
├── fonts/               # Kullanılacak fontlar
└── training_config.json # Eğitim yapılandırması
```

### 5. Otomatik Veri Hazırlama

```python
from scripts.train_tesseract import TesseractTrainer

trainer = TesseractTrainer()
trainer.prepare_training_data(
    images_dir='training-data/images',
    ground_truth_dir='training-data/ground-truth'
)
```

---

## Model Eğitimi

### Yöntem 1: Sıfırdan Eğitim (Zor)

Tamamen yeni bir model oluşturmak için:

```bash
python scripts/train_tesseract.py --action train
```

**Avantajlar:**
- Tam kontrol
- Özel karakter setleri

**Dezavantajlar:**
- Çok fazla veri gerekir (10,000+ örnek)
- Uzun sürer (günler/haftalar)
- Karmaşık süreç

### Yöntem 2: Fine-Tuning (Önerilir) ⭐

Mevcut Arapça modelini Osmanlıca için özelleştirmek:

```bash
python scripts/train_tesseract.py \
    --action finetune \
    --base-model ara \
    --iterations 10000
```

**Avantajlar:**
- Daha az veri gerekir (500-1000 örnek)
- Daha hızlı (saatler)
- Daha kolay
- Yüksek doğruluk

**Dezavantajlar:**
- Temel modele bağımlı

### Adım Adım Fine-Tuning

#### 1. Temel Modeli İndir

```bash
# Arapça ve Türkçe modellerini indir
wget https://github.com/tesseract-ocr/tessdata_best/raw/main/ara.traineddata
wget https://github.com/tesseract-ocr/tessdata_best/raw/main/tur.traineddata

# Tesseract dizinine taşı
sudo mv *.traineddata /usr/share/tesseract-ocr/4.00/tessdata/
```

#### 2. Eğitim Konfigürasyonu Oluştur

```bash
python scripts/train_tesseract.py --action config
```

Bu komut `training-data/training_config.json` dosyası oluşturur:

```json
{
  "language_code": "osmanlica",
  "fonts": [
    "Amiri-Regular",
    "ScheherazadeNew-Regular",
    "NotoNaskhArabic-Regular"
  ],
  "training_params": {
    "max_iterations": 10000,
    "learning_rate": 0.0001,
    "target_error_rate": 0.02
  },
  "character_set": "ابتثجحخدذرزسشصضطظعغفقكلمنهويءآأؤإئةىپچژگ"
}
```

#### 3. Fontları Hazırla

Osmanlıca için uygun fontlar:

- **Amiri**: Modern Arap fontu
- **Scheherazade New**: Naskh tarzı
- **Noto Naskh Arabic**: Google'ın açık kaynak fontu

```bash
# Fontları indir ve kur
mkdir -p training-data/fonts
cd training-data/fonts

# Örnek: Amiri fontunu indir
wget https://github.com/aliftype/amiri/releases/download/0.113/Amiri-0.113.zip
unzip Amiri-0.113.zip
```

#### 4. Eğitim Metnini Hazırla

Osmanlıca metinlerin bulunduğu bir dosya oluştur:

```bash
# training-data/training_text.txt
cat > training-data/training_text.txt << 'EOF'
بسم الله الرحمن الرحیم
العالمین رب لله الحمد
الرحیم الرحمن
الدین یوم مالک
نعبد إیاک
نستعین وإیاک
EOF
```

#### 5. Eğitimi Başlat

```bash
python scripts/train_tesseract.py \
    --action finetune \
    --base-model ara \
    --iterations 10000
```

Bu işlem:
- Temel Arapça modelini yükler
- Osmanlıca verilerle özelleştirir
- 10,000 iterasyon eğitir
- `models/osmanlica.traineddata` dosyasını oluşturur

#### 6. Eğitim İlerlemesini İzle

Eğitim sırasında:

```
Iteration 100: Error Rate: 5.23%
Iteration 200: Error Rate: 4.87%
Iteration 300: Error Rate: 4.52%
...
Iteration 10000: Error Rate: 1.95%
```

**Hedef Error Rate**: %2-3 altı

---

## Model Değerlendirme

### Test Seti Hazırlama

```
test-set/
├── images/
│   ├── test001.png
│   ├── test002.png
│   └── ...
└── ground-truth/
    ├── test001.txt
    ├── test002.txt
    └── ...
```

### Model Performansını Test Et

```bash
python scripts/evaluate.py \
    --test-dir test-set/images \
    --gt-dir test-set/ground-truth \
    --model models/osmanlica.traineddata \
    --output evaluation_report.json
```

### Değerlendirme Metrikleri

```
MODEL DEĞERLENDIRME RAPORU
============================================================

Toplam Test Örneği: 100

Ortalama Karakter Doğruluğu: 96.50%
Ortalama Kelime Doğruluğu: 92.30%
Ortalama CER (Character Error Rate): 3.50%
Ortalama WER (Word Error Rate): 7.70%
Ortalama Güven Skoru: 89.20%

En İyi Sonuç: test045.png (Char: 99.10%)
En Kötü Sonuç: test078.png (Char: 87.40%)

============================================================
```

### İyi Performans Kriterleri

- ✅ **Karakter Doğruluğu**: %95+
- ✅ **Kelime Doğruluğu**: %90+
- ✅ **CER**: %5 altı
- ✅ **WER**: %10 altı
- ✅ **Güven Skoru**: %85+

---

## İpuçları ve En İyi Pratikler

### 🎯 Veri Kalitesi

1. **Çeşitlilik**: Farklı yazı tipleri, boyutlar, renkler
2. **Denge**: Her karakter için yeterli örnek
3. **Kalite > Miktar**: Az ama kaliteli veri, çok ama kötü veriden iyidir
4. **Gerçekçi Örnekler**: Gerçek dünya senaryolarını yansıtan veriler

### 🚀 Eğitim Optimizasyonu

1. **Başlangıç Noktası**: Ara veya Tur modeli ile başlayın
2. **Iterasyon Sayısı**: 
   - Fine-tuning için: 5,000-15,000
   - Sıfırdan eğitim için: 50,000+
3. **Erken Durdurma**: Error rate platoya ulaşınca durdurun
4. **Checkpoint'ler**: Her 1000 iterasyonda kaydet

### 📊 Veri Artırma (Data Augmentation)

Veriyi çoğaltmak için:

```python
from scripts.preprocess import preprocess_image

# Farklı varyasyonlar oluştur
variations = [
    {'denoise': True, 'binarize': True},
    {'enhance_contrast': True, 'sharpen': True},
    {'deskew': True, 'remove_shadow': True}
]

for i, params in enumerate(variations):
    output = f"augmented_{i}.png"
    preprocess_image(original, output, **params)
```

### 🔧 Hata Ayıklama

Düşük doğruluk durumunda:

1. **Veriyi Kontrol Et**: Ground truth doğru mu?
2. **Ön İşleme**: Görüntüler optimize mi?
3. **Karakter Seti**: Tüm karakterler tanımlı mı?
4. **Daha Fazla Veri**: Özellikle zor karakterler için
5. **Daha Fazla İterasyon**: Eğitim yeterli mi?

### 📈 İyileştirme Stratejileri

```python
# 1. Zor örnekleri belirle
difficult_samples = [r for r in results if r['char_accuracy'] < 90]

# 2. Bu örneklere benzer daha fazla veri ekle

# 3. Tekrar eğit
trainer.fine_tune_model('osmanlica', additional_iterations=5000)
```

### 💾 Model Yedekleme

```bash
# Eğitilmiş modeli yedekle
cp models/osmanlica.traineddata models/osmanlica_backup_$(date +%Y%m%d).traineddata

# GitHub'a yükle (dikkatli!)
git lfs track "*.traineddata"
git add models/osmanlica.traineddata
git commit -m "Yeni model versiyonu"
```

---

## Sık Sorulan Sorular

### S: Eğitim ne kadar sürer?

**C**: 
- Fine-tuning: 2-6 saat (normal bilgisayar)
- Sıfırdan eğitim: 1-7 gün (GPU ile daha hızlı)

### S: Minimum veri miktarı nedir?

**C**: 
- Fine-tuning: 500-1000 örnek
- Sıfırdan eğitim: 10,000+ örnek

### S: GPU gerekli mi?

**C**: Hayır, ama önerilir. GPU ile 5-10x daha hızlı.

### S: Hangi fontları kullanmalıyım?

**C**: 
- Modern metinler için: Amiri, Scheherazade
- El yazısı için: Daha fazla veri ve özel eğitim gerekir

### S: Model boyutu ne kadar?

**C**: Genellikle 10-50 MB arası.

---

## Ek Kaynaklar

- [Tesseract Resmi Dokümantasyonu](https://tesseract-ocr.github.io/)
- [Tesseract Training Wiki](https://github.com/tesseract-ocr/tesseract/wiki/TrainingTesseract-4.00)
- [Osmanlıca Fontlar](https://github.com/osmanlica/fonts)
- [Arapça OCR İpuçları](https://github.com/tesseract-ocr/tesseract/wiki/4.0-with-LSTM#arabic)

---

**Son Güncelleme**: 2026-02-16
