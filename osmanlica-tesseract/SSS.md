# ❓ Sık Sorulan Sorular (SSS) / FAQ

## Eğitim Verisi Hakkında / About Training Data

### S1: Kaç orijinal Osmanlıca sayfayla eğittin?

**C**: **0 (sıfır)** orijinal sayfa. Bu proje sadece altyapı sağlar, gerçek belge taramalarıyla eğitilmiş model içermez.

- Sample-data dizinindeki 5 görüntü **sentetiktir** (programla oluşturulmuş)
- Training-data dizini **boştur**
- Kullanıcılar kendi belgelerini ekleyip model eğitmelidir

**Detay**: [TRAINING-DATA-STATUS.md](TRAINING-DATA-STATUS.md)

---

### S2: Neden önceden eğitilmiş model yok?

**C**: Birkaç nedenden dolayı:

1. **Telif Hakları**: Osmanlı belgeleri telif hakkına tabi olabilir
2. **Boyut**: 1000+ sayfalık veri çok büyük (GitHub limitleri)
3. **Çeşitlilik**: Her kullanıcının farklı ihtiyacı var
4. **Özelleştirme**: Her proje farklı dönem/stil gerektirebilir

---

### S3: Nasıl kendi modelimi eğitebilirim?

**C**: Adım adım:

1. **Belge Topla**: 500-1000 Osmanlıca sayfa taraması
2. **Transkribe Et**: Her sayfa için doğru metin oluştur
3. **Ekle**: `training-data/images/` ve `training-data/ground-truth/`
4. **Eğit**: `python scripts/train_tesseract.py --action finetune`
5. **Test Et**: `python scripts/evaluate.py`

**Rehber**: [docs/EGITIM.md](docs/EGITIM.md)

---

### S4: Nereden Osmanlıca belge bulabilirim?

**C**: Çeşitli kaynaklar:

- **Milli Kütüphane**: https://www.mkutup.gov.tr/
- **Süleymaniye Kütüphanesi**: https://www.suleymaniye.ykm.gov.tr/
- **Archive.org**: "Ottoman Turkish" ara
- **Library of Congress**: Osmanlı koleksiyonu
- **İstanbul Üniversitesi**: Nadir Eserler

**Tam liste**: [TRAINING-DATA-STATUS.md](TRAINING-DATA-STATUS.md#-gerçek-osmanlıca-belge-kaynakları)

---

### S5: Minimum kaç sayfa gerekir?

**C**: Eğitim yöntemine göre:

- **Fine-tuning**: 500-1000 sayfa (önerilir)
- **Sıfırdan eğitim**: 10,000+ sayfa
- **Test amaçlı**: 100-200 sayfa

**Kalite > Miktar**: Az ama kaliteli veri daha iyi sonuç verir.

---

## Teknik Sorular / Technical Questions

### S6: Sample-data ve training-data arasındaki fark?

**C**: 

| Özellik | sample-data | training-data |
|---------|-------------|---------------|
| Amaç | Demo/test | Model eğitimi |
| Sayfa | 5 adet | 0 (boş) |
| Kaynak | Sentetik | Gerçek taramalar |
| Kalite | Programatik | Gerçek belgeler |
| Kullanım | Hemen test et | Eğitim için ekle |

---

### S7: Tesseract kullanmadan OCR yapabilir miyim?

**C**: Bu proje Tesseract tabanlıdır. Alternatifler:

- **EasyOCR**: Daha kolay, daha az özelleştirme
- **PaddleOCR**: Modern, GPU desteği
- **Google Vision API**: Bulut tabanlı (ücretli)

Ancak Osmanlıca için özel eğitim gerektirir.

---

### S8: Modeli nasıl değerlendiririm?

**C**:

```bash
python scripts/evaluate.py \
    --test-dir test-images/ \
    --gt-dir test-ground-truth/ \
    --model models/osmanlica.traineddata
```

**Metrikler**:
- Karakter doğruluğu
- Kelime doğruluğu
- CER (Character Error Rate)
- WER (Word Error Rate)

---

### S9: GPU gerekli mi?

**C**: Hayır, ama önerilir:

- **CPU**: Yavaş ama yeterli (saatler)
- **GPU**: 5-10x daha hızlı
- Eğitim için GPU önerilir
- OCR kullanımı için CPU yeterli

---

### S10: Kaç DPI kullanmalıyım?

**C**:

- **Minimum**: 300 DPI
- **Önerilen**: 400-600 DPI
- **Maksimum**: 600 DPI (daha fazla fayda yok)

Yüksek DPI = Daha iyi sonuç ama daha yavaş işlem

---

## Kullanım Soruları / Usage Questions

### S11: Demo nasıl çalıştırılır?

**C**:

```bash
# Interaktif demo
python demo.py

# Jupyter notebook
jupyter notebook examples/Osmanlica_OCR_Tutorial.ipynb

# Komut satırı
python scripts/osmanlica_ocr.py sample-data/images/sample001_besmele.png
```

---

### S12: Toplu işleme nasıl yapılır?

**C**:

```python
from scripts.osmanlica_ocr import OsmanlicaOCR

ocr = OsmanlicaOCR()
results = ocr.batch_process(
    image_dir='belgeler/',
    output_dir='metinler/'
)
```

**Detay**: [docs/API.md](docs/API.md)

---

### S13: Doğruluk nasıl artırılır?

**C**: Birkaç yöntem:

1. **Ön işleme**: Gürültü temizle, kontrast artır
2. **Kaliteli veri**: Yüksek DPI, net görüntüler
3. **Daha fazla eğitim**: 1000+ sayfa kullan
4. **Fine-tuning**: Kendi verilerinle özelleştir

**Rehber**: [docs/OPTIMIZASYON.md](docs/OPTIMIZASYON.md)

---

## Yasal ve Etik / Legal & Ethical

### S14: Telif hakları nasıl?

**C**: Dikkat edin:

- ✅ Kamu malı belgeler serbest
- ⚠️ Modern eserler telif hakkına tabi
- ✅ Kendi belgeleriniz serbest
- ❌ İzinsiz dağıtmayın

**Her zaman kontrol edin!**

---

### S15: Modeli ticari kullanabilir miyim?

**C**: Evet, MIT lisansı altında:

- ✅ Ticari kullanım serbest
- ✅ Değiştirme serbest
- ✅ Dağıtma serbest
- ⚠️ Lisans metnini koruyun
- ❌ Garanti yok

**Lisans**: [LICENSE](LICENSE)

---

## Destek / Support

### S16: Hata buldum, ne yapmalıyım?

**C**:

1. GitHub Issues açın
2. Hatayı detaylı açıklayın
3. Kod örneği ekleyin
4. Hata mesajını paylaşın

**Link**: GitHub Issues

---

### S17: Katkıda bulunmak istiyorum

**C**: Harika! Yapabilecekleriniz:

- 🐛 Hata düzeltmeleri
- 📚 Dokümantasyon iyileştirmeleri
- ✨ Yeni özellikler
- 📊 Veri setleri (lisans uygunsa)
- 🧪 Testler

**Pull Request gönderin!**

---

### S18: Daha fazla yardım?

**C**: Kaynaklar:

- 📖 **Dokümantasyon**: `docs/` dizini
- 💬 **GitHub Issues**: Sorular ve tartışma
- 📚 **Örnekler**: `examples/` dizini
- 🎓 **Tutorial**: Jupyter notebook

---

## Hızlı Referans / Quick Reference

### Önemli Dosyalar

- 📊 **TRAINING-DATA-STATUS.md** - Eğitim verisi durumu
- 📖 **docs/EGITIM.md** - Eğitim rehberi
- 🔧 **docs/OPTIMIZASYON.md** - İpuçları
- 📚 **docs/API.md** - API dokümantasyonu
- ⚡ **HIZLI-BASLANGIC.md** - Hızlı başlangıç

### Önemli Komutlar

```bash
# Test çalıştır
python run_tests.py

# Demo
python demo.py

# OCR yap
python scripts/osmanlica_ocr.py resim.jpg

# Model eğit
python scripts/train_tesseract.py --action finetune

# Değerlendir
python scripts/evaluate.py --test-dir test/
```

---

**Güncelleme**: 2026-02-16  
**Soru/öneri?** GitHub Issues açın!
