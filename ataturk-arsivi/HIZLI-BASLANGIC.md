# 🚀 Hızlı Başlangıç Kılavuzu - Atatürk Arşiv Sistemi

## 5 Dakikada Başlayın!

### Adım 1: Örnek Verileri Yükleyin (30 saniye)

```bash
cd ataturk-arsivi/araclar
python3 ornek_veri_yukle.py
```

Bu komut 20+ ünlü Atatürk sözünü otomatik olarak arşive yükler.

**Çıktı:**
```
✅ Başarıyla eklenen: 20
⚠️  Tekrarlı (atlandı): 0
❌ Hata: 0
```

### Adım 2: İnteraktif Arayüzü Başlatın (1 dakika)

```bash
python3 interaktif_arayuz.py
```

**Menü seçenekleri:**
```
1. 📝 Yeni söz ekle
2. 🔍 Arşivde ara
3. 📊 İstatistikleri görüntüle
4. 📖 Tüm sözleri listele
5. 🏷️  Kategoriye göre listele
6. 💾 Dışa aktar (JSON/TXT/MD)
7. 📥 Örnek verileri yükle
0. 🚪 Çıkış
```

### Adım 3: İlk Arama Yapın (30 saniye)

Menüden **2** seçin ve:
- Anahtar kelime: `gençlik`
- Enter ile devam edin

**Sonuç:**
```
✅ 3 sonuç bulundu:
- Ey Türk gençliği! Birinci vazifen...
- Ben Türk evladının yapamayacağı iş yoktur...
- Fikri hür, vicdanı hür...
```

### Adım 4: Yeni Söz Ekleyin (1 dakika)

Menüden **1** seçin ve:
```
💬 Söz: Muallim, yeni nesli sen yetiştireceksin.
🏷️  Kategoriler: Eğitim, Öğretmen
📅 Tarih: 1922-11-24
📚 Kaynak: Öğretmenler Günü
```

**Sonuç:**
```
✅ Söz başarıyla eklendi! (ID: 21)
```

### Adım 5: Dışa Aktarın (30 saniye)

Menüden **6** seçin:
```
Format seçin:
  3. MD (Markdown)

Dosya adı: ataturk_sozleri.md
```

**Sonuç:**
```
✅ Arşiv 'ataturk_sozleri.md' dosyasına aktarıldı!
```

## 🎯 Hemen Kullanım: Python API

### Basit Örnek (30 saniye)

```python
from arsiv_yoneticisi import AtaturkArsivi

# Arşiv oluştur
arsiv = AtaturkArsivi()

# Söz ekle
arsiv.soz_ekle(
    metin="Hayatta en hakiki mürşit ilimdir, fendir.",
    kategori=["Bilim", "Eğitim"]
)

# Ara
sonuclar = arsiv.ara(kategori="Eğitim")
print(f"Bulunan: {len(sonuclar)} söz")

# İstatistikler
istat = arsiv.istatistikler()
print(f"Toplam: {istat['toplam_kayit']} söz")
```

### Gelişmiş Örnek (2 dakika)

```python
from arsiv_yoneticisi import AtaturkArsivi

# Özel dosya yolu ile arşiv oluştur
arsiv = AtaturkArsivi("ozel/yolum/sozler.json")

# Toplu ekleme
sozler_listesi = [
    {
        "metin": "Egemenlik kayıtsız şartsız milletindir.",
        "kategori": ["Cumhuriyet"],
        "tarih": "1920-04-23"
    },
    {
        "metin": "Yurtta sulh, cihanda sulh.",
        "kategori": ["Barış"],
        "tarih": "1933-10-29"
    }
]

istatistik = arsiv.toplu_ekle(sozler_listesi)
print(f"Eklenen: {istatistik['eklenen']}")
print(f"Tekrar: {istatistik['tekrar']}")

# Gelişmiş arama
sonuclar = arsiv.ara(
    anahtar_kelime="cumhuriyet",
    kategori="Demokrasi"
)

# Her sonucu yazdır
for soz in sonuclar:
    arsiv.yazdir_soz(soz)

# Dışa aktar
arsiv.disa_aktar("arsiv.md", format="md")
```

## 🧪 Tekrar Testi (1 dakika)

Aynı sözü farklı formatlarda eklemeyi deneyin:

```python
from arsiv_yoneticisi import AtaturkArsivi

arsiv = AtaturkArsivi()

# İlk ekleme - başarılı
arsiv.soz_ekle("Hayatta en hakiki mürşit ilimdir, fendir.")
# Sonuç: ✅ Söz başarıyla eklendi!

# İkinci ekleme - aynı söz
arsiv.soz_ekle("Hayatta en hakiki mürşit ilimdir fendir")
# Sonuç: ⚠️ Bu söz zaten arşivde mevcut!

# Üçüncü ekleme - büyük harfle
arsiv.soz_ekle("HAYATTA EN HAKİKİ MÜRŞİT İLİMDİR, FENDİR.")
# Sonuç: ⚠️ Bu söz zaten arşivde mevcut!
```

**Başarı!** ✅ Sistem tekrarları başarıyla engelledi.

## 📊 İstatistik Örneği (30 saniye)

```python
from arsiv_yoneticisi import AtaturkArsivi

arsiv = AtaturkArsivi()
istat = arsiv.istatistikler()

print(f"📈 Arşiv İstatistikleri:")
print(f"   Toplam Söz: {istat['toplam_kayit']}")
print(f"   Toplam Kelime: {istat['toplam_kelime']}")
print(f"   Ortalama Uzunluk: {istat['ortalama_kelime']} kelime")

print(f"\n🏷️  Kategori Dağılımı:")
for kat, sayi in istat['kategori_dagilimi'].items():
    print(f"   {kat}: {sayi} söz")
```

**Çıktı:**
```
📈 Arşiv İstatistikleri:
   Toplam Söz: 20
   Toplam Kelime: 212
   Ortalama Uzunluk: 10 kelime

🏷️  Kategori Dağılımı:
   Eğitim: 7 söz
   Cumhuriyet: 4 söz
   Bilim: 3 söz
   ...
```

## 🔍 Arama Örnekleri (2 dakika)

### Basit Arama
```python
# Kelime araması
egitim = arsiv.ara(anahtar_kelime="eğitim")

# Kategori araması
bilim = arsiv.ara(kategori="Bilim")

# Tarih araması
yil_1927 = arsiv.ara(tarih="1927")
```

### Gelişmiş Arama
```python
# Çoklu kriter
sonuc = arsiv.ara(
    anahtar_kelime="cumhuriyet",
    kategori="Demokrasi",
    tarih="1920-04-23"
)

# Kaynak bazlı
nutuk = arsiv.ara(kaynak="Nutuk")
```

## 💾 Dışa Aktarma Örnekleri (1 dakika)

```python
from arsiv_yoneticisi import AtaturkArsivi

arsiv = AtaturkArsivi()

# JSON (programatik kullanım)
arsiv.disa_aktar("arsiv.json", format="json")

# TXT (düz metin)
arsiv.disa_aktar("arsiv.txt", format="txt")

# Markdown (GitHub, dokümantasyon)
arsiv.disa_aktar("arsiv.md", format="md")
```

## 🎓 Örnek Kullanım Senaryoları

### Senaryo 1: Öğretmen - Ders Materyali (5 dakika)
```python
# 1. Eğitim kategorisindeki tüm sözleri bul
egitim_sozleri = arsiv.ara(kategori="Eğitim")

# 2. Markdown olarak kaydet
arsiv.disa_aktar("egitim_sozleri.md", format="md")

# 3. Öğrencilere dağıt
```

### Senaryo 2: Araştırmacı - Söz Analizi (10 dakika)
```python
# 1. Tüm sözleri al
tum_sozler = arsiv.veriler["sozler"]

# 2. Kelime sayısı analizi
uzun_sozler = [s for s in tum_sozler if s["kelime_sayisi"] > 15]
kisa_sozler = [s for s in tum_sozler if s["kelime_sayisi"] < 10]

# 3. Kategori analizi
istat = arsiv.istatistikler()
en_cok_kullanilan = max(istat['kategori_dagilimi'].items(), 
                        key=lambda x: x[1])
```

### Senaryo 3: Kişisel Kullanım - Koleksiyon (sürekli)
```python
# Her gün yeni bir söz ekle
arsiv.soz_ekle(
    metin="Bugün bulduğum Atatürk sözü...",
    kategori=["İlgili Kategori"],
    notlar="Nereden bulduğum: ..."
)

# Aylık yedekle
arsiv.disa_aktar(f"yedek_{datetime.now().strftime('%Y-%m')}.json", 
                 format="json")
```

## ⚡ Hızlı Referans

### Temel Komutlar
```bash
# Örnek verileri yükle
python3 ornek_veri_yukle.py

# İnteraktif arayüz
python3 interaktif_arayuz.py

# Ana modül test
python3 arsiv_yoneticisi.py
```

### Python API
```python
# Arşiv oluştur
arsiv = AtaturkArsivi()

# Söz ekle
arsiv.soz_ekle(metin, kategori, tarih, kaynak)

# Ara
arsiv.ara(anahtar_kelime, kategori, tarih, kaynak)

# İstatistikler
arsiv.istatistikler()

# Dışa aktar
arsiv.disa_aktar(dosya_adi, format)
```

## 🎯 Sonraki Adımlar

1. ✅ **5 Dakikada**: Örnek verileri yükleyin
2. ✅ **10 Dakikada**: İnteraktif arayüzü keşfedin
3. ✅ **30 Dakikada**: Python API ile kod yazın
4. ✅ **1 Saatte**: Kendi sözlerinizi ekleyin
5. ✅ **Sürekli**: Arşivinizi geliştirin

## 💡 İpuçları

- **Tutarlı kategoriler kullanın**: Her zaman aynı kategori isimlerini kullanın
- **Tarih formatı**: YYYY-MM-DD formatını tercih edin
- **Kaynak belirtin**: Her söz için kaynak ekleyin
- **Düzenli yedekleyin**: Dışa aktarma ile yedek alın
- **İstatistikleri takip edin**: Arşiv büyümesini izleyin

## 🆘 Sorun Giderme

**Soru:** Aynı söz eklenmeye çalışılınca ne olur?  
**Cevap:** Sistem ⚠️ uyarısı verir ve eklemez.

**Soru:** Veri nerede saklanır?  
**Cevap:** `veriler/sozler.json` dosyasında.

**Soru:** İnternet gerekir mi?  
**Cevap:** Hayır, tamamen yerel çalışır.

**Soru:** Kategoriler sınırlı mı?  
**Cevap:** Hayır, istediğiniz kategoriyi kullanabilirsiniz.

---

<div align="center">

**🇹🇷 Şimdi başlayın! 5 dakika içinde çalışan bir arşiviniz olacak.**

</div>
