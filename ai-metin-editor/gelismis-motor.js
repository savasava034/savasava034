// Uygulama Merkezi Durum Yönetimi
const uygulamaMerkezi = {
    yapilandirma: {
        aiServis: 'openai',
        erisimKodu: null,
        dilMotoru: 'gpt-4-turbo',
        aktifTema: 'lacivert'
    },
    belge: {
        baslik: 'Başlıksız',
        icerik: '',
        kayitZamani: null
    },
    arayuz: {
        onizlemeAcik: true,
        solPanelAcik: true,
        formatPaletiGoster: true,
        splitMod: false
    },
    dosyalar: [],
    diyaloglar: [],
    gecmis: {
        geriStack: [],
        ileriStack: []
    }
};

// LocalStorage Yönetimi
const depolamaYoneticisi = {
    kaydet: (anahtar, deger) => {
        try {
            localStorage.setItem(`yazistudyo_${anahtar}`, JSON.stringify(deger));
            return true;
        } catch (hata) {
            console.error('Depolama hatası:', hata);
            return false;
        }
    },
    
    yukle: (anahtar) => {
        try {
            const deger = localStorage.getItem(`yazistudyo_${anahtar}`);
            return deger ? JSON.parse(deger) : null;
        } catch (hata) {
            console.error('Yükleme hatası:', hata);
            return null;
        }
    },
    
    sil: (anahtar) => {
        localStorage.removeItem(`yazistudyo_${anahtar}`);
    }
};

// Tema Yöneticisi
const temaYoneticisi = {
    uygula: (temaismi) => {
        document.body.setAttribute('data-tema', temaismi);
        uygulamaMerkezi.yapilandirma.aktifTema = temaismi;
        depolamaYoneticisi.kaydet('tema', temaismi);
        
        // Tüm tema kartlarını güncelle
        document.querySelectorAll('.tema-kart').forEach(kart => {
            kart.removeAttribute('data-secili');
        });
        const aktifKart = document.querySelector(`[data-tema="${temaismi}"]`);
        if (aktifKart) {
            aktifKart.setAttribute('data-secili', 'evet');
        }
    },
    
    yukle: () => {
        const kaydedilmisTema = depolamaYoneticisi.yukle('tema') || 'lacivert';
        temaYoneticisi.uygula(kaydedilmisTema);
    }
};

// Metrik Hesaplayıcı
const metrikHesapla = {
    kelimeSayisi: (metin) => {
        if (!metin || metin.trim() === '') return 0;
        return metin.trim().split(/\s+/).filter(k => k.length > 0).length;
    },
    
    karakterSayisi: (metin) => {
        return metin ? metin.length : 0;
    },
    
    satirSayisi: (metin) => {
        if (!metin) return 0;
        return metin.split('\n').length;
    },
    
    okumaSuresi: (kelimeSayisi) => {
        // Ortalama 200 kelime/dakika okuma hızı
        const dakika = Math.ceil(kelimeSayisi / 200);
        return dakika < 1 ? '< 1dk' : `${dakika}dk`;
    },
    
    guncelle: () => {
        const editor = document.getElementById('yaziTuvali');
        if (!editor) return;
        
        const metin = editor.innerText || '';
        const kelime = metrikHesapla.kelimeSayisi(metin);
        const karakter = metrikHesapla.karakterSayisi(metin);
        const satir = metrikHesapla.satirSayisi(metin);
        const okuma = metrikHesapla.okumaSuresi(kelime);
        
        document.querySelector('#kelimeMetrik .metrik-sayi').textContent = kelime;
        document.querySelector('#karakterMetrik .metrik-sayi').textContent = karakter;
        document.querySelector('#satirMetrik .metrik-sayi').textContent = satir;
        document.querySelector('#okumaSureMetrik .metrik-sayi').textContent = okuma;
        
        // Satır numaralarını güncelle
        satirNumaralariniGuncelle(satir);
        
        // Önizlemeyi güncelle
        onizlemeYoneticisi.guncelle();
    }
};

// Satır Numaraları
function satirNumaralariniGuncelle(satirSayisi) {
    const gosterge = document.getElementById('satirNumaralari');
    if (!gosterge) return;
    
    let satirHTML = '';
    for (let i = 1; i <= Math.max(satirSayisi, 50); i++) {
        satirHTML += `<div>${i}</div>`;
    }
    gosterge.innerHTML = satirHTML;
}

// Önizleme Yöneticisi
const onizlemeYoneticisi = {
    guncelle: () => {
        const editor = document.getElementById('yaziTuvali');
        const onizleme = document.getElementById('onizlemeIcerik');
        const mod = document.getElementById('onizlemeTipi')?.value || 'markdown';
        
        if (!editor || !onizleme) return;
        
        const metin = editor.innerText || '';
        
        if (mod === 'markdown') {
            try {
                const ham = marked.parse(metin);
                onizleme.innerHTML = DOMPurify.sanitize(ham);
            } catch (hata) {
                onizleme.textContent = 'Markdown işleme hatası: ' + hata.message;
            }
        } else if (mod === 'html') {
            onizleme.innerHTML = DOMPurify.sanitize(metin);
        } else {
            onizleme.textContent = metin;
        }
    },
    
    toggle: () => {
        const panel = document.getElementById('onizlemeBolgesi');
        const dugme = document.getElementById('gorselGorunumDegistir');
        
        if (!panel) return;
        
        const daraltilmis = panel.getAttribute('data-daraltilmis') === 'evet';
        panel.setAttribute('data-daraltilmis', daraltilmis ? 'hayir' : 'evet');
        dugme.setAttribute('data-aktif', daraltilmis ? 'evet' : 'hayir');
        uygulamaMerkezi.arayuz.onizlemeAcik = daraltilmis;
    }
};

// Biçim Komutları
const bicimKomutlari = {
    uygula: (komut) => {
        const secim = window.getSelection();
        const aralik = secim.rangeCount > 0 ? secim.getRangeAt(0) : null;
        
        if (!aralik) return;
        
        switch(komut) {
            case 'kalin':
                document.execCommand('bold', false, null);
                break;
            case 'egik':
                document.execCommand('italic', false, null);
                break;
            case 'alticizili':
                document.execCommand('underline', false, null);
                break;
            case 'baslik1':
                bicimKomutlari.baslikEkle('h1');
                break;
            case 'baslik2':
                bicimKomutlari.baslikEkle('h2');
                break;
            case 'baslik3':
                bicimKomutlari.baslikEkle('h3');
                break;
            case 'maddeliste':
                document.execCommand('insertUnorderedList', false, null);
                break;
            case 'sayiliste':
                document.execCommand('insertOrderedList', false, null);
                break;
            case 'alinti':
                bicimKomutlari.alintiEkle();
                break;
            case 'kod':
                bicimKomutlari.kodEkle();
                break;
            case 'baglanti':
                bicimKomutlari.baglantiEkle();
                break;
            case 'gorsel':
                bicimKomutlari.gorselEkle();
                break;
            case 'tablo':
                bicimKomutlari.tabloEkle();
                break;
            case 'geri':
                document.execCommand('undo', false, null);
                break;
            case 'ileri':
                document.execCommand('redo', false, null);
                break;
        }
        
        metrikHesapla.guncelle();
    },
    
    baslikEkle: (seviye) => {
        document.execCommand('formatBlock', false, seviye);
    },
    
    alintiEkle: () => {
        document.execCommand('formatBlock', false, 'blockquote');
    },
    
    kodEkle: () => {
        const seciliMetin = window.getSelection().toString();
        if (seciliMetin) {
            document.execCommand('insertHTML', false, `<code>${seciliMetin}</code>`);
        }
    },
    
    baglantiEkle: () => {
        const url = prompt('Bağlantı URL\'si:');
        if (url) {
            document.execCommand('createLink', false, url);
        }
    },
    
    gorselEkle: () => {
        const url = prompt('Görsel URL\'si:');
        if (url) {
            document.execCommand('insertImage', false, url);
        }
    },
    
    tabloEkle: () => {
        const satirSay = prompt('Satır sayısı:', '3');
        const sutunSay = prompt('Sütun sayısı:', '3');
        
        if (satirSay && sutunSay) {
            let tabloHTML = '<table border="1" style="border-collapse: collapse;">';
            for (let i = 0; i < parseInt(satirSay); i++) {
                tabloHTML += '<tr>';
                for (let j = 0; j < parseInt(sutunSay); j++) {
                    tabloHTML += '<td style="padding: 8px; border: 1px solid #ccc;">Hücre</td>';
                }
                tabloHTML += '</tr>';
            }
            tabloHTML += '</table>';
            document.execCommand('insertHTML', false, tabloHTML);
        }
    }
};

// Arama ve Değiştirme
const aramaMotoru = {
    suankiIndeks: -1,
    sonuclar: [],
    
    ara: (metin) => {
        const editor = document.getElementById('yaziTuvali');
        const icerik = editor.innerText;
        
        aramaMotoru.sonuclar = [];
        aramaMotoru.suankiIndeks = -1;
        
        if (!metin) return;
        
        let indeks = icerik.toLowerCase().indexOf(metin.toLowerCase());
        while (indeks !== -1) {
            aramaMotoru.sonuclar.push(indeks);
            indeks = icerik.toLowerCase().indexOf(metin.toLowerCase(), indeks + 1);
        }
        
        if (aramaMotoru.sonuclar.length > 0) {
            aramaMotoru.sonrakiniVurgula();
        }
    },
    
    sonrakiniVurgula: () => {
        if (aramaMotoru.sonuclar.length === 0) return;
        
        aramaMotoru.suankiIndeks = (aramaMotoru.suankiIndeks + 1) % aramaMotoru.sonuclar.length;
        aramaMotoru.vurgula();
    },
    
    oncekiniVurgula: () => {
        if (aramaMotoru.sonuclar.length === 0) return;
        
        aramaMotoru.suankiIndeks = aramaMotoru.suankiIndeks <= 0 
            ? aramaMotoru.sonuclar.length - 1 
            : aramaMotoru.suankiIndeks - 1;
        aramaMotoru.vurgula();
    },
    
    vurgula: () => {
        // Bu basit bir implementasyon - gerçek uygulamada daha gelişmiş olmalı
        const editor = document.getElementById('yaziTuvali');
        editor.focus();
    },
    
    degistir: (eskiMetin, yeniMetin) => {
        const editor = document.getElementById('yaziTuvali');
        let icerik = editor.innerText;
        
        if (aramaMotoru.suankiIndeks >= 0 && aramaMotoru.suankiIndeks < aramaMotoru.sonuclar.length) {
            const baslangic = aramaMotoru.sonuclar[aramaMotoru.suankiIndeks];
            icerik = icerik.substring(0, baslangic) + yeniMetin + icerik.substring(baslangic + eskiMetin.length);
            editor.innerText = icerik;
            metrikHesapla.guncelle();
        }
    },
    
    hepsiniDegistir: (eskiMetin, yeniMetin) => {
        const editor = document.getElementById('yaziTuvali');
        let icerik = editor.innerText;
        
        const regex = new RegExp(eskiMetin.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
        icerik = icerik.replace(regex, yeniMetin);
        
        editor.innerText = icerik;
        metrikHesapla.guncelle();
    }
};

// AI İletişim Yöneticisi
const aiIletisim = {
    gonder: async (komut) => {
        if (!uygulamaMerkezi.yapilandirma.erisimKodu) {
            return 'Lütfen önce API erişim kodunuzu girin ve kaydedin.';
        }
        
        const editor = document.getElementById('yaziTuvali');
        const mevcutMetin = editor.innerText || '';
        
        const sistem = `Sen gelişmiş bir Türkçe yazı editörü asistanısın. Kullanıcının metin üzerinde istediği işlemleri anla ve uygula. Mevcut metin: "${mevcutMetin.substring(0, 800)}..."`;
        
        try {
            const servis = uygulamaMerkezi.yapilandirma.aiServis;
            
            if (servis === 'openai') {
                return await aiIletisim.openaiCagri(komut, sistem);
            } else if (servis === 'anthropic') {
                return await aiIletisim.anthropicCagri(komut, sistem);
            } else if (servis === 'google') {
                return await aiIletisim.geminiCagri(komut, sistem);
            }
        } catch (hata) {
            console.error('AI iletişim hatası:', hata);
            return `Hata oluştu: ${hata.message}`;
        }
    },
    
    openaiCagri: async (komut, sistem) => {
        const yanit = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${uygulamaMerkezi.yapilandirma.erisimKodu}`
            },
            body: JSON.stringify({
                model: uygulamaMerkezi.yapilandirma.dilMotoru,
                messages: [
                    {role: 'system', content: sistem},
                    {role: 'user', content: komut}
                ],
                temperature: 0.7,
                max_tokens: 2500
            })
        });
        
        if (!yanit.ok) {
            const hata = await yanit.json();
            throw new Error(hata.error?.message || 'API isteği başarısız');
        }
        
        const veri = await yanit.json();
        return veri.choices[0].message.content;
    },
    
    anthropicCagri: async (komut, sistem) => {
        const yanit = await fetch('https://api.anthropic.com/v1/messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': uygulamaMerkezi.yapilandirma.erisimKodu,
                'anthropic-version': '2023-06-01'
            },
            body: JSON.stringify({
                model: uygulamaMerkezi.yapilandirma.dilMotoru,
                max_tokens: 2500,
                system: sistem,
                messages: [{role: 'user', content: komut}]
            })
        });
        
        if (!yanit.ok) {
            const hata = await yanit.json();
            throw new Error(hata.error?.message || 'API isteği başarısız');
        }
        
        const veri = await yanit.json();
        return veri.content[0].text;
    },
    
    geminiCagri: async (komut, sistem) => {
        const yanit = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${uygulamaMerkezi.yapilandirma.erisimKodu}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                contents: [{parts: [{text: `${sistem}\n\nKullanıcı: ${komut}`}]}]
            })
        });
        
        if (!yanit.ok) {
            const hata = await yanit.json();
            throw new Error(hata.error?.message || 'API isteği başarısız');
        }
        
        const veri = await yanit.json();
        return veri.candidates[0].content.parts[0].text;
    }
};

// Diyalog Yöneticisi
const diyalogYoneticisi = {
    ekle: (kim, mesaj) => {
        const konteyner = document.getElementById('diyalogKonteyner');
        const balon = document.createElement('div');
        balon.className = `baloncuk ${kim === 'kullanici' ? 'kullanici-baloncugu' : 'ai-baloncugu'}`;
        
        const icerik = document.createElement('div');
        icerik.className = 'baloncuk-icerik';
        
        const kimlik = document.createElement('strong');
        kimlik.className = 'konusan-kimlik';
        kimlik.textContent = kim === 'kullanici' ? 'Siz' : 'AI Asistan';
        
        const mesajGovde = document.createElement('p');
        mesajGovde.className = 'mesaj-govdesi';
        mesajGovde.textContent = mesaj;
        
        icerik.appendChild(kimlik);
        icerik.appendChild(mesajGovde);
        balon.appendChild(icerik);
        konteyner.appendChild(balon);
        
        konteyner.scrollTop = konteyner.scrollHeight;
        
        uygulamaMerkezi.diyaloglar.push({kim, mesaj, zaman: new Date()});
    },
    
    temizle: () => {
        const konteyner = document.getElementById('diyalogKonteyner');
        konteyner.innerHTML = '';
        uygulamaMerkezi.diyaloglar = [];
    }
};

// Dosya İşlemleri
const dosyaIslemleri = {
    yukle: (dosyalar) => {
        Array.from(dosyalar).forEach(dosya => {
            const okuyucu = new FileReader();
            
            okuyucu.onload = (e) => {
                uygulamaMerkezi.dosyalar.push({
                    isim: dosya.name,
                    icerik: e.target.result,
                    boyut: dosya.size,
                    tip: dosya.type,
                    zaman: new Date()
                });
                
                dosyaIslemleri.listeyiGuncelle();
            };
            
            okuyucu.readAsText(dosya);
        });
    },
    
    listeyiGuncelle: () => {
        const konteyner = document.getElementById('dosyaKonteyner');
        if (!konteyner) return;
        
        konteyner.innerHTML = uygulamaMerkezi.dosyalar.map((dosya, indeks) => 
            `<div style="padding: 6px; margin: 4px 0; background: var(--renk-zemin-ana); border-radius: 6px; font-size: 11px;">
                ✓ ${dosya.isim} (${Math.round(dosya.boyut / 1024)}KB)
            </div>`
        ).join('');
    },
    
    kaydet: () => {
        const editor = document.getElementById('yaziTuvali');
        const baslik = document.getElementById('belgeBasi').value || 'Başlıksız';
        const metin = editor.innerText;
        
        const blob = new Blob([metin], {type: 'text/plain;charset=utf-8'});
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        
        const tarih = new Date();
        const dosyaAdi = `${baslik}_${tarih.getFullYear()}${(tarih.getMonth()+1).toString().padStart(2,'0')}${tarih.getDate().toString().padStart(2,'0')}.txt`;
        
        link.href = url;
        link.download = dosyaAdi;
        link.click();
        
        URL.revokeObjectURL(url);
    },
    
    cikar: (format) => {
        const editor = document.getElementById('yaziTuvali');
        const baslik = document.getElementById('belgeBasi').value || 'Başlıksız';
        let icerik = editor.innerText;
        let mimeType = 'text/plain';
        let uzanti = 'txt';
        
        if (format === 'md') {
            uzanti = 'md';
            mimeType = 'text/markdown';
        } else if (format === 'html') {
            icerik = editor.innerHTML;
            uzanti = 'html';
            mimeType = 'text/html';
        } else if (format === 'pdf') {
            window.print();
            return;
        }
        
        const blob = new Blob([icerik], {type: mimeType + ';charset=utf-8'});
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${baslik}.${uzanti}`;
        link.click();
        URL.revokeObjectURL(url);
    }
};

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Tema yükleme
    temaYoneticisi.yukle();
    
    // Tema seçimi
    document.querySelectorAll('.tema-kart').forEach(kart => {
        kart.addEventListener('click', () => {
            const tema = kart.getAttribute('data-tema');
            temaYoneticisi.uygula(tema);
        });
    });
    
    // API Kimlik kaydetme
    document.getElementById('kimlikSakla')?.addEventListener('click', () => {
        const kod = document.getElementById('erisimKimlik').value.trim();
        if (kod) {
            uygulamaMerkezi.yapilandirma.erisimKodu = kod;
            depolamaYoneticisi.kaydet('apiKod', kod);
            diyalogYoneticisi.ekle('ai', 'API erişim kodunuz kaydedildi.');
        }
    });
    
    // Servis değiştirme
    document.getElementById('servisSaglayici')?.addEventListener('change', (e) => {
        uygulamaMerkezi.yapilandirma.aiServis = e.target.value;
        depolamaYoneticisi.kaydet('servis', e.target.value);
    });
    
    // Model değiştirme
    document.getElementById('dilMotoru')?.addEventListener('change', (e) => {
        uygulamaMerkezi.yapilandirma.dilMotoru = e.target.value;
        depolamaYoneticisi.kaydet('model', e.target.value);
    });
    
    // Dosya yükleme
    document.getElementById('dosyaYukle')?.addEventListener('change', (e) => {
        dosyaIslemleri.yukle(e.target.files);
    });
    
    // AI komut gönderme
    document.getElementById('komutGonder')?.addEventListener('click', async () => {
        const girdi = document.getElementById('kullaniciKomut');
        const komut = girdi.value.trim();
        
        if (!komut) return;
        
        diyalogYoneticisi.ekle('kullanici', komut);
        girdi.value = '';
        
        const gonderBtn = document.getElementById('komutGonder');
        gonderBtn.disabled = true;
        gonderBtn.textContent = '⏳';
        
        const yanit = await aiIletisim.gonder(komut);
        
        gonderBtn.disabled = false;
        gonderBtn.innerHTML = '<span class="gonder-oku">➤</span>';
        
        diyalogYoneticisi.ekle('ai', yanit);
    });
    
    // Ctrl+Enter ile gönderme
    document.getElementById('kullaniciKomut')?.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            document.getElementById('komutGonder').click();
        }
    });
    
    // Biçim araçları
    document.querySelectorAll('.palet-araci').forEach(arac => {
        arac.addEventListener('click', () => {
            const islem = arac.getAttribute('data-islem');
            bicimKomutlari.uygula(islem);
        });
    });
    
    // Editor değişiklik izleme
    const editor = document.getElementById('yaziTuvali');
    if (editor) {
        let guncellemeZamanlayici;
        editor.addEventListener('input', () => {
            clearTimeout(guncellemeZamanlayici);
            guncellemeZamanlayici = setTimeout(() => {
                metrikHesapla.guncelle();
            }, 300);
        });
    }
    
    // Önizleme toggle
    document.getElementById('gorselGorunumDegistir')?.addEventListener('click', () => {
        onizlemeYoneticisi.toggle();
    });
    
    // Önizleme tipi değiştirme
    document.getElementById('onizlemeTipi')?.addEventListener('change', () => {
        onizlemeYoneticisi.guncelle();
    });
    
    // Belge işlemleri
    document.getElementById('belgeSakla')?.addEventListener('click', () => {
        dosyaIslemleri.kaydet();
    });
    
    document.getElementById('yeniBelge')?.addEventListener('click', () => {
        if (confirm('Yeni belge oluşturulacak. Devam edilsin mi?')) {
            document.getElementById('yaziTuvali').innerText = '';
            document.getElementById('belgeBasi').value = 'Başlıksız';
            metrikHesapla.guncelle();
        }
    });
    
    // Dışarı çıkarma
    document.querySelectorAll('.menu-oge').forEach(oge => {
        oge.addEventListener('click', () => {
            const format = oge.getAttribute('data-tip');
            dosyaIslemleri.cikar(format);
        });
    });
    
    // Yazdırma
    document.getElementById('yaziciyaGonder')?.addEventListener('click', () => {
        window.print();
    });
    
    // Arama
    document.getElementById('aramaAc')?.addEventListener('click', () => {
        const aramaCubuk = document.getElementById('aramaCubugu');
        if (aramaCubuk) {
            aramaCubuk.style.display = aramaCubuk.style.display === 'none' ? 'flex' : 'none';
        }
    });
    
    document.getElementById('aramaKapat')?.addEventListener('click', () => {
        document.getElementById('aramaCubugu').style.display = 'none';
    });
    
    document.getElementById('sonrakiBul')?.addEventListener('click', () => {
        const aramaMetni = document.getElementById('aramaMetni').value;
        aramaMotoru.ara(aramaMetni);
        aramaMotoru.sonrakiniVurgula();
    });
    
    document.getElementById('oncekiBul')?.addEventListener('click', () => {
        aramaMotoru.oncekiniVurgula();
    });
    
    document.getElementById('tekDegistir')?.addEventListener('click', () => {
        const eskiMetin = document.getElementById('aramaMetni').value;
        const yeniMetin = document.getElementById('degistirMetni').value;
        aramaMotoru.degistir(eskiMetin, yeniMetin);
    });
    
    document.getElementById('tumDegistir')?.addEventListener('click', () => {
        const eskiMetin = document.getElementById('aramaMetni').value;
        const yeniMetin = document.getElementById('degistirMetni').value;
        aramaMotoru.hepsiniDegistir(eskiMetin, yeniMetin);
    });
    
    // Drag & Drop
    const konteyner = document.getElementById('uygulamaKonteyneri');
    const katman = document.getElementById('dosyaSurukleKatman');
    
    konteyner.addEventListener('dragover', (e) => {
        e.preventDefault();
        katman.setAttribute('data-aktif', 'evet');
    });
    
    konteyner.addEventListener('dragleave', (e) => {
        if (e.target === konteyner) {
            katman.setAttribute('data-aktif', 'hayir');
        }
    });
    
    konteyner.addEventListener('drop', (e) => {
        e.preventDefault();
        katman.setAttribute('data-aktif', 'hayir');
        
        if (e.dataTransfer.files.length > 0) {
            dosyaIslemleri.yukle(e.dataTransfer.files);
        }
    });
    
    // İlk yükleme
    metrikHesapla.guncelle();
    
    // Kaydedilmiş verileri yükle
    const kaydedilenKod = depolamaYoneticisi.yukle('apiKod');
    if (kaydedilenKod) {
        uygulamaMerkezi.yapilandirma.erisimKodu = kaydedilenKod;
        document.getElementById('erisimKimlik').value = kaydedilenKod;
    }
    
    const kaydedilenServis = depolamaYoneticisi.yukle('servis');
    if (kaydedilenServis) {
        uygulamaMerkezi.yapilandirma.aiServis = kaydedilenServis;
        document.getElementById('servisSaglayici').value = kaydedilenServis;
    }
    
    const kaydedilenModel = depolamaYoneticisi.yukle('model');
    if (kaydedilenModel) {
        uygulamaMerkezi.yapilandirma.dilMotoru = kaydedilenModel;
        document.getElementById('dilMotoru').value = kaydedilenModel;
    }
});

// Otomatik kaydetme (her 2 dakikada)
setInterval(() => {
    const editor = document.getElementById('yaziTuvali');
    if (editor && editor.innerText.trim()) {
        depolamaYoneticisi.kaydet('otomatikYedek', {
            icerik: editor.innerText,
            baslik: document.getElementById('belgeBasi').value,
            zaman: new Date()
        });
    }
}, 120000);

// Sayfa yüklendiğinde otomatik yedek kontrolü
window.addEventListener('load', () => {
    const yedek = depolamaYoneticisi.yukle('otomatikYedek');
    if (yedek && yedek.icerik) {
        const editor = document.getElementById('yaziTuvali');
        if (editor.innerText.trim() === '') {
            const yukle = confirm('Kaydedilmiş bir çalışma bulundu. Yüklemek ister misiniz?');
            if (yukle) {
                editor.innerText = yedek.icerik;
                document.getElementById('belgeBasi').value = yedek.baslik || 'Başlıksız';
                metrikHesapla.guncelle();
                diyalogYoneticisi.ekle('ai', 'Önceki çalışmanız geri yüklendi.');
            }
        }
    }
});
