// Basit Motor - OpenCanvas Tarzı

// Durum
const durum = {
    apiKey: null,
    model: 'gpt-4-turbo',
    tema: 'koyu'
};

// LocalStorage'dan yükle
function yukle() {
    const key = localStorage.getItem('apiKey');
    const model = localStorage.getItem('model');
    const tema = localStorage.getItem('tema');
    
    if (key) {
        durum.apiKey = key;
        document.getElementById('apiKey').value = key;
    }
    if (model) {
        durum.model = model;
        document.getElementById('aiModel').value = model;
    }
    if (tema) {
        durum.tema = tema;
        temaUygula(tema);
    }
}

// Tema uygula
function temaUygula(tema) {
    document.body.className = '';
    if (tema === 'acik') {
        document.body.classList.add('acik-tema');
    } else if (tema === 'mor') {
        document.body.classList.add('mor-tema');
    } else if (tema === 'yesil') {
        document.body.classList.add('yesil-tema');
    }
    durum.tema = tema;
    localStorage.setItem('tema', tema);
}

// İstatistik güncelle
function istatistikGuncelle() {
    const metin = document.getElementById('yaziCanvas').value;
    const kelimeler = metin.trim().split(/\s+/).filter(k => k.length > 0);
    
    document.getElementById('kelimeSayisi').textContent = `${kelimeler.length} kelime`;
    document.getElementById('karakterSayisi').textContent = `${metin.length} karakter`;
}

// Mesaj ekle
function mesajEkle(tip, icerik) {
    const kutu = document.getElementById('mesajKutusu');
    const mesaj = document.createElement('div');
    mesaj.className = tip === 'bot' ? 'bot-mesaj' : 'kullanici-mesaj';
    
    const baslik = document.createElement('strong');
    baslik.textContent = tip === 'bot' ? 'AI:' : 'Siz:';
    
    mesaj.appendChild(baslik);
    mesaj.appendChild(document.createTextNode(' ' + icerik));
    
    kutu.appendChild(mesaj);
    kutu.scrollTop = kutu.scrollHeight;
}

// AI çağrısı
async function aiCagir(komut) {
    if (!durum.apiKey) {
        return 'Lütfen API key girin ve kaydedin.';
    }
    
    const metin = document.getElementById('yaziCanvas').value;
    const sistem = `Sen bir yazı asistanısın. Kullanıcının isteklerini yerine getir. Uzun metinler yazabilirsin (100+ sayfa). Mevcut metin: "${metin.substring(0, 500)}..."`;
    
    try {
        const yanit = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${durum.apiKey}`
            },
            body: JSON.stringify({
                model: durum.model,
                messages: [
                    {role: 'system', content: sistem},
                    {role: 'user', content: komut}
                ],
                max_tokens: 4000,
                temperature: 0.7
            })
        });
        
        if (!yanit.ok) {
            const hata = await yanit.json();
            throw new Error(hata.error?.message || 'API hatası');
        }
        
        const veri = await yanit.json();
        return veri.choices[0].message.content;
    } catch (hata) {
        console.error('Hata:', hata);
        return `Hata: ${hata.message}`;
    }
}

// Komut gönder
async function komutGonder() {
    const giris = document.getElementById('komutGiris');
    const komut = giris.value.trim();
    
    if (!komut) return;
    
    mesajEkle('kullanici', komut);
    giris.value = '';
    
    const btn = document.getElementById('gonderBtn');
    btn.disabled = true;
    btn.textContent = '⏳';
    
    const yanit = await aiCagir(komut);
    
    btn.disabled = false;
    btn.textContent = '▶ Gönder';
    
    mesajEkle('bot', yanit);
    
    // Eğer yanıt metin içeriyorsa ve değiştirme komutuysa
    if (komut.toLowerCase().includes('yaz') || 
        komut.toLowerCase().includes('ekle') ||
        komut.toLowerCase().includes('değiştir')) {
        
        const canvas = document.getElementById('yaziCanvas');
        
        // Eğer "100 sayfa yaz" gibi komutsa, tüm metni değiştir
        if (komut.toLowerCase().includes('sayfa') || komut.length > 20) {
            canvas.value = yanit;
        } else {
            // Değilse sona ekle
            canvas.value += '\n\n' + yanit;
        }
        
        istatistikGuncelle();
    }
}

// Yeni belge
function yeniBelge() {
    if (confirm('Yeni belge oluşturulsun mu?')) {
        document.getElementById('yaziCanvas').value = '';
        istatistikGuncelle();
        mesajEkle('bot', 'Yeni belge hazır!');
    }
}

// Kaydet
function kaydet() {
    const metin = document.getElementById('yaziCanvas').value;
    const blob = new Blob([metin], {type: 'text/plain;charset=utf-8'});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    
    const tarih = new Date();
    const dosyaAdi = `belge_${tarih.getFullYear()}${(tarih.getMonth()+1).toString().padStart(2,'0')}${tarih.getDate().toString().padStart(2,'0')}.txt`;
    
    link.href = url;
    link.download = dosyaAdi;
    link.click();
    
    URL.revokeObjectURL(url);
    mesajEkle('bot', 'Belge kaydedildi!');
}

// Tema değiştir
let temaSayac = 0;
function temaDegistir() {
    const temalar = ['koyu', 'acik', 'mor', 'yesil'];
    temaSayac = (temaSayac + 1) % temalar.length;
    temaUygula(temalar[temaSayac]);
    mesajEkle('bot', `Tema değiştirildi: ${temalar[temaSayac]}`);
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    yukle();
    istatistikGuncelle();
    
    // API Kaydet
    document.getElementById('apiKaydet').addEventListener('click', () => {
        const key = document.getElementById('apiKey').value.trim();
        if (key) {
            durum.apiKey = key;
            localStorage.setItem('apiKey', key);
            mesajEkle('bot', 'API key kaydedildi!');
        }
    });
    
    // Model seçimi
    document.getElementById('aiModel').addEventListener('change', (e) => {
        durum.model = e.target.value;
        localStorage.setItem('model', e.target.value);
    });
    
    // Hızlı butonlar
    document.getElementById('yeniBtn').addEventListener('click', yeniBelge);
    document.getElementById('kaydetBtn').addEventListener('click', kaydet);
    document.getElementById('aktarBtn').addEventListener('click', kaydet);
    document.getElementById('temaBtn').addEventListener('click', temaDegistir);
    
    // Komut gönder
    document.getElementById('gonderBtn').addEventListener('click', komutGonder);
    
    // Enter ile gönder
    document.getElementById('komutGiris').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            e.preventDefault();
            komutGonder();
        }
    });
    
    // Canvas değişiklik izle
    document.getElementById('yaziCanvas').addEventListener('input', istatistikGuncelle);
    
    // Otomatik kaydet (her 2 dakika)
    setInterval(() => {
        const metin = document.getElementById('yaziCanvas').value;
        if (metin.trim()) {
            localStorage.setItem('otomatikYedek', metin);
        }
    }, 120000);
    
    // Otomatik yedek yükle
    const yedek = localStorage.getItem('otomatikYedek');
    if (yedek && !document.getElementById('yaziCanvas').value) {
        if (confirm('Kaydedilmiş çalışma var. Yüklensin mi?')) {
            document.getElementById('yaziCanvas').value = yedek;
            istatistikGuncelle();
        }
    }
});
