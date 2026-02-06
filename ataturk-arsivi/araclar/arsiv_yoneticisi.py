#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atatürk Arşiv Yöneticisi
========================
Mustafa Kemal Atatürk'ün sözlerini, cümlelerini ve paragraflarını
yönetmek için geliştirilmiş kapsamlı arşiv sistemi.

Özellikler:
- Tekrarlı kayıtları tespit etme ve engelleme
- Kategorize etme
- Arama ve filtreleme
- İçe ve dışa aktarma
- Tarih ve kaynak takibi
"""

import json
import hashlib
import os
from datetime import datetime
from typing import List, Dict, Optional, Set
import re


class AtaturkArsivi:
    """Atatürk sözleri ve yazıları için arşiv yönetim sistemi."""
    
    def __init__(self, veri_dosyasi: str = "veriler/sozler.json"):
        """
        Arşiv yöneticisini başlatır.
        
        Args:
            veri_dosyasi: JSON veri dosyasının yolu
        """
        self.veri_dosyasi = veri_dosyasi
        self.veriler = self._veri_yukle()
        self.hash_seti: Set[str] = self._hash_seti_olustur()
    
    def _veri_yukle(self) -> Dict:
        """JSON dosyasından verileri yükler."""
        if os.path.exists(self.veri_dosyasi):
            with open(self.veri_dosyasi, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "metadata": {
                "versiyon": "1.0",
                "olusturma_tarihi": datetime.now().strftime("%Y-%m-%d"),
                "aciklama": "Mustafa Kemal Atatürk'ün sözleri, cümleleri ve paragraflarından oluşan kapsamlı arşiv",
                "toplam_kayit": 0,
                "son_guncelleme": datetime.now().strftime("%Y-%m-%d")
            },
            "sozler": [],
            "kategoriler": []
        }
    
    def _veri_kaydet(self):
        """Verileri JSON dosyasına kaydeder."""
        os.makedirs(os.path.dirname(self.veri_dosyasi), exist_ok=True)
        self.veriler["metadata"]["son_guncelleme"] = datetime.now().strftime("%Y-%m-%d")
        self.veriler["metadata"]["toplam_kayit"] = len(self.veriler["sozler"])
        
        with open(self.veri_dosyasi, 'w', encoding='utf-8') as f:
            json.dump(self.veriler, f, ensure_ascii=False, indent=2)
    
    def _hash_seti_olustur(self) -> Set[str]:
        """Mevcut sözlerin hash değerlerinden bir set oluşturur."""
        return {soz.get("hash", "") for soz in self.veriler.get("sozler", [])}
    
    @staticmethod
    def _metin_hash_olustur(metin: str) -> str:
        """
        Metinden benzersiz bir hash oluşturur.
        Noktalama işaretleri ve boşluklar normalize edilerek karşılaştırma yapılır.
        """
        # Metni temizle ve normalize et
        temiz_metin = re.sub(r'[^\w\s]', '', metin.lower().strip())
        temiz_metin = re.sub(r'\s+', ' ', temiz_metin)
        return hashlib.sha256(temiz_metin.encode('utf-8')).hexdigest()
    
    def soz_ekle(self, 
                 metin: str, 
                 kategori: Optional[List[str]] = None,
                 tarih: Optional[str] = None,
                 kaynak: Optional[str] = None,
                 yer: Optional[str] = None,
                 notlar: Optional[str] = None) -> bool:
        """
        Arşive yeni bir söz, cümle veya paragraf ekler.
        
        Args:
            metin: Eklenecek metin
            kategori: Kategoriler (örn: ["Eğitim", "Bilim"])
            tarih: Söylenme/yazılma tarihi
            kaynak: Kaynağın adı (kitap, konuşma, vs.)
            yer: Söylendiği/yazıldığı yer
            notlar: Ek notlar
        
        Returns:
            True: Ekleme başarılı
            False: Tekrarlı kayıt, eklenmedi
        """
        if not metin or not metin.strip():
            print("❌ Boş metin eklenemez!")
            return False
        
        # Hash kontrolü - tekrar kontrolü
        metin_hash = self._metin_hash_olustur(metin)
        if metin_hash in self.hash_seti:
            print(f"⚠️  Bu söz zaten arşivde mevcut (tekrarlı kayıt)!")
            return False
        
        # Yeni kayıt oluştur
        yeni_kayit = {
            "id": len(self.veriler["sozler"]) + 1,
            "metin": metin.strip(),
            "hash": metin_hash,
            "kategori": kategori or [],
            "tarih": tarih,
            "kaynak": kaynak,
            "yer": yer,
            "notlar": notlar,
            "eklenme_zamani": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "kelime_sayisi": len(metin.split()),
            "karakter_sayisi": len(metin)
        }
        
        self.veriler["sozler"].append(yeni_kayit)
        self.hash_seti.add(metin_hash)
        self._veri_kaydet()
        
        print(f"✅ Söz başarıyla eklendi! (ID: {yeni_kayit['id']})")
        return True
    
    def toplu_ekle(self, sozler_listesi: List[Dict]) -> Dict[str, int]:
        """
        Birden fazla sözü toplu olarak ekler.
        
        Args:
            sozler_listesi: Eklenecek sözlerin listesi
        
        Returns:
            İstatistik sözlüğü (eklenen, tekrar, hata)
        """
        istatistik = {"eklenen": 0, "tekrar": 0, "hata": 0}
        
        for soz_data in sozler_listesi:
            try:
                if self.soz_ekle(
                    metin=soz_data.get("metin", ""),
                    kategori=soz_data.get("kategori"),
                    tarih=soz_data.get("tarih"),
                    kaynak=soz_data.get("kaynak"),
                    yer=soz_data.get("yer"),
                    notlar=soz_data.get("notlar")
                ):
                    istatistik["eklenen"] += 1
                else:
                    istatistik["tekrar"] += 1
            except Exception as e:
                print(f"❌ Hata: {e}")
                istatistik["hata"] += 1
        
        return istatistik
    
    def ara(self, 
            anahtar_kelime: Optional[str] = None,
            kategori: Optional[str] = None,
            tarih: Optional[str] = None,
            kaynak: Optional[str] = None) -> List[Dict]:
        """
        Arşivde arama yapar.
        
        Args:
            anahtar_kelime: Aranacak kelime/kelimeler
            kategori: Kategori filtresi
            tarih: Tarih filtresi
            kaynak: Kaynak filtresi
        
        Returns:
            Bulunan kayıtların listesi
        """
        sonuclar = self.veriler["sozler"].copy()
        
        if anahtar_kelime:
            anahtar = anahtar_kelime.lower()
            sonuclar = [s for s in sonuclar if anahtar in s["metin"].lower()]
        
        if kategori:
            sonuclar = [s for s in sonuclar if kategori in s.get("kategori", [])]
        
        if tarih:
            sonuclar = [s for s in sonuclar if s.get("tarih") == tarih]
        
        if kaynak:
            sonuclar = [s for s in sonuclar if kaynak.lower() in (s.get("kaynak") or "").lower()]
        
        return sonuclar
    
    def istatistikler(self) -> Dict:
        """Arşiv istatistiklerini döndürür."""
        sozler = self.veriler["sozler"]
        
        if not sozler:
            return {
                "toplam_kayit": 0,
                "toplam_kelime": 0,
                "ortalama_kelime": 0,
                "en_uzun_soz": None,
                "en_kisa_soz": None,
                "kategori_dagilimi": {}
            }
        
        toplam_kelime = sum(s["kelime_sayisi"] for s in sozler)
        
        # Kategori dağılımı
        kategori_sayaci = {}
        for soz in sozler:
            for kat in soz.get("kategori", []):
                kategori_sayaci[kat] = kategori_sayaci.get(kat, 0) + 1
        
        return {
            "toplam_kayit": len(sozler),
            "toplam_kelime": toplam_kelime,
            "ortalama_kelime": toplam_kelime // len(sozler),
            "en_uzun_soz": max(sozler, key=lambda x: x["kelime_sayisi"]),
            "en_kisa_soz": min(sozler, key=lambda x: x["kelime_sayisi"]),
            "kategori_dagilimi": kategori_sayaci
        }
    
    def yazdir_soz(self, soz: Dict):
        """Bir sözü formatlanmış şekilde yazdırır."""
        print("\n" + "="*70)
        print(f"📝 ID: {soz['id']}")
        print(f"💬 Söz: \"{soz['metin']}\"")
        
        if soz.get("kategori"):
            print(f"🏷️  Kategori: {', '.join(soz['kategori'])}")
        
        if soz.get("tarih"):
            print(f"📅 Tarih: {soz['tarih']}")
        
        if soz.get("kaynak"):
            print(f"📚 Kaynak: {soz['kaynak']}")
        
        if soz.get("yer"):
            print(f"📍 Yer: {soz['yer']}")
        
        if soz.get("notlar"):
            print(f"📌 Notlar: {soz['notlar']}")
        
        print(f"📊 {soz['kelime_sayisi']} kelime, {soz['karakter_sayisi']} karakter")
        print("="*70)
    
    def disa_aktar(self, dosya_adi: str, format: str = "json"):
        """
        Arşivi farklı formatlarda dışa aktarır.
        
        Args:
            dosya_adi: Hedef dosya adı
            format: Dosya formatı (json, txt, md)
        """
        if format == "json":
            with open(dosya_adi, 'w', encoding='utf-8') as f:
                json.dump(self.veriler, f, ensure_ascii=False, indent=2)
        
        elif format == "txt":
            with open(dosya_adi, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("MUSTAFA KEMAL ATATÜRK SÖZLERİ ARŞİVİ\n")
                f.write("=" * 70 + "\n\n")
                
                for soz in self.veriler["sozler"]:
                    f.write(f"ID: {soz['id']}\n")
                    f.write(f"{soz['metin']}\n")
                    
                    if soz.get("kategori"):
                        f.write(f"Kategori: {', '.join(soz['kategori'])}\n")
                    if soz.get("tarih"):
                        f.write(f"Tarih: {soz['tarih']}\n")
                    if soz.get("kaynak"):
                        f.write(f"Kaynak: {soz['kaynak']}\n")
                    
                    f.write("\n" + "-" * 70 + "\n\n")
        
        elif format == "md":
            with open(dosya_adi, 'w', encoding='utf-8') as f:
                f.write("# Mustafa Kemal Atatürk Sözleri Arşivi\n\n")
                
                istat = self.istatistikler()
                f.write(f"**Toplam Kayıt:** {istat['toplam_kayit']}\n\n")
                f.write(f"**Toplam Kelime:** {istat['toplam_kelime']}\n\n")
                f.write("---\n\n")
                
                for soz in self.veriler["sozler"]:
                    f.write(f"## {soz['id']}. Söz\n\n")
                    f.write(f"> {soz['metin']}\n\n")
                    
                    if soz.get("kategori"):
                        f.write(f"**Kategori:** {', '.join(soz['kategori'])}\n\n")
                    if soz.get("tarih"):
                        f.write(f"**Tarih:** {soz['tarih']}\n\n")
                    if soz.get("kaynak"):
                        f.write(f"**Kaynak:** {soz['kaynak']}\n\n")
                    
                    f.write("---\n\n")
        
        print(f"✅ Arşiv '{dosya_adi}' dosyasına aktarıldı!")


def main():
    """Ana program - örnek kullanım."""
    print("🇹🇷 Atatürk Arşiv Yöneticisi")
    print("=" * 70)
    
    # Arşiv oluştur
    arsiv = AtaturkArsivi()
    
    # İstatistikleri göster
    istat = arsiv.istatistikler()
    print(f"\n📊 Mevcut Arşiv İstatistikleri:")
    print(f"   Toplam Kayıt: {istat['toplam_kayit']}")
    print(f"   Toplam Kelime: {istat['toplam_kelime']}")
    
    if istat['toplam_kayit'] > 0:
        print(f"   Ortalama Kelime/Söz: {istat['ortalama_kelime']}")
        print(f"\n📈 Kategori Dağılımı:")
        for kat, sayi in istat['kategori_dagilimi'].items():
            print(f"   {kat}: {sayi} söz")


if __name__ == "__main__":
    main()
