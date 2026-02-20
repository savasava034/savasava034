#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Örnek Veri Yükleyici
====================
Atatürk'ün bazı ünlü sözlerini arşive yükler.
"""

import sys
import os

# Modülü import edebilmek için path'e ekle
sys.path.insert(0, os.path.dirname(__file__))

from arsiv_yoneticisi import AtaturkArsivi


def ornek_veriler_yukle():
    """Örnek Atatürk sözlerini arşive yükler."""
    
    arsiv = AtaturkArsivi()
    
    # Atatürk'ün ünlü sözleri
    ornek_sozler = [
        {
            "metin": "Hayatta en hakiki mürşit ilimdir, fendir.",
            "kategori": ["Bilim", "Eğitim"],
            "kaynak": "Samsun'da Öğretmenlerle Konuşma",
            "tarih": "1924-09-22",
            "notlar": "En bilinen sözlerinden biri"
        },
        {
            "metin": "Egemenlik kayıtsız şartsız milletindir.",
            "kategori": ["Cumhuriyet", "Demokrasi"],
            "kaynak": "TBMM Açılış Konuşması",
            "tarih": "1920-04-23",
            "notlar": "Cumhuriyet'in temel prensibi"
        },
        {
            "metin": "Muhtaç olduğumuz kudret, damarlarımızdaki asil kanda mevcuttur.",
            "kategori": ["Milli Mücadele", "Vatan"],
            "kaynak": "Nutuk",
            "tarih": "1927",
            "notlar": "Nutuk'tan alıntı"
        },
        {
            "metin": "Benim naçiz vücudum elbet bir gün toprak olacaktır, ancak Türkiye Cumhuriyeti ilelebet payidar kalacaktır.",
            "kategori": ["Cumhuriyet", "Vatan"],
            "kaynak": "Gençliğe Hitabe",
            "tarih": "1927",
            "notlar": "Ölümsüz vasiyet"
        },
        {
            "metin": "Ey Türk gençliği! Birinci vazifen, Türk istiklalini, Türk Cumhuriyetini, ilelebet muhafaza ve müdafaa etmektir.",
            "kategori": ["Gençlik", "Cumhuriyet", "Vatan"],
            "kaynak": "Gençliğe Hitabe",
            "tarih": "1927",
            "notlar": "Gençliğe emanet"
        },
        {
            "metin": "Bir milletin varlık ve bağımsızlığı ancak kültür varlığı ve bağımsızlığı ile korunur.",
            "kategori": ["Kültür", "Bağımsızlık"],
            "kaynak": "Türk Tarih Kurumu Açılış Konuşması",
            "tarih": "1931-09-01"
        },
        {
            "metin": "Yurtta sulh, cihanda sulh.",
            "kategori": ["Barış", "Dış Politika"],
            "kaynak": "10. Yıl Nutku",
            "tarih": "1933-10-29",
            "notlar": "Türk dış politikasının temeli"
        },
        {
            "metin": "Türk kadını, daha fazla ileriye, daha fazla yükselmeye hak kazanmış olduğunu anlamalıdır.",
            "kategori": ["Kadın Hakları", "Çağdaşlaşma"],
            "kaynak": "Türk Kadın Birliği'ne Konuşma",
            "tarih": "1923"
        },
        {
            "metin": "Eğitim ateştir, ithal edilmez. Kendi içinizde çakmak gerekir.",
            "kategori": ["Eğitim"],
            "kaynak": "Öğretmenlerle Söyleşi"
        },
        {
            "metin": "Millet, maarif ordusu denilen öğretmenlerin fedakarlığı sayesinde cehaletin karanlıklarından aydınlığa doğru yol alacaktır.",
            "kategori": ["Eğitim", "Öğretmen"],
            "kaynak": "Öğretmenler Kongresi",
            "tarih": "1925-08-25"
        },
        {
            "metin": "Hayat demek mücadele demektir. Hayatta başarılı olmak, mücadelede başarılı olmak demektir.",
            "kategori": ["Yaşam Felsefesi", "Mücadele"],
            "kaynak": "Gençlerle Söyleşi"
        },
        {
            "metin": "Ordular! İlk hedefiniz Akdeniz'dir. İleri!",
            "kategori": ["Milli Mücadele", "Komutanlık"],
            "kaynak": "Büyük Taarruz Emri",
            "tarih": "1922-08-26",
            "yer": "Afyonkarahisar"
        },
        {
            "metin": "Ben Türk evladının yapamayacağı iş yoktur diye düşünüyorum.",
            "kategori": ["Özgüven", "Gençlik"],
            "kaynak": "Gençlerle Konuşma"
        },
        {
            "metin": "Bir ulusun gerçek kurtarıcıları, yalnız ve ancak öğretmenlerdir.",
            "kategori": ["Eğitim", "Öğretmen"],
            "kaynak": "Öğretmenler Günü Konuşması",
            "tarih": "1922-11-24"
        },
        {
            "metin": "Dünyada her şey için, medeniyet için, hayat için, muvaffakiyet için en hakiki mürşit ilimdir, fendir.",
            "kategori": ["Bilim", "Çağdaşlaşma", "Eğitim"],
            "kaynak": "Samsun'da Öğretmenlerle Konuşma",
            "tarih": "1924-09-22",
            "notlar": "Ünlü sözün tam hali"
        },
        {
            "metin": "Cumhuriyet, karakteri, kuvvetli, kudretli olduğu kadar merhametli ve muhterem insanlar ister.",
            "kategori": ["Cumhuriyet", "Karakter"],
            "kaynak": "TBMM Açılış Konuşması"
        },
        {
            "metin": "Gerçek güzellik, güzelliğin esaslı olanıdır. Cehalete dayanan güzellik göz boyayan bir maskeden başka bir şey değildir.",
            "kategori": ["Eğitim", "Kadın"],
            "kaynak": "İzmir'de Konuşma"
        },
        {
            "metin": "İnsanlık aleminde yükselmenin tek yolu da medeniyet yolunda yürümektir. Medeniyet yolunda yürümek bir milletin hayatı için esastır.",
            "kategori": ["Medeniyet", "Çağdaşlaşma"],
            "kaynak": "Kastamonu Konuşması",
            "tarih": "1925-08-30"
        },
        {
            "metin": "Fikri hür, vicdanı hür, irfanı hür nesiller yetiştirmek ülkünün temelidir.",
            "kategori": ["Eğitim", "Özgürlük", "Gençlik"],
            "kaynak": "Öğretmenlerle Konuşma"
        },
        {
            "metin": "Türk milletinin yürümekte olduğu terakkî ve medeniyet yolunda, elinde ve kafasında olmak üzere tuttuğu meşale müspet ilimdir.",
            "kategori": ["Bilim", "İlerleme", "Medeniyet"],
            "kaynak": "TTK Genel Kurulu Açılış Konuşması",
            "tarih": "1931-04-15"
        }
    ]
    
    print("\n🔄 Örnek veriler yükleniyor...")
    print("=" * 70)
    
    # Toplu ekleme yap
    istatistik = arsiv.toplu_ekle(ornek_sozler)
    
    print(f"\n📊 Yükleme İstatistikleri:")
    print(f"   ✅ Başarıyla eklenen: {istatistik['eklenen']}")
    print(f"   ⚠️  Tekrarlı (atlandı): {istatistik['tekrar']}")
    print(f"   ❌ Hata: {istatistik['hata']}")
    
    # Güncel istatistikleri göster
    print("\n📈 Güncel Arşiv İstatistikleri:")
    istat = arsiv.istatistikler()
    print(f"   Toplam Kayıt: {istat['toplam_kayit']}")
    print(f"   Toplam Kelime: {istat['toplam_kelime']}")
    print(f"   Ortalama Kelime/Söz: {istat['ortalama_kelime']}")
    
    if istat['kategori_dagilimi']:
        print(f"\n🏷️  Kategori Dağılımı:")
        for kat, sayi in sorted(istat['kategori_dagilimi'].items(), key=lambda x: x[1], reverse=True):
            print(f"   {kat}: {sayi} söz")
    
    print("\n" + "=" * 70)
    print("✅ Örnek veriler başarıyla yüklendi!")
    
    return arsiv


if __name__ == "__main__":
    ornek_veriler_yukle()
