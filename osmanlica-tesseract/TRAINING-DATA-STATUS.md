# 📊 Eğitim Verisi Durumu / Training Data Status

## ❓ Soru: "Kaç orijinal Osmanlıca sayfayla eğittin?"

## ✅ CEVAP: Şu anda 0 (sıfır) orijinal sayfa kullanıldı

Bu proje **sadece altyapı ve araçları** sağlar. Gerçek Osmanlıca belgelerle eğitim kullanıcı sorumluluğundadır.

---

## 📋 Mevcut Durum / Current Status

### ✅ Var Olanlar / What Exists

1. **Sentetik Demo Örnekleri**: 5 adet
   - `sample-data/images/` dizininde
   - Programatik olarak oluşturulmuş (PIL ile)
   - **Gerçek tarama DEĞİL**, sadece test amaçlı
   - Fatiha suresinden alınan metinler

2. **Eğitim Altyapısı**: Tam hazır
   - `scripts/train_tesseract.py` - Model eğitimi
   - `scripts/preprocess.py` - Görüntü ön işleme
   - `scripts/evaluate.py` - Model değerlendirme
   - Fine-tuning ve tam eğitim desteği

3. **Dokümantasyon**: Eksiksiz
   - Eğitim rehberi (`docs/EGITIM.md`)
   - Optimizasyon ipuçları (`docs/OPTIMIZASYON.md`)
   - API dokümantasyonu (`docs/API.md`)

### ❌ Olmayan / What's Missing

1. **Gerçek Osmanlıca Belgeler**: 0 adet
   - `training-data/images/` dizini BOŞ
   - `training-data/ground-truth/` dizini BOŞ
   - Hiçbir tarihsel belge taraması yok

2. **Eğitilmiş Model**: Yok
   - `models/` dizini BOŞ (sadece README var)
   - Önceden eğitilmiş `.traineddata` dosyası yok
   - Kullanıcı kendi verisiyle eğitmeli

---

## 🎯 Neden Gerçek Veri Yok? / Why No Real Data?

### Yasal ve Etik Nedenler

1. **Telif Hakları**: Osmanlı belgeleri telif hakkına tabi olabilir
2. **Kullanım İzinleri**: Her belge için ayrı izin gerekebilir
3. **Gizlilik**: Bazı belgeler kişisel veya hassas olabilir
4. **Dağıtım Kısıtlamaları**: Tüm belgeleri serbest dağıtamayız

### Teknik Nedenler

1. **Boyut**: 1000+ sayfa çok büyük olur (GitHub limitleri)
2. **Çeşitlilik**: Her kullanıcının farklı ihtiyacı var
3. **Kalite**: Kullanıcı kendi kalite kriterlerini belirlemeli
4. **Özelleştirme**: Her proje farklı font/stil gerektirebilir

---

## 📚 Gerçek Osmanlıca Belge Kaynakları

### 1. Türkiye Kütüphaneleri

#### Milli Kütüphane (Ankara)
- **Web**: https://www.mkutup.gov.tr/
- **Dijital Arşiv**: https://katalog.mkutup.gov.tr/
- **İçerik**: Osmanlı dönemi yazmaları, matbu eserler
- **Erişim**: Ücretsiz, çevrimiçi erişim mevcut

#### İstanbul Üniversitesi Kütüphanesi
- **Web**: https://kutuphane.istanbul.edu.tr/
- **Nadir Eserler**: Geniş Osmanlıca koleksiyonu
- **Erişim**: Akademik hesap gerekebilir

#### Süleymaniye Kütüphanesi
- **Web**: https://www.suleymaniye.ykm.gov.tr/
- **İçerik**: 100,000+ yazma eser
- **Dijital**: Kısmen dijitalleştirilmiş
- **Erişim**: Yerinde ve çevrimiçi

### 2. Uluslararası Kaynaklar

#### Library of Congress (ABD)
- **Web**: https://www.loc.gov/
- **Osmanlı Koleksiyonu**: Ferman, mektup, belgeler
- **Erişim**: Çoğu dijital, ücretsiz

#### British Library
- **Web**: https://www.bl.uk/
- **Osmanlı Arşivi**: Geniş koleksiyon
- **Dijital**: Kısmi erişim

#### Archive.org
- **Web**: https://archive.org/
- **Arama**: "Ottoman Turkish" veya "Osmanlıca"
- **Lisans**: Çoğu kamu malı
- **Format**: PDF, JPEG indirilebilir

### 3. Akademik Projeler

#### Ottoman Texts Archive Project (OTAP)
- Çeşitli üniversiteler işbirliği
- Dijitalleştirilmiş Osmanlı metinleri

#### Digital Ottoman Platform
- Modern OCR projeleri
- Açık erişim verileri

---

## 📖 Eğitim Verisi Toplama Rehberi

### Adım 1: Belge Seçimi

**Minimum Gereksinimler:**
- **Fine-tuning için**: 500-1000 sayfa
- **Sıfırdan eğitim için**: 10,000+ sayfa

**İdeal Özellikler:**
- Çeşitli yazı stilleri (matbu, el yazısı)
- Farklı dönemler (16-20. yüzyıl)
- Çeşitli konular (edebi, resmi, günlük)
- İyi korunmuş, net görüntüler

### Adım 2: Dijitalleştirme

```bash
# Tarama önerileri
- Çözünürlük: 300-600 DPI
- Format: PNG veya TIFF (kayıpsız)
- Renk: Gri tonlama veya renkli
- Düzgün hizalanmış, düz ışık
```

### Adım 3: Ground Truth Oluşturma

Her görüntü için transkripsiyon:

```
# Örnek: page001.png için
# Oluştur: page001.gt.txt

بسم الله الرحمن الرحیم
السلطان محمد خان
```

**Araçlar:**
- [Transkribus](https://readcoop.eu/transkribus/) - Yarı-otomatik transkripsiyon
- [OCR4all](https://www.ocr4all.org/) - Açık kaynak OCR platformu
- Manuel editörler (UTF-8 destekli text editörler)

### Adım 4: Veri Organizasyonu

```
training-data/
├── images/
│   ├── page001.png
│   ├── page002.png
│   ├── ...
│   └── page1000.png
├── ground-truth/
│   ├── page001.gt.txt
│   ├── page002.gt.txt
│   ├── ...
│   └── page1000.gt.txt
└── metadata.json  # Opsiyonel: belge bilgileri
```

---

## 🚀 Eğitim Nasıl Başlatılır?

### 1. Verilerinizi Ekleyin

```bash
# Görüntüleri kopyalayın
cp /yol/to/belgeler/*.png osmanlica-tesseract/training-data/images/

# Ground truth dosyalarını kopyalayın
cp /yol/to/transkriptler/*.gt.txt osmanlica-tesseract/training-data/ground-truth/
```

### 2. Verileri Hazırlayın

```bash
python scripts/train_tesseract.py \
    --action prepare \
    --images-dir training-data/images \
    --gt-dir training-data/ground-truth
```

### 3. Fine-Tuning Yapın (Önerilen)

```bash
python scripts/train_tesseract.py \
    --action finetune \
    --base-model ara \
    --iterations 10000
```

### 4. Modeli Değerlendirin

```bash
python scripts/evaluate.py \
    --test-dir test-set/images \
    --gt-dir test-set/ground-truth \
    --model models/osmanlica.traineddata
```

---

## ⚠️ Önemli Notlar

### Telif Hakları ve Lisanslar

1. **Kendi Verilerinizi Kullanın**: En güvenli yol
2. **Kamu Malı Belgeler**: Lisansı kontrol edin
3. **İzin Alın**: Telif hakkı varsa mutlaka izin alın
4. **Paylaşma**: Eğitilmiş modeli paylaşırken dikkat

### Veri Kalitesi

```
✅ İyi Örnekler:
- Net, yüksek çözünürlüklü taramalar
- Düzgün hizalanmış
- İyi aydınlatılmış
- Temiz arka plan

❌ Kötü Örnekler:
- Bulanık, düşük çözünürlük
- Eğik veya bozuk
- Gölgeli, yansımalı
- Lekeli, yırtık sayfalar
```

---

## 📊 Örnek Eğitim Senaryoları

### Senaryo 1: Küçük Proje (Test Amaçlı)

```
Sayfa Sayısı: 100-200
Süre: 1-2 hafta (hazırlık + eğitim)
Doğruluk: %85-90
Kullanım: Kişisel projeler, öğrenme
```

### Senaryo 2: Orta Ölçekli Proje

```
Sayfa Sayısı: 500-1000
Süre: 1-2 ay
Doğruluk: %92-95
Kullanım: Akademik araştırma, küçük arşivler
```

### Senaryo 3: Büyük Ölçekli Proje

```
Sayfa Sayısı: 5000-10000+
Süre: 3-6 ay
Doğruluk: %95-98+
Kullanım: Kütüphane dijitalleştirme, ticari kullanım
```

---

## 🤝 Topluluk Katkıları

### Veri Paylaşımı

Eğer lisansı uygunsa, verilerinizi paylaşabilirsiniz:

1. **GitHub Release**: Model ve örnek veri
2. **Zenodo/Figshare**: Akademik veri setleri
3. **HuggingFace**: Model paylaşım platformu

### Açık Veri Setleri

Topluluk tarafından oluşturulan açık veri setleri:
- [Belirtilecek - şu anda yok]

---

## 📈 İstatistikler (Örnek)

Diğer Tesseract projeleri için tipik sayılar:

| Proje | Sayfa Sayısı | Süre | Doğruluk |
|-------|-------------|------|----------|
| German Fraktur | 10,000+ | 6 ay | 95%+ |
| Arabic Historical | 5,000 | 4 ay | 93% |
| Old English | 8,000 | 5 ay | 94% |
| **Osmanlıca (Hedef)** | **500-1000** | **1-2 ay** | **92-95%** |

---

## 🎯 Sonuç

### Mevcut Durum Özeti

```
Gerçek Eğitim Verisi:  0 sayfa
Demo Örnekleri:        5 sayfa (sentetik)
Eğitim Altyapısı:     ✅ Hazır
Dokümantasyon:        ✅ Eksiksiz
Eğitilmiş Model:      ❌ Yok
```

### Sonraki Adımlar

1. ✅ Belge kaynakları belirleyin
2. ✅ Yasal izinleri kontrol edin
3. ✅ Sayfa toplamaya başlayın (hedef: 500-1000)
4. ✅ Ground truth oluşturun
5. ✅ Model eğitin
6. ✅ Değerlendirin ve optimize edin

---

## 📞 Destek ve Sorular

Eğitim verisi hakkında sorularınız için:
- GitHub Issues: Teknik sorular
- Dokümantasyon: `docs/EGITIM.md`
- Topluluk: [Belirtilecek]

---

**Güncelleme Tarihi**: 2026-02-16  
**Durum**: Altyapı hazır, veri bekleniyor  
**Hedef**: 500-1000 sayfa ile başlayın
