#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
İnteraktif Arşiv Arayüzü
========================
Komut satırından arşivi yönetmek için kullanıcı dostu arayüz.
"""

import sys
import os

# Modülü import edebilmek için path'e ekle
sys.path.insert(0, os.path.dirname(__file__))

from arsiv_yoneticisi import AtaturkArsivi


def menu_goster():
    """Ana menüyü gösterir."""
    print("\n" + "=" * 70)
    print("🇹🇷  ATATÜRK ARŞİVİ YÖNETİM SİSTEMİ")
    print("=" * 70)
    print("\n📋 Menü:")
    print("  1. 📝 Yeni söz ekle")
    print("  2. 🔍 Arşivde ara")
    print("  3. 📊 İstatistikleri görüntüle")
    print("  4. 📖 Tüm sözleri listele")
    print("  5. 🏷️  Kategoriye göre listele")
    print("  6. 💾 Dışa aktar (JSON/TXT/MD)")
    print("  7. 📥 Örnek verileri yükle")
    print("  0. 🚪 Çıkış")
    print("=" * 70)


def yeni_soz_ekle(arsiv: AtaturkArsivi):
    """Kullanıcıdan yeni söz bilgilerini alır ve ekler."""
    print("\n📝 Yeni Söz Ekleme")
    print("-" * 70)
    
    metin = input("💬 Söz/Cümle/Paragraf: ").strip()
    if not metin:
        print("❌ Söz boş olamaz!")
        return
    
    # Kategoriler
    print("\n🏷️  Kategoriler (virgülle ayırın):")
    print("   Örnekler: Eğitim, Bilim, Cumhuriyet, Kadın Hakları, vb.")
    kategori_str = input("Kategoriler: ").strip()
    kategoriler = [k.strip() for k in kategori_str.split(",")] if kategori_str else []
    
    # Tarih
    tarih = input("📅 Tarih (YYYY-MM-DD formatında, boş bırakılabilir): ").strip() or None
    
    # Kaynak
    kaynak = input("📚 Kaynak (kitap, konuşma adı, boş bırakılabilir): ").strip() or None
    
    # Yer
    yer = input("📍 Yer (söylendiği/yazıldığı yer, boş bırakılabilir): ").strip() or None
    
    # Notlar
    notlar = input("📌 Notlar (ek bilgiler, boş bırakılabilir): ").strip() or None
    
    # Ekleme işlemi
    print("\n🔄 Ekleniyor...")
    basarili = arsiv.soz_ekle(
        metin=metin,
        kategori=kategoriler,
        tarih=tarih,
        kaynak=kaynak,
        yer=yer,
        notlar=notlar
    )
    
    if basarili:
        print("✨ Söz başarıyla arşive eklendi!")
    else:
        print("⚠️  Bu söz zaten arşivde mevcut (tekrarlı kayıt).")


def arama_yap(arsiv: AtaturkArsivi):
    """Arşivde arama yapar."""
    print("\n🔍 Arşivde Arama")
    print("-" * 70)
    print("Arama kriterleri (boş bırakılabilir):")
    
    anahtar = input("🔎 Anahtar kelime: ").strip() or None
    kategori = input("🏷️  Kategori: ").strip() or None
    tarih = input("📅 Tarih: ").strip() or None
    kaynak = input("📚 Kaynak: ").strip() or None
    
    sonuclar = arsiv.ara(
        anahtar_kelime=anahtar,
        kategori=kategori,
        tarih=tarih,
        kaynak=kaynak
    )
    
    if not sonuclar:
        print("\n❌ Arama kriterlerinize uygun sonuç bulunamadı.")
        return
    
    print(f"\n✅ {len(sonuclar)} sonuç bulundu:")
    for soz in sonuclar:
        arsiv.yazdir_soz(soz)
    
    print(f"\n📊 Toplam {len(sonuclar)} sonuç gösteriliyor.")


def istatistik_goster(arsiv: AtaturkArsivi):
    """Arşiv istatistiklerini gösterir."""
    print("\n📊 Arşiv İstatistikleri")
    print("-" * 70)
    
    istat = arsiv.istatistikler()
    
    if istat['toplam_kayit'] == 0:
        print("❌ Arşivde henüz kayıt yok.")
        print("💡 Menüden '7. Örnek verileri yükle' seçeneğini kullanabilirsiniz.")
        return
    
    print(f"📈 Genel İstatistikler:")
    print(f"   • Toplam Kayıt: {istat['toplam_kayit']}")
    print(f"   • Toplam Kelime: {istat['toplam_kelime']:,}")
    print(f"   • Ortalama Kelime/Söz: {istat['ortalama_kelime']}")
    
    print(f"\n📏 En Uzun Söz:")
    print(f"   • ID: {istat['en_uzun_soz']['id']}")
    print(f"   • Kelime Sayısı: {istat['en_uzun_soz']['kelime_sayisi']}")
    print(f"   • \"{istat['en_uzun_soz']['metin'][:100]}...\"")
    
    print(f"\n📏 En Kısa Söz:")
    print(f"   • ID: {istat['en_kisa_soz']['id']}")
    print(f"   • Kelime Sayısı: {istat['en_kisa_soz']['kelime_sayisi']}")
    print(f"   • \"{istat['en_kisa_soz']['metin']}\"")
    
    if istat['kategori_dagilimi']:
        print(f"\n🏷️  Kategori Dağılımı:")
        for kat, sayi in sorted(istat['kategori_dagilimi'].items(), key=lambda x: x[1], reverse=True):
            print(f"   • {kat}: {sayi} söz")


def tum_sozleri_listele(arsiv: AtaturkArsivi):
    """Tüm sözleri listeler."""
    sozler = arsiv.veriler["sozler"]
    
    if not sozler:
        print("\n❌ Arşivde henüz kayıt yok.")
        return
    
    print(f"\n📖 Tüm Sözler (Toplam: {len(sozler)})")
    print("=" * 70)
    
    for soz in sozler:
        arsiv.yazdir_soz(soz)
    
    print(f"\n📊 Toplam {len(sozler)} söz gösteriliyor.")


def kategoriye_gore_listele(arsiv: AtaturkArsivi):
    """Belirli bir kategorideki sözleri listeler."""
    istat = arsiv.istatistikler()
    
    if not istat['kategori_dagilimi']:
        print("\n❌ Arşivde henüz kategorilendirilmiş söz yok.")
        return
    
    print("\n🏷️  Mevcut Kategoriler:")
    print("-" * 70)
    kategoriler = sorted(istat['kategori_dagilimi'].items(), key=lambda x: x[1], reverse=True)
    
    for i, (kat, sayi) in enumerate(kategoriler, 1):
        print(f"  {i}. {kat} ({sayi} söz)")
    
    secim = input(f"\nKategori seçin (1-{len(kategoriler)}): ").strip()
    
    try:
        idx = int(secim) - 1
        if 0 <= idx < len(kategoriler):
            secilen_kategori = kategoriler[idx][0]
            sonuclar = arsiv.ara(kategori=secilen_kategori)
            
            print(f"\n📖 '{secilen_kategori}' kategorisindeki sözler:")
            print("=" * 70)
            
            for soz in sonuclar:
                arsiv.yazdir_soz(soz)
            
            print(f"\n📊 Toplam {len(sonuclar)} söz gösteriliyor.")
        else:
            print("❌ Geçersiz seçim!")
    except ValueError:
        print("❌ Geçersiz giriş!")


def disa_aktar(arsiv: AtaturkArsivi):
    """Arşivi dışa aktarır."""
    print("\n💾 Dışa Aktarma")
    print("-" * 70)
    print("Format seçin:")
    print("  1. JSON (yapılandırılmış veri)")
    print("  2. TXT (düz metin)")
    print("  3. MD (Markdown)")
    
    secim = input("\nSeçiminiz (1-3): ").strip()
    
    format_map = {
        "1": ("json", "ataturk_arsivi.json"),
        "2": ("txt", "ataturk_arsivi.txt"),
        "3": ("md", "ataturk_arsivi.md")
    }
    
    if secim not in format_map:
        print("❌ Geçersiz seçim!")
        return
    
    format_tipi, varsayilan_dosya = format_map[secim]
    
    dosya_adi = input(f"Dosya adı [{varsayilan_dosya}]: ").strip() or varsayilan_dosya
    
    try:
        # Dışa aktarma dizinini oluştur
        export_dir = "../../ataturk-arsivi-disa-aktarma"
        os.makedirs(export_dir, exist_ok=True)
        
        tam_yol = os.path.join(export_dir, dosya_adi)
        arsiv.disa_aktar(tam_yol, format=format_tipi)
        
        print(f"\n✅ Arşiv başarıyla '{tam_yol}' dosyasına aktarıldı!")
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")


def ornek_veri_yukle(arsiv: AtaturkArsivi):
    """Örnek verileri yükler."""
    print("\n📥 Örnek Veri Yükleme")
    print("-" * 70)
    print("⚠️  Bu işlem örnek Atatürk sözlerini arşive ekleyecektir.")
    print("   (Zaten mevcut olan sözler atlanacaktır)")
    
    onay = input("\nDevam etmek istiyor musunuz? (e/h): ").strip().lower()
    
    if onay != 'e':
        print("❌ İşlem iptal edildi.")
        return
    
    # Örnek veri yükleme scriptini çalıştır
    try:
        from ornek_veri_yukle import ornek_veriler_yukle
        ornek_veriler_yukle()
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")


def main():
    """Ana program döngüsü."""
    arsiv = AtaturkArsivi("veriler/sozler.json")
    
    while True:
        menu_goster()
        secim = input("\n👉 Seçiminiz: ").strip()
        
        if secim == "1":
            yeni_soz_ekle(arsiv)
        elif secim == "2":
            arama_yap(arsiv)
        elif secim == "3":
            istatistik_goster(arsiv)
        elif secim == "4":
            tum_sozleri_listele(arsiv)
        elif secim == "5":
            kategoriye_gore_listele(arsiv)
        elif secim == "6":
            disa_aktar(arsiv)
        elif secim == "7":
            ornek_veri_yukle(arsiv)
        elif secim == "0":
            print("\n👋 Atatürk Arşivi Yönetim Sisteminden çıkılıyor...")
            print("🇹🇷  Güle güle!\n")
            break
        else:
            print("\n❌ Geçersiz seçim! Lütfen 0-7 arasında bir sayı girin.")
        
        input("\n⏸️  Devam etmek için Enter'a basın...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program kullanıcı tarafından sonlandırıldı. Güle güle!")
        sys.exit(0)
