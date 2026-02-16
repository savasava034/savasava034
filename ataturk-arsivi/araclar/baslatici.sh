#!/bin/bash
# Atatürk Arşiv Sistemi - Basit Başlatıcı

echo "🇹🇷 ATATÜRK ARŞİV SİSTEMİ - BAŞLATICI"
echo "======================================"
echo ""

# Mevcut dizini kontrol et
if [ ! -f "interaktif_arayuz.py" ]; then
    echo "⚠️  Dikkat: interaktif_arayuz.py bulunamadı!"
    echo ""
    echo "Lütfen şu klasördeyken çalıştırın:"
    echo "  ataturk-arsivi/araclar/"
    echo ""
    echo "Örnek:"
    echo "  cd ataturk-arsivi/araclar"
    echo "  ./baslatici.sh"
    exit 1
fi

# Python kontrolü
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 bulunamadı!"
    echo ""
    echo "Lütfen Python 3'ü yükleyin:"
    echo "  - Windows: https://www.python.org/downloads/"
    echo "  - macOS: brew install python3"
    echo "  - Linux: sudo apt install python3"
    exit 1
fi

echo "✅ Python bulundu: $(python3 --version)"
echo ""

# Menü göster
echo "Ne yapmak istersiniz?"
echo ""
echo "1. 📥 Örnek verileri yükle (20+ Atatürk sözü)"
echo "2. 🖥️  İnteraktif menüyü başlat"
echo "3. ℹ️  Sistem bilgisi göster"
echo "0. ❌ Çıkış"
echo ""
read -p "Seçiminiz (1-3): " choice

case $choice in
    1)
        echo ""
        echo "📥 Örnek veriler yükleniyor..."
        echo ""
        python3 ornek_veri_yukle.py
        echo ""
        echo "✅ İşlem tamamlandı!"
        echo ""
        read -p "İnteraktif menüyü başlatmak ister misiniz? (e/h): " yn
        if [ "$yn" = "e" ] || [ "$yn" = "E" ]; then
            python3 interaktif_arayuz.py
        fi
        ;;
    2)
        echo ""
        echo "🖥️  İnteraktif menü başlatılıyor..."
        echo ""
        python3 interaktif_arayuz.py
        ;;
    3)
        echo ""
        echo "ℹ️  Sistem Bilgisi"
        echo "=================="
        echo "Python: $(python3 --version)"
        echo "Klasör: $(pwd)"
        echo ""
        if [ -f "veriler/sozler.json" ]; then
            echo "✅ Veri dosyası mevcut"
            # JSON'dan kayıt sayısını al (basit yöntem)
            record_count=$(python3 -c "import json; f=open('veriler/sozler.json'); d=json.load(f); print(len(d.get('sozler', [])))" 2>/dev/null || echo "0")
            echo "📊 Kayıtlı söz sayısı: $record_count"
        else
            echo "⚠️  Veri dosyası henüz oluşturulmamış"
            echo "💡 Örnek verileri yüklemek için seçenek 1'i kullanın"
        fi
        ;;
    0)
        echo ""
        echo "👋 Görüşürüz!"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Geçersiz seçim!"
        exit 1
        ;;
esac

echo ""
echo "👋 Program sonlandı."
