# 🚀 Hızlı Başlangıç Kılavuzu

## 1. Uygulamayı Açın

### Yerel Olarak
Basitçe `index.html` dosyasına çift tıklayın. Modern herhangi bir tarayıcıda açılacaktır.

### HTTP Sunucusu İle (Önerilen)
```bash
# Python ile
cd ai-metin-editor
python -m http.server 8000

# Node.js ile
npx http-server

# Sonra tarayıcıda: http://localhost:8000
```

## 2. API Anahtarı Alın

### OpenAI için (Önerilen - En Güçlü)
1. https://platform.openai.com/signup adresine gidin
2. Hesap oluşturun (kredi kartı gerekli)
3. https://platform.openai.com/api-keys sayfasına gidin
4. "Create new secret key" butonuna tıklayın
5. Anahtarı kopyalayın (sk-... ile başlar)

**Maliyet**: ~$0.01-0.03 per 1000 kelime (GPT-4 Turbo)

### Anthropic Claude için
1. https://console.anthropic.com adresine gidin
2. "Get API Keys" bölümüne gidin
3. Yeni anahtar oluşturun

**Maliyet**: ~$0.015 per 1000 kelime (Claude 3)

### Google Gemini için (Ücretsiz Başlangıç)
1. https://makersuite.google.com/app/apikey adresine gidin
2. Google hesabınızla giriş yapın
3. "Create API Key" butonuna tıklayın

**Maliyet**: İlk 60 istek/dakika ücretsiz

## 3. Uygulamayı Yapılandırın

1. **Sol üst köşedeki "Yapılandırma" bölümünden**:
   - AI Sağlayıcısını seçin (OpenAI, Anthropic, Google)
   - API Anahtarınızı girin
   - "Sakla" butonuna tıklayın ✅

2. **Model seçin**:
   - GPT-4 Turbo (en güçlü, en pahalı)
   - GPT-3.5 Turbo (hızlı, uygun fiyat)
   - Claude 3 Opus (dengeli)
   - Gemini Pro (ücretsiz başlangıç)

3. **Temayı seçin**:
   - Koyu Mavi (varsayılan)
   - Koyu Mor
   - Koyu Yeşil
   - Koyu Gri

## 4. Yazmaya Başlayın!

### Direkt Yazma
Sağ taraftaki büyük alana tıklayın ve yazmaya başlayın. İstatistikler otomatik güncellenir.

### AI ile Yazma
Sol alttaki chat paneline komutlar yazın:

**Temel Komutlar**:
```
"Teknoloji hakkında 3 paragraf yaz"
"Bu konuda bir giriş paragrafı ekle"
"Sonuç bölümü yaz"
```

**Düzenleme Komutları**:
```
"İlk paragrafı sil"
"Son cümleyi değiştir"
"2. paragrafı daha detaylı yap"
"Tüm metni başlıklara ayır"
```

**İyileştirme Komutları**:
```
"Yazım hatalarını düzelt"
"Daha profesyonel bir dil kullan"
"Metni daha akıcı yap"
"Tekrarları kaldır"
```

**Analiz Komutları**:
```
"Bu metnin özetini çıkar"
"Ana fikirleri listele"
"Metni 500 kelimeye indir"
```

## 5. Dosya İşlemleri

### Belge Yükleme
1. "Dosya Yükle" bölümüne tıklayın
2. Dosyalarınızı seçin (TXT, MD, DOC, DOCX, PDF)
3. Yüklenen dosyalar listede görünür
4. Chat'te bu dosyalara referans vererek bilgi alabilirsiniz

**Örnek**:
```
"Yüklediğim belgeden önemli noktaları çıkar"
"Belgedeki tarihleri listele"
```

### Kaydetme
- **Otomatik**: Her 2 dakikada otomatik kaydedilir
- **Manuel**: 💾 butonuna tıklayarak TXT olarak indirin
- **Oturum**: Sayfa kapanıp açılsa bile son hali gelir

### Yazdırma
🖨️ butonuna tıklayın, tarayıcı yazdırma penceresi açılır.

## 6. İpuçları

### 💡 Verimli Kullanım
1. **Net Komutlar**: "Düzelt" yerine "Yazım hatalarını düzelt" deyin
2. **Küçük Adımlar**: Büyük değişiklikleri parçalara bölün
3. **Geri Alma**: Ctrl+Z ile metin değişikliklerini geri alabilirsiniz
4. **Düzenli Kaydetme**: Önemli metinleri manuel kaydedin

### ⚡ Performans
- Uzun metinler (10,000+ kelime) için GPT-4 Turbo öneriyoruz
- Hızlı düzenlemeler için GPT-3.5 Turbo yeterli
- İlk denemeler için Gemini Pro ücretsiz

### 🔐 Güvenlik
- API anahtarınızı kimseyle paylaşmayın
- Hassas içerikler için OpenAI'ın gizlilik politikasını okuyun
- İş bilgisayarında kullanıyorsanız çıkışta tarayıcı geçmişini temizleyin

### 🎨 Özelleştirme
- `tema.css` dosyasını düzenleyerek kendi temanızı oluşturabilirsiniz
- CSS değişkenlerini değiştirmeniz yeterli

## 7. Sorun Giderme

### ❌ "API isteği başarısız oldu"
**Çözüm**:
- API anahtarınızı kontrol edin
- İnternet bağlantınızı kontrol edin
- API limitinizi aşmamış olduğunuzdan emin olun
- F12 ile konsolu açıp hata detaylarına bakın

### ❌ "API anahtarı geçersiz"
**Çözüm**:
- Anahtarı yeniden kopyalayın (boşluk olmasın)
- Doğru sağlayıcıyı seçtiğinizden emin olun
- API hesabınızın aktif olduğunu kontrol edin

### ❌ "Tema değişmiyor"
**Çözüm**:
- Sayfayı yenileyin (F5)
- Tarayıcı önbelleğini temizleyin (Ctrl+Shift+Del)

### ❌ "Otomatik kayıt çalışmıyor"
**Çözüm**:
- Tarayıcınızın çerezlere izin verdiğinden emin olun
- Gizli modda çalışmıyorsanız kontrol edin
- LocalStorage'ın bloke edilmediğinden emin olun

## 8. Klavye Kısayolları

- **Enter**: Chat'te mesaj gönder
- **Shift+Enter**: Chat'te yeni satır
- **Ctrl+Z**: Geri al (metin alanında)
- **Ctrl+Y**: Yinele (metin alanında)
- **Ctrl+S**: Kaydet (önerilen: manuel kaydetme)
- **Ctrl+P**: Yazdır

## 9. Sınırlamalar

- ⚠️ API çağrıları ücretlidir (ücretsiz kotalar hariç)
- ⚠️ Çok uzun metinler (50,000+ kelime) token limitine takılabilir
- ⚠️ Görsel/resim düzenleme desteği yok
- ⚠️ Gerçek zamanlı işbirliği yok

## 10. İleri Düzey

### Kendi AI Modelinizi Kullanma
`islevler.js` dosyasında yeni bir fonksiyon ekleyerek kendi API'nizi entegre edebilirsiniz:

```javascript
async function kendiModelimCagrisi(komut, sistem) {
    const yanit = await fetch('https://your-api.com/endpoint', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${uygulamaDurumu.erisimAnahtari}`
        },
        body: JSON.stringify({prompt: komut})
    });
    const veri = await yanit.json();
    return veri.response;
}
```

### Özel Prompts
Sistem promptlarını düzenleyerek AI'ın davranışını değiştirebilirsiniz.

## 📞 Yardım

Sorunuz mu var? 
- GitHub Issues: https://github.com/savasava034/savasava034/issues
- README.md dosyasında detaylı bilgi

---

**Keyifli yazılar! 🚀**
