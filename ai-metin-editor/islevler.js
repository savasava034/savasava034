// Uygulama Durumu
const uygulamaDurumu = {
    yapayzekaTipi: 'openai',
    erisimAnahtari: null,
    seciliModel: 'gpt-4-turbo',
    yukluDosyalar: [],
    sohbetGecmisi: [],
    kaydedilmisMetin: ''
};

// LocalStorage'dan ayarları yükle
function ayarlariYukle() {
    const kaydedilmisAnahtar = localStorage.getItem('yzErisimKodu');
    const kaydedilmisTema = localStorage.getItem('yzTema');
    const kaydedilmisTip = localStorage.getItem('yzTip');
    
    if (kaydedilmisAnahtar) {
        uygulamaDurumu.erisimAnahtari = kaydedilmisAnahtar;
        document.getElementById('erisim-kodu').value = kaydedilmisAnahtar;
    }
    
    if (kaydedilmisTema) {
        temaDegistir(kaydedilmisTema);
    }
    
    if (kaydedilmisTip) {
        uygulamaDurumu.yapayzekaTipi = kaydedilmisTip;
        document.getElementById('yapayzeka-secici').value = kaydedilmisTip;
    }
}

// Tema değiştirme fonksiyonu
function temaDegistir(temaismi) {
    const govde = document.body;
    govde.className = '';
    if (temaismi !== 'koyu-mavi') {
        govde.classList.add(temaismi);
    }
    localStorage.setItem('yzTema', temaismi);
}

// İstatistikleri güncelle
function istatistikleriGuncelle() {
    const yaziAlani = document.getElementById('yazi-tuvali');
    const metin = yaziAlani.innerText || '';
    
    const kelimeler = metin.trim().split(/\s+/).filter(k => k.length > 0);
    const kelimeSayisi = kelimeler.length;
    const karakterSayisi = metin.length;
    const sayfaTahmini = Math.ceil(kelimeSayisi / 250);
    
    document.getElementById('kelime-sayaci').textContent = `Kelime: ${kelimeSayisi}`;
    document.getElementById('karakter-sayaci').textContent = `Harf: ${karakterSayisi}`;
    document.getElementById('sayfa-tahmini').textContent = `Sayfa: ${sayfaTahmini}`;
}

// Mesaj ekleme fonksiyonu
function mesajEkle(gonderen, icerik) {
    const mesajAlani = document.getElementById('mesaj-alani');
    const yeniMesaj = document.createElement('div');
    yeniMesaj.className = `mesaj ${gonderen === 'kullanici' ? 'kullanici-mesaji' : 'asistan-mesaji'}`;
    
    const gonderenAdi = document.createElement('strong');
    gonderenAdi.className = 'gonderen-adi';
    gonderenAdi.textContent = gonderen === 'kullanici' ? 'Siz:' : 'Yardımcı:';
    
    const mesajMetni = document.createElement('span');
    mesajMetni.className = 'mesaj-metni';
    mesajMetni.textContent = icerik;
    
    yeniMesaj.appendChild(gonderenAdi);
    yeniMesaj.appendChild(mesajMetni);
    mesajAlani.appendChild(yeniMesaj);
    
    mesajAlani.scrollTop = mesajAlani.scrollHeight;
    
    uygulamaDurumu.sohbetGecmisi.push({gonderen, icerik, zaman: new Date()});
}

// AI ile iletişim
async function yapayzekayaCagriYap(komut, metin) {
    if (!uygulamaDurumu.erisimAnahtari) {
        return 'Lütfen önce API erişim kodunuzu girin ve kaydedin.';
    }
    
    const sistemMesaji = `Sen Türkçe yazı editörü için bir asistansın. Kullanıcının metin üzerinde yapmak istediği işlemleri anla ve uygula. Mevcut metin: "${metin.substring(0, 500)}..."`;
    
    try {
        if (uygulamaDurumu.yapayzekaTipi === 'openai') {
            return await openaiCagrisi(komut, sistemMesaji);
        } else if (uygulamaDurumu.yapayzekaTipi === 'anthropic') {
            return await anthropicCagrisi(komut, sistemMesaji);
        } else if (uygulamaDurumu.yapayzekaTipi === 'google') {
            return await geminiCagrisi(komut, sistemMesaji);
        }
    } catch (hata) {
        console.error('AI çağrısında hata:', hata);
        return `Bir hata oluştu: ${hata.message}. Lütfen API anahtarınızı ve internet bağlantınızı kontrol edin.`;
    }
}

// OpenAI API çağrısı
async function openaiCagrisi(komut, sistem) {
    const yanit = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${uygulamaDurumu.erisimAnahtari}`
        },
        body: JSON.stringify({
            model: uygulamaDurumu.seciliModel,
            messages: [
                {role: 'system', content: sistem},
                {role: 'user', content: komut}
            ],
            temperature: 0.7,
            max_tokens: 2000
        })
    });
    
    if (!yanit.ok) {
        const hata = await yanit.json();
        throw new Error(hata.error?.message || 'API isteği başarısız oldu');
    }
    
    const veri = await yanit.json();
    return veri.choices[0].message.content;
}

// Anthropic API çağrısı
async function anthropicCagrisi(komut, sistem) {
    const yanit = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-api-key': uygulamaDurumu.erisimAnahtari,
            'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
            model: uygulamaDurumu.seciliModel,
            max_tokens: 2000,
            system: sistem,
            messages: [
                {role: 'user', content: komut}
            ]
        })
    });
    
    if (!yanit.ok) {
        const hata = await yanit.json();
        throw new Error(hata.error?.message || 'API isteği başarısız oldu');
    }
    
    const veri = await yanit.json();
    return veri.content[0].text;
}

// Google Gemini API çağrısı
async function geminiCagrisi(komut, sistem) {
    const yanit = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${uygulamaDurumu.erisimAnahtari}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            contents: [{
                parts: [{
                    text: `${sistem}\n\nKullanıcı talebi: ${komut}`
                }]
            }]
        })
    });
    
    if (!yanit.ok) {
        const hata = await yanit.json();
        throw new Error(hata.error?.message || 'API isteği başarısız oldu');
    }
    
    const veri = await yanit.json();
    return veri.candidates[0].content.parts[0].text;
}

// Komutu işle ve metni güncelle
async function komutuIsle() {
    const komutGirisi = document.getElementById('komut-girisi');
    const komut = komutGirisi.value.trim();
    
    if (!komut) return;
    
    mesajEkle('kullanici', komut);
    komutGirisi.value = '';
    
    const yaziAlani = document.getElementById('yazi-tuvali');
    const mevcutMetin = yaziAlani.innerText;
    
    const gonderDugmesi = document.getElementById('gonder-dugme');
    gonderDugmesi.disabled = true;
    gonderDugmesi.classList.add('yukleniyor-efekt');
    
    const yanit = await yapayzekayaCagriYap(komut, mevcutMetin);
    
    gonderDugmesi.disabled = false;
    gonderDugmesi.classList.remove('yukleniyor-efekt');
    
    mesajEkle('asistan', yanit);
    
    // Eğer yanıt metni değiştirmeyi içeriyorsa otomatik uygula
    if (komut.toLowerCase().includes('sil') || 
        komut.toLowerCase().includes('ekle') || 
        komut.toLowerCase().includes('değiştir') ||
        komut.toLowerCase().includes('düzelt')) {
        
        // Basit otomasyon - gerçek uygulamada daha gelişmiş olmalı
        yaziAlani.innerText = yanit;
        istatistikleriGuncelle();
    }
}

// Dosya yükleme işlemi
function dosyaYukle(olay) {
    const dosyalar = Array.from(olay.target.files);
    const dosyaListesi = document.getElementById('yuklenen-dosyalar');
    
    dosyalar.forEach(dosya => {
        const okuyucu = new FileReader();
        
        okuyucu.onload = (e) => {
            uygulamaDurumu.yukluDosyalar.push({
                isim: dosya.name,
                icerik: e.target.result,
                boyut: dosya.size,
                tip: dosya.type
            });
            
            const dosyaOgesi = document.createElement('div');
            dosyaOgesi.style.marginTop = '4px';
            dosyaOgesi.style.padding = '4px';
            dosyaOgesi.style.background = 'var(--zemin-ucuncul)';
            dosyaOgesi.style.borderRadius = '4px';
            dosyaOgesi.textContent = `✓ ${dosya.name} (${Math.round(dosya.size / 1024)} KB)`;
            dosyaListesi.appendChild(dosyaOgesi);
        };
        
        okuyucu.readAsText(dosya);
    });
}

// Belge kaydetme
function belgeKaydet() {
    const yaziAlani = document.getElementById('yazi-tuvali');
    const metin = yaziAlani.innerText;
    
    const blob = new Blob([metin], {type: 'text/plain;charset=utf-8'});
    const url = URL.createObjectURL(blob);
    const indirmeLinki = document.createElement('a');
    
    const tarih = new Date();
    const dosyaIsmi = `belge_${tarih.getFullYear()}${(tarih.getMonth()+1).toString().padStart(2,'0')}${tarih.getDate().toString().padStart(2,'0')}_${tarih.getHours()}${tarih.getMinutes()}.txt`;
    
    indirmeLinki.href = url;
    indirmeLinki.download = dosyaIsmi;
    indirmeLinki.click();
    
    URL.revokeObjectURL(url);
    
    mesajEkle('asistan', `Belgeniz "${dosyaIsmi}" olarak kaydedildi.`);
}

// Yazdırma fonksiyonu
function yazdir() {
    window.print();
}

// Yeni belge
function yeniBelge() {
    if (confirm('Mevcut çalışmanız silinecek. Devam etmek istiyor musunuz?')) {
        document.getElementById('yazi-tuvali').innerText = '';
        istatistikleriGuncelle();
        mesajEkle('asistan', 'Yeni bir belge oluşturuldu. İyi çalışmalar!');
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    ayarlariYukle();
    istatistikleriGuncelle();
    
    // API anahtar kaydetme
    document.getElementById('kaydet-dugme').addEventListener('click', () => {
        const anahtar = document.getElementById('erisim-kodu').value.trim();
        if (anahtar) {
            uygulamaDurumu.erisimAnahtari = anahtar;
            localStorage.setItem('yzErisimKodu', anahtar);
            mesajEkle('asistan', 'API erişim kodunuz güvenli bir şekilde kaydedildi.');
        }
    });
    
    // AI tipi değişimi
    document.getElementById('yapayzeka-secici').addEventListener('change', (e) => {
        uygulamaDurumu.yapayzekaTipi = e.target.value;
        localStorage.setItem('yzTip', e.target.value);
    });
    
    // Model seçimi
    document.getElementById('model-secimi').addEventListener('change', (e) => {
        uygulamaDurumu.seciliModel = e.target.value;
    });
    
    // Tema değişimi
    document.getElementById('tema-degistirici').addEventListener('change', (e) => {
        temaDegistir(e.target.value);
    });
    
    // Dosya yükleme
    document.getElementById('dosya-yukleyici').addEventListener('change', dosyaYukle);
    
    // Komut gönderme
    document.getElementById('gonder-dugme').addEventListener('click', komutuIsle);
    
    // Enter ile gönderme
    document.getElementById('komut-girisi').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            komutuIsle();
        }
    });
    
    // Metin değişikliği izleme
    document.getElementById('yazi-tuvali').addEventListener('input', istatistikleriGuncelle);
    
    // Toolbar butonları
    document.getElementById('yeni-belge').addEventListener('click', yeniBelge);
    document.getElementById('kaydet-belge').addEventListener('click', belgeKaydet);
    document.getElementById('disa-aktar').addEventListener('click', belgeKaydet);
    document.getElementById('yazdir').addEventListener('click', yazdir);
});

// Otomatik kaydetme (her 2 dakikada)
setInterval(() => {
    const yaziAlani = document.getElementById('yazi-tuvali');
    const metin = yaziAlani.innerText;
    if (metin !== uygulamaDurumu.kaydedilmisMetin) {
        localStorage.setItem('yzOtomatikKayit', metin);
        uygulamaDurumu.kaydedilmisMetin = metin;
        console.log('Otomatik kayıt yapıldı');
    }
}, 120000);

// Sayfa yüklendiğinde otomatik kaydedilmiş metni geri yükle
window.addEventListener('load', () => {
    const otomatikKayit = localStorage.getItem('yzOtomatikKayit');
    if (otomatikKayit) {
        const yaziAlani = document.getElementById('yazi-tuvali');
        if (yaziAlani.innerText.trim() === '') {
            yaziAlani.innerText = otomatikKayit;
            istatistikleriGuncelle();
            mesajEkle('asistan', 'Önceki çalışmanız geri yüklendi.');
        }
    }
});
