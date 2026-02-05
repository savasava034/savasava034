# 📝 AI Destekli Metin Editörü

Yapay zeka entegrasyonlu, modern ve kullanıcı dostu bir metin editörü. Tüm metin düzenleme işlemlerinizi yapay zeka asistanıyla sohbet ederek gerçekleştirin!

## ✨ Özellikler

### 🎨 Arayüz
- **Geniş Yazı Alanı**: 100+ sayfalık uzun metinler için optimize edilmiş canvas tarzı editör
- **Yan Chat Paneli**: Tüm işlemleri komutlarla yapabileceğiniz AI asistanı
- **Koyu Temalar**: 4 farklı uyumlu koyu ton (Mavi, Mor, Yeşil, Gri)
- **Türkçe Arayüz**: Tamamen Türkçe kullanıcı deneyimi
- **Responsive Tasarım**: Masaüstü ve tablet uyumlu

### 🤖 Yapay Zeka Özellikleri
- **Çoklu AI Desteği**: OpenAI, Anthropic Claude, Google Gemini
- **Komutla Düzenleme**: Metne dokunmadan tüm işlemleri chat üzerinden yapın
- **Akıllı Analiz**: Yüklediğiniz belgelerden bilgi çekme ve analiz
- **Otomatik İşlemler**: 
  - Yazım hatası düzeltme
  - Özet çıkarma
  - Paragraf düzenleme
  - Başlık ekleme
  - İçerik genişletme

### 💾 Dosya Yönetimi
- **Belge Yükleme**: TXT, MD, DOC, DOCX, PDF desteği
- **Otomatik Kaydetme**: Her 2 dakikada otomatik yedekleme
- **Dışa Aktarma**: TXT formatında indirme
- **Yazdırma**: Doğrudan yazdırma desteği

### 📊 Canlı İstatistikler
- Kelime sayısı
- Karakter sayısı
- Tahmini sayfa sayısı

## 🚀 Kurulum ve Kullanım

### 1. Dosyaları İndirin
```bash
git clone https://github.com/savasava034/savasava034.git
cd savasava034/ai-metin-editor
```

### 2. Tarayıcıda Açın
`index.html` dosyasını çift tıklayarak herhangi bir modern web tarayıcısında açabilirsiniz. Sunucu kurulumuna gerek yoktur!

Alternatif olarak, yerel bir sunucu başlatmak için:
```bash
# Python 3 ile
python -m http.server 8000

# Node.js ile
npx http-server
```

Sonra tarayıcınızda `http://localhost:8000` adresini açın.

### 3. API Anahtarı Alın

#### OpenAI için:
1. https://platform.openai.com/api-keys adresine gidin
2. Hesap oluşturun veya giriş yapın
3. "Create new secret key" butonuna tıklayın
4. Anahtarı kopyalayın

#### Anthropic (Claude) için:
1. https://console.anthropic.com/ adresine gidin
2. API Keys bölümünden yeni anahtar oluşturun

#### Google Gemini için:
1. https://makersuite.google.com/app/apikey adresine gidin
2. "Create API Key" butonuna tıklayın

### 4. Uygulamayı Yapılandırın
1. Sol paneldeki "Yapılandırma" bölümünden AI sağlayıcısını seçin
2. API anahtarınızı yapıştırın
3. "Sakla" butonuna tıklayın
4. İstediğiniz temayı seçin

## 📖 Kullanım Kılavuzu

### Temel Komutlar

Chat panelinde aşağıdaki gibi komutlar yazabilirsiniz:

**Düzenleme Komutları:**
```
"İlk 3 paragrafı sil"
"Son cümleyi değiştir"
"Tüm metni başlıklara ayır"
"5. paragraftan sonra yeni bir bölüm ekle"
```

**İçerik İyileştirme:**
```
"Yazım hatalarını düzelt"
"Daha profesyonel bir dil kullan"
"Metni daha akıcı yap"
"Tekrarları kaldır"
```

**Analiz ve Özet:**
```
"Bu metnin özetini çıkar"
"Ana fikirler neler?"
"Metni 500 kelimeye indir"
"3 madde halinde özetle"
```

**İçerik Oluşturma:**
```
"Konuyla ilgili bir giriş paragrafı yaz"
"Sonuç bölümünü genişlet"
"Bu başlık altına örnek ekle"
"İstatistik ekleyerek güçlendir"
```

**Belge Analizi:**
```
"Yüklediğim belgeden önemli noktaları çıkar"
"Belgede geçen tarihleri listele"
"Belgelerden alıntı yaparak metni zenginleştir"
```

### Dosya İşlemleri

**Belge Yükleme:**
1. "Dosya Yükle" bölümünden dosyalarınızı seçin
2. Yüklenen dosyalar listede görünecektir
3. Chat'te bu dosyalara referans vererek bilgi alabilirsiniz

**Kaydetme:**
- 💾 simgesine tıklayarak manuel kaydedin
- Otomatik kaydetme her 2 dakikada çalışır
- Sayfa yeniden yüklendiğinde son hali geri gelir

**Yazdırma:**
- 🖨️ simgesine tıklayın
- Tarayıcı yazdırma penceresi açılacaktır

## ⚙️ Teknik Detaylar

### Desteklenen API'ler

**OpenAI (GPT-4 / GPT-3.5):**
```javascript
Endpoint: https://api.openai.com/v1/chat/completions
Models: gpt-4-turbo, gpt-3.5-turbo
```

**Anthropic (Claude):**
```javascript
Endpoint: https://api.anthropic.com/v1/messages
Models: claude-3-opus, claude-3-sonnet
```

**Google Gemini:**
```javascript
Endpoint: generativelanguage.googleapis.com/v1beta/models/gemini-pro
Model: gemini-pro
```

### Tarayıcı Uyumluluğu
- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Opera 76+

### Depolama
- API anahtarları ve tercihler tarayıcı LocalStorage'da saklanır
- Tüm veriler yerel cihazınızda kalır
- Güvenlik için HTTPS kullanımı önerilir

## 🎨 Tema Özelleştirme

CSS değişkenlerini düzenleyerek kendi temanızı oluşturabilirsiniz:

```css
body.ozel-tema {
    --zemin-birincil: #0b1426;
    --zemin-ikincil: #152038;
    --zemin-ucuncul: #1f2d4a;
    --vurgu-birincil: #5294e2;
    --vurgu-ikincil: #72b0ff;
    --yazi-ana: #eef1f9;
    --yazi-soluk: #b4bdd6;
    --kenari-renk: #2d3f62;
}
```

## 🔐 Güvenlik

- ⚠️ API anahtarlarınız tarayıcınızda LocalStorage'da saklanır
- 🔒 Anahtarlar şifrelenmiş olarak saklanmaz
- 🌐 Önemli işler için HTTPS sunucusu kullanın
- 🚫 API anahtarlarınızı asla paylaşmayın
- 🗑️ Kullanım sonrası tarayıcı geçmişini temizleyebilirsiniz

## 💡 İpuçları

1. **Verimli Komutlar**: Net ve spesifik komutlar daha iyi sonuç verir
2. **Küçük Adımlar**: Büyük değişiklikleri küçük parçalara bölün
3. **Geri Alma**: Ctrl+Z ile son değişiklikleri geri alabilirsiniz
4. **Düzenli Kaydetme**: Önemli metinleri sık sık kaydedin
5. **Tema Seçimi**: Uzun çalışmalarda gözünüzü yormayan temayı seçin

## 🐛 Sorun Giderme

**API Bağlantı Hatası:**
- API anahtarınızın doğru olduğundan emin olun
- İnternet bağlantınızı kontrol edin
- Tarayıcı konsolunu (F12) açarak hata mesajlarını inceleyin

**Otomatik Kayıt Çalışmıyor:**
- Tarayıcı LocalStorage'ı bloklamadığından emin olun
- Gizli modda çalışmıyor olabilir
- Tarayıcı çerezlerine izin verin

**Tema Değişmiyor:**
- Sayfayı yenileyin (F5)
- Tarayıcı önbelleğini temizleyin

## 📝 Lisans

Bu proje açık kaynaklıdır ve MIT lisansı altında sunulmaktadır.

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Pull request göndermekten çekinmeyin.

## 📧 İletişim

Sorularınız için GitHub Issues kullanabilirsiniz.

---

**Not:** Bu uygulama yerel olarak çalışır ve verileriniz yalnızca tarayıcınızda saklanır. API çağrıları dışında hiçbir veri internete gönderilmez.

🚀 **İyi yazılar!**
