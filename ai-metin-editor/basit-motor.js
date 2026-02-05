// Basit Motor - OpenCanvas Tarzı

// Durum
const durum = {
    apiKey: null,
    apiProvider: 'openai',
    model: 'gpt-4-turbo',
    tema: 'koyu',
    ayarlar: {
        fontBoyut: 16,
        satirYukseklik: 1.8,
        canvasGenislik: '800px',
        yaziTipi: 'Georgia, serif',
        otomatikKayit: 120,
        aiSicaklik: 0.7,
        kelimeHedef: 0
    }
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
    const satirlar = metin.split('\n').length;
    const kelimeSayisi = kelimeler.length;
    const okumaDk = Math.ceil(kelimeSayisi / 200);
    
    document.getElementById('kelimeSayisi').textContent = `${kelimeSayisi} kelime`;
    document.getElementById('karakterSayisi').textContent = `${metin.length} karakter`;
    document.getElementById('satirSayisi').textContent = `${satirlar} satır`;
    document.getElementById('okumaSure').textContent = `${okumaDk}dk okuma`;
    
    // Hedef gösterge
    if (durum.ayarlar.kelimeHedef > 0) {
        const yuzde = Math.min((kelimeSayisi / durum.ayarlar.kelimeHedef) * 100, 100);
        document.getElementById('hedefGrup').style.display = 'flex';
        document.getElementById('hedefProgress').style.width = `${yuzde}%`;
        document.getElementById('hedefYuzde').textContent = `${Math.round(yuzde)}%`;
    } else {
        document.getElementById('hedefGrup').style.display = 'none';
    }
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
    ayarlariYukle();
    istatistikGuncelle();
    
    // Klavye kısayolları
    document.addEventListener('keydown', klavyeKisayollari);
    
    // API Kaydet
    document.getElementById('apiKaydet').addEventListener('click', () => {
        const key = document.getElementById('apiKey').value.trim();
        const provider = document.getElementById('aiSagla').value;
        if (key) {
            durum.apiKey = key;
            durum.apiProvider = provider;
            localStorage.setItem('apiKey', key);
            localStorage.setItem('apiProvider', provider);
            mesajEkle('bot', 'API key kaydedildi!');
        }
    });
    
    // Model seçimi
    document.getElementById('aiModel').addEventListener('change', (e) => {
        durum.model = e.target.value;
        localStorage.setItem('model', e.target.value);
    });
    
    // Provider seçimi
    document.getElementById('aiSagla').addEventListener('change', (e) => {
        durum.apiProvider = e.target.value;
        localStorage.setItem('apiProvider', e.target.value);
    });
    
    // Hızlı butonlar
    document.getElementById('yeniBtn').addEventListener('click', yeniBelge);
    document.getElementById('kaydetBtn').addEventListener('click', kaydet);
    document.getElementById('aktarBtn').addEventListener('click', kaydet);
    document.getElementById('temaBtn').addEventListener('click', temaDegistir);
    
    // Ayarlar butonu
    document.getElementById('ayarBtn').addEventListener('click', () => {
        const panel = document.getElementById('ayarlarPanel');
        panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    });
    
    // Ayarlar kapat
    document.getElementById('ayarKapat').addEventListener('click', () => {
        document.getElementById('ayarlarPanel').style.display = 'none';
    });
    
    // Kısayollar butonu
    document.getElementById('kisayolBtn').addEventListener('click', () => {
        document.getElementById('kisayolModal').style.display = 'flex';
    });
    
    // Kısayollar kapat
    document.getElementById('kisayolKapat').addEventListener('click', () => {
        document.getElementById('kisayolModal').style.display = 'none';
    });
    
    // Modal dışına tıklayınca kapat
    document.getElementById('kisayolModal').addEventListener('click', (e) => {
        if (e.target.id === 'kisayolModal') {
            e.target.style.display = 'none';
        }
    });
    
    // Ayar değişiklikleri
    document.getElementById('fontBoyut').addEventListener('input', (e) => {
        durum.ayarlar.fontBoyut = parseInt(e.target.value);
        ayarlariUygula();
        ayarlariKaydet();
    });
    
    document.getElementById('satirYukseklik').addEventListener('input', (e) => {
        durum.ayarlar.satirYukseklik = parseFloat(e.target.value);
        ayarlariUygula();
        ayarlariKaydet();
    });
    
    document.getElementById('canvasGenislik').addEventListener('change', (e) => {
        durum.ayarlar.canvasGenislik = e.target.value;
        ayarlariUygula();
        ayarlariKaydet();
    });
    
    document.getElementById('yaziTipi').addEventListener('change', (e) => {
        durum.ayarlar.yaziTipi = e.target.value;
        ayarlariUygula();
        ayarlariKaydet();
    });
    
    document.getElementById('otomatikKayit').addEventListener('change', (e) => {
        durum.ayarlar.otomatikKayit = parseInt(e.target.value);
        ayarlariKaydet();
        // Otomatik kayıt zamanlayıcısını yeniden başlat
        clearInterval(window.otomatikKayitInterval);
        window.otomatikKayitInterval = setInterval(() => {
            const metin = document.getElementById('yaziCanvas').value;
            if (metin.trim()) {
                localStorage.setItem('otomatikYedek', metin);
            }
        }, durum.ayarlar.otomatikKayit * 1000);
    });
    
    document.getElementById('aiSicaklik').addEventListener('input', (e) => {
        durum.ayarlar.aiSicaklik = parseFloat(e.target.value);
        ayarlariUygula();
        ayarlariKaydet();
    });
    
    document.getElementById('kelimeHedef').addEventListener('change', (e) => {
        durum.ayarlar.kelimeHedef = parseInt(e.target.value) || 0;
        ayarlariKaydet();
        istatistikGuncelle();
    });
    
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
    
    // Otomatik kaydet
    window.otomatikKayitInterval = setInterval(() => {
        const metin = document.getElementById('yaziCanvas').value;
        if (metin.trim()) {
            localStorage.setItem('otomatikYedek', metin);
        }
    }, durum.ayarlar.otomatikKayit * 1000);
    
    // Otomatik yedek yükle
    const yedek = localStorage.getItem('otomatikYedek');
    if (yedek && !document.getElementById('yaziCanvas').value) {
        if (confirm('Kaydedilmiş çalışma var. Yüklensin mi?')) {
            document.getElementById('yaziCanvas').value = yedek;
            istatistikGuncelle();
        }
    }
    
    // Provider yükle
    const provider = localStorage.getItem('apiProvider');
    if (provider) {
        durum.apiProvider = provider;
        document.getElementById('aiSagla').value = provider;
    }
});

// Ayarları uygula
function ayarlariUygula() {
    const canvas = document.getElementById('yaziCanvas');
    canvas.style.fontSize = durum.ayarlar.fontBoyut + 'px';
    canvas.style.lineHeight = durum.ayarlar.satirYukseklik;
    canvas.style.fontFamily = durum.ayarlar.yaziTipi;
    canvas.style.maxWidth = durum.ayarlar.canvasGenislik;
    
    // Değerleri göster
    document.getElementById('fontBoyutDeger').textContent = durum.ayarlar.fontBoyut + 'px';
    document.getElementById('satirYukseklikDeger').textContent = durum.ayarlar.satirYukseklik;
    document.getElementById('aiSicaklikDeger').textContent = durum.ayarlar.aiSicaklik;
}

// Ayarları kaydet
function ayarlariKaydet() {
    localStorage.setItem('ayarlar', JSON.stringify(durum.ayarlar));
}

// Ayarları yükle
function ayarlariYukle() {
    const kayitli = localStorage.getItem('ayarlar');
    if (kayitli) {
        durum.ayarlar = {...durum.ayarlar, ...JSON.parse(kayitli)};
        
        // Form elemanlarını güncelle
        document.getElementById('fontBoyut').value = durum.ayarlar.fontBoyut;
        document.getElementById('satirYukseklik').value = durum.ayarlar.satirYukseklik;
        document.getElementById('canvasGenislik').value = durum.ayarlar.canvasGenislik;
        document.getElementById('yaziTipi').value = durum.ayarlar.yaziTipi;
        document.getElementById('otomatikKayit').value = durum.ayarlar.otomatikKayit;
        document.getElementById('aiSicaklik').value = durum.ayarlar.aiSicaklik;
        document.getElementById('kelimeHedef').value = durum.ayarlar.kelimeHedef;
        
        ayarlariUygula();
    }
}

// Klavye kısayolları
function klavyeKisayollari(e) {
    // Ctrl+N - Yeni belge
    if (e.ctrlKey && e.key === 'n') {
        e.preventDefault();
        yeniBelge();
    }
    // Ctrl+S - Kaydet
    else if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        kaydet();
    }
    // Ctrl+/ - Kısayollar
    else if (e.ctrlKey && e.key === '/') {
        e.preventDefault();
        document.getElementById('kisayolModal').style.display = 'flex';
    }
    // Alt+T - Tema
    else if (e.altKey && e.key === 't') {
        e.preventDefault();
        temaDegistir();
    }
    // Alt+A - Ayarlar
    else if (e.altKey && e.key === 'a') {
        e.preventDefault();
        const panel = document.getElementById('ayarlarPanel');
        panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    }
}

// Gelişmiş AI çağrısı
async function aiCagir(komut) {
    if (!durum.apiKey) {
        return 'Lütfen API key girin ve kaydedin.';
    }
    
    const metin = document.getElementById('yaziCanvas').value;
    const sistem = `Sen bir yazı asistanısın. Kullanıcının isteklerini yerine getir. Uzun metinler yazabilirsin (100+ sayfa). Mevcut metin: "${metin.substring(0, 800)}..."`;
    
    try {
        if (durum.apiProvider === 'openai') {
            return await openaiCagri(komut, sistem);
        } else if (durum.apiProvider === 'anthropic') {
            return await anthropicCagri(komut, sistem);
        } else if (durum.apiProvider === 'google') {
            return await geminiCagri(komut, sistem);
        }
    } catch (hata) {
        console.error('Hata:', hata);
        return `Hata: ${hata.message}`;
    }
}

async function openaiCagri(komut, sistem) {
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
            temperature: durum.ayarlar.aiSicaklik
        })
    });
    
    if (!yanit.ok) {
        const hata = await yanit.json();
        throw new Error(hata.error?.message || 'API hatası');
    }
    
    const veri = await yanit.json();
    return veri.choices[0].message.content;
}

async function anthropicCagri(komut, sistem) {
    const yanit = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-api-key': durum.apiKey,
            'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
            model: durum.model,
            max_tokens: 4000,
            temperature: durum.ayarlar.aiSicaklik,
            system: sistem,
            messages: [{role: 'user', content: komut}]
        })
    });
    
    if (!yanit.ok) {
        const hata = await yanit.json();
        throw new Error(hata.error?.message || 'API hatası');
    }
    
    const veri = await yanit.json();
    return veri.content[0].text;
}

async function geminiCagri(komut, sistem) {
    const yanit = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${durum.apiKey}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            contents: [{parts: [{text: `${sistem}\n\nKullanıcı: ${komut}`}]}],
            generationConfig: {
                temperature: durum.ayarlar.aiSicaklik,
                maxOutputTokens: 4000
            }
        })
    });
    
    if (!yanit.ok) {
        const hata = await yanit.json();
        throw new Error(hata.error?.message || 'API hatası');
    }
    
    const veri = await yanit.json();
    return veri.candidates[0].content.parts[0].text;
}

// Export işlemleri
function exportMarkdown() {
    const metin = document.getElementById('yaziCanvas').value;
    const blob = new Blob([metin], {type: 'text/markdown;charset=utf-8'});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    
    const tarih = new Date();
    const dosyaAdi = `belge_${tarih.getFullYear()}${(tarih.getMonth()+1).toString().padStart(2,'0')}${tarih.getDate().toString().padStart(2,'0')}.md`;
    
    link.href = url;
    link.download = dosyaAdi;
    link.click();
    
    URL.revokeObjectURL(url);
    mesajEkle('bot', 'Markdown olarak kaydedildi!');
}

