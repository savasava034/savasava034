# 📚 200-300 Sayfa Osmanlıca Eğitim Verisi Ekleme Rehberi

## 🎯 Hedef

200-300 sayfa kaliteli, açık kaynak Osmanlıca belge ile model eğitimi.

## ⚠️ Önemli Not

**Manuel transkripsiyon gereklidir!** 200-300 sayfa transkribe etmek **100-300 saat** sürebilir. Bu rehber süreci optimize etmenize yardımcı olur.

---

## 🚀 Hızlı Başlangıç (3 Adım)

### Adım 1: Belgeleri İndirin

```bash
# Önerilen kaynakları gör
python scripts/collect_documents.py --action recommend

# Belge indir (örnek)
python scripts/collect_documents.py --action download --identifier kitbuttevhid00sade
```

### Adım 2: PDF'i Görüntülere Dönüştürün

```bash
# İndirilen PDF'i işle
python scripts/prepare_training_data.py \
    --pdf training-data/collected/belge.pdf \
    --max-pages 300 \
    --dpi 300
```

### Adım 3: Ground Truth Oluşturun

```bash
# Manuel transkripsiyon yapın
# Her training-data/ground-truth/*.gt.txt dosyasını düzenleyin
```

---

## 📖 Detaylı Rehber

### 1. Kaliteli Açık Kaynak Kaynaklar

#### A. Archive.org (Önerilen) ⭐

**En iyi seçenekler:**

1. **Kitab-üt Tevhid** (200 sayfa)
   - ID: `kitbuttevhid00sade`
   - Kalite: Çok yüksek (matbu, net)
   - Lisans: Public Domain
   - İndirme: `python scripts/collect_documents.py --action download --identifier kitbuttevhid00sade`

2. **Gülistan Tercümesi** (300 sayfa)
   - ID: `gulistn00saadi`
   - Kalite: Yüksek
   - Lisans: Public Domain

3. **Mevlid-i Şerif** (150 sayfa)
   - ID: `mevlidiveysihan00gazi`
   - Kalite: Çok yüksek
   - Lisans: Public Domain

**Manuel arama:**
```bash
# Archive.org'da ara
python scripts/collect_documents.py --action search --query "ottoman turkish books"
```

#### B. Wikisource (Transkripsiyon Var!) ⭐⭐⭐

**En Değerli**: Wikisource'ta bazı belgeler zaten transkribe edilmiş!

Örnekler:
- [Tanzimat Fermanı](https://tr.wikisource.org/wiki/Tanzimat_Fermanı)
- [Hatt-ı Hümayun](https://tr.wikisource.org/wiki/Gülhane_Hatt-ı_Hümayunu)
- [Osmanlı Kanunnameleri](https://tr.wikisource.org/wiki/Kategori:Kanunnameler)

**Avantaj**: Ground truth zaten var! Sadece görüntüyü ekleyin.

#### C. Diğer Kaynaklar

- **HathiTrust**: https://babel.hathitrust.org/
- **Gallica (BnF)**: https://gallica.bnf.fr/
- **İstanbul Üniversitesi Dijital Arşiv**

---

### 2. Belge İndirme

#### Otomatik İndirme

```bash
# Toplu indirme için liste oluştur
cat > belge_listesi.txt << EOF
kitbuttevhid00sade
gulistn00saadi
mevlidiveysihan00gazi
EOF

# Hepsini indir
while read id; do
    python scripts/collect_documents.py --action download --identifier "$id"
    sleep 5  # API'ye nezaket
done < belge_listesi.txt
```

#### Manuel İndirme

1. Archive.org'da belgeyi bulun
2. "Download Options" → PDF veya DjVu seçin
3. `training-data/collected/` dizinine kaydedin

---

### 3. PDF → PNG Dönüştürme

```bash
# Gerekli araçları kur
sudo apt-get install poppler-utils  # pdftoppm için

# PDF'i işle
python scripts/prepare_training_data.py \
    --pdf training-data/collected/belge.pdf \
    --max-pages 300 \
    --dpi 300 \
    --optimize
```

**Çıktı:**
- `training-data/images/belge-001.png` (sayfa 1)
- `training-data/images/belge-002.png` (sayfa 2)
- ...
- `training-data/images/belge-300.png` (sayfa 300)

---

### 4. Ground Truth Oluşturma (En Zor Kısım)

#### Yaklaşım 1: Manuel Transkripsiyon (En Doğru)

**Araçlar:**
- Herhangi bir metin editörü (UTF-8 destekli)
- Görüntü görüntüleyici (yan yana)

**Süreç:**
1. `training-data/images/belge-001.png` açın
2. `training-data/ground-truth/belge-001.gt.txt` düzenleyin
3. Metni satır satır transkribe edin
4. Kaydedin ve sonraki sayfaya geçin

**Süre**: ~10-30 dakika/sayfa (deneyime göre)

#### Yaklaşım 2: Yarı-Otomatik (Hızlı ama Hatalı)

**Transkribus kullanın** (önerilir):
- Website: https://readcoop.eu/transkribus/
- Özellik: HTR (Handwritten Text Recognition)
- Avantaj: Otomatik transkripsiyon + manuel düzeltme

**Adımlar:**
1. Transkribus'a kaydolun (ücretsiz)
2. Görüntüleri yükleyin
3. HTR modeli çalıştırın (Arapça/Ottoman seçin)
4. Sonuçları manuel olarak düzeltin
5. Eksport edin

**Süre**: ~5-10 dakika/sayfa

#### Yaklaşım 3: OCR + Manuel Düzeltme

```bash
# Mevcut Arapça model ile ön transkripsiyon
for img in training-data/images/*.png; do
    base=$(basename "$img" .png)
    tesseract "$img" "training-data/ground-truth/$base" -l ara
done

# Sonra her dosyayı manuel düzeltin
```

**Süre**: ~5-15 dakika/sayfa

#### Yaklaşım 4: Topluluk İşbirliği

**En Verimli!** Çok kişi paylaşırsa süre kısalır:

```
300 sayfa / 10 kişi = 30 sayfa/kişi
30 sayfa × 15 dakika = 7.5 saat/kişi
```

---

### 5. Kalite Kontrolü

```bash
# Ground truth dosyalarını kontrol et
python scripts/evaluate.py --test-dir training-data/images --gt-dir training-data/ground-truth
```

**Kontrol listesi:**
- [ ] Her görüntü için .gt.txt var mı?
- [ ] Dosyalar UTF-8 formatında mı?
- [ ] Boş dosya yok mu?
- [ ] Arapça karakterler doğru mu?

---

### 6. Model Eğitimi

```bash
# Fine-tuning (önerilen)
python scripts/train_tesseract.py \
    --action finetune \
    --base-model ara \
    --iterations 10000

# Değerlendirme
python scripts/evaluate.py \
    --test-dir test-set/images \
    --gt-dir test-set/ground-truth \
    --model models/osmanlica.traineddata
```

---

## 📊 Gerçekçi Süre Tahminleri

### Senaryo 1: Tek Kişi, Manuel

```
200 sayfa × 20 dakika/sayfa = 4,000 dakika = 67 saat
Günde 2 saat = 34 gün
```

### Senaryo 2: Tek Kişi, Transkribus

```
200 sayfa × 10 dakika/sayfa = 2,000 dakika = 33 saat
Günde 2 saat = 17 gün
```

### Senaryo 3: 5 Kişi, İşbirliği

```
200 sayfa / 5 kişi = 40 sayfa/kişi
40 × 10 dakika = 400 dakika = 7 saat/kişi
1 hafta içinde tamamlanabilir
```

---

## 🎯 Öncelikli Belgeler (Kalite Sırası)

### 1. Wikisource Belgeler (En Kolay) ⭐⭐⭐

**Neden**: Ground truth zaten var!

```
Toplam: ~50 sayfa
Süre: 2-3 saat (sadece görüntü ekleme)
```

### 2. Matbu Eserler (Kolay) ⭐⭐

**Örnekler**: Kitab-üt Tevhid, Gülistan

```
Toplam: 200-300 sayfa
Kalite: Çok yüksek (net baskı)
Süre: 30-50 saat (Transkribus ile)
```

### 3. El Yazması Eserler (Zor) ⭐

**Sadece ileri seviye için**

```
Süre: 2-3x daha uzun
Doğruluk: Daha düşük
```

---

## 💡 İpuçları ve Püf Noktaları

### Ground Truth İçin

1. **Kısaltmalar**: Osmanlıca'da çok var
   - Tam yazın, kısaltma olarak değil
   - Örnek: ص.ع.م → صلى الله عليه وسلم

2. **Satır Sonları**: Koruyun
   - Her satır yeni satırla bitsin
   - Sayfa düzeni önemli

3. **Noktalama**: Orijinale sadık kalın
   - Modern noktalama eklemeyin

4. **Belirsiz Karakterler**: İşaretleyin
   - `[?]` veya `[belirsiz]` kullanın

### Verimlilik İçin

1. **Klavye Düzeni**: Arapça klavye öğrenin
2. **Kısayollar**: Sık kullanılan kelimeler için
3. **Toplu İşlem**: Benzer sayfaları grup halinde
4. **Molalar**: Her saatte 10 dakika

---

## 📦 Hazır Veri Setleri (Eğer varsa)

**Şu anda bilinen açık kaynak Osmanlıca OCR veri seti yok.**

Ama oluşturursanız paylaşabilirsiniz:
- GitHub Release
- Zenodo (DOI ile)
- HuggingFace Datasets

---

## 🤝 Topluluk Katkısı

### Veri Paylaşımı

Eğer ground truth oluşturursanız:

1. **Lisans Kontrol**: Kamu malı mı?
2. **Paylaş**: GitHub'a ekleyin
3. **Belgelendirin**: Hangi kaynak, hangi tarih

### Katkıda Bulunma

```bash
# Fork edin
# Ground truth ekleyin
# Pull request gönderin
```

---

## 📞 Yardım

**Sorular için:**
- GitHub Issues
- `SSS.md` dosyası

**Araçlar:**
- Transkribus: https://readcoop.eu/transkribus/
- OCR4all: https://www.ocr4all.org/

---

## ✅ Kontrol Listesi

200-300 sayfa eklemek için:

- [ ] Kaynakları belirledim
- [ ] Lisansları kontrol ettim
- [ ] Belgeleri indirdim
- [ ] PDF'leri PNG'ye çevirdim
- [ ] Ground truth stratejisi seçtim
- [ ] Transkripsiyona başladım
- [ ] Kalite kontrolü yaptım
- [ ] Model eğitimine hazırım

---

**Başarılar!** 🎉

Bu iş zaman alır ama sonuçlar harika olacak!

**Güncelleme**: 2026-02-16
