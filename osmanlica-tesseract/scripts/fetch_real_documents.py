#!/usr/bin/env python3
"""
Gerçek Osmanlıca Tarihsel Belgeleri İndirici

Bu script, açık kaynak platformlardan GERÇEK Osmanlıca tarihsel belgeleri indirir.
"""

import os
import sys
import requests
import json
from pathlib import Path
from typing import List, Dict, Optional
import time
from urllib.parse import urlencode
import re

class WikisourceOttomanFetcher:
    """
    Wikisource'tan gerçek Osmanlıca belgeleri indirir.
    
    Wikisource avantajları:
    - Zaten transkribe edilmiş (ground truth hazır!)
    - Kamu malı (telif yok)
    - API erişimi kolay
    - Yüksek kalite
    """
    
    def __init__(self, output_dir="training-data/wikisource"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.images_dir = self.output_dir / "images"
        self.groundtruth_dir = self.output_dir / "groundtruth"
        self.metadata_dir = self.output_dir / "metadata"
        
        for d in [self.images_dir, self.groundtruth_dir, self.metadata_dir]:
            d.mkdir(exist_ok=True)
        
        self.api_url = "https://tr.wikisource.org/w/api.php"
        self.base_url = "https://tr.wikisource.org"
        
    def get_ottoman_documents(self) -> List[Dict]:
        """
        Wikisource'tan Osmanlıca belge listesini al
        """
        print("📚 Wikisource'tan Osmanlıca belgeler aranıyor...")
        
        # Önemli Osmanlıca belgeler
        documents = [
            {
                "title": "Tanzimat Fermanı",
                "pages": ["Tanzimat_Fermanı"],
                "description": "1839 Tanzimat Fermanı",
                "year": 1839,
                "type": "ferman"
            },
            {
                "title": "Gülhane Hatt-ı Hümayunu",
                "pages": ["Gülhane_Hatt-ı_Hümayunu"],
                "description": "1839 Gülhane Hatt-ı Hümayunu",
                "year": 1839,
                "type": "ferman"
            },
            {
                "title": "Islahat Fermanı",
                "pages": ["Islahat_Fermanı"],
                "description": "1856 Islahat Fermanı",
                "year": 1856,
                "type": "ferman"
            },
            {
                "title": "Kanun-i Esasi",
                "pages": ["Kanun-i_Esasi"],
                "description": "1876 Osmanlı Anayasası",
                "year": 1876,
                "type": "anayasa"
            },
        ]
        
        return documents
    
    def fetch_page_content(self, page_title: str) -> Optional[str]:
        """
        Wikisource sayfasının içeriğini (transkripsiyon) al
        """
        params = {
            "action": "query",
            "format": "json",
            "titles": page_title,
            "prop": "revisions",
            "rvprop": "content",
            "rvslots": "main"
        }
        
        try:
            response = requests.get(self.api_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            pages = data.get("query", {}).get("pages", {})
            for page_id, page_data in pages.items():
                if page_id == "-1":
                    print(f"   ❌ Sayfa bulunamadı: {page_title}")
                    return None
                
                revisions = page_data.get("revisions", [])
                if revisions:
                    content = revisions[0].get("slots", {}).get("main", {}).get("*", "")
                    return content
            
            return None
            
        except Exception as e:
            print(f"   ⚠️ API hatası: {e}")
            return None
    
    def clean_wikitext(self, wikitext: str) -> str:
        """
        Wikitext'i temizle ve saf Osmanlıca metne dönüştür
        """
        if not wikitext:
            return ""
        
        # Wiki syntax'ı temizle
        text = wikitext
        
        # Şablonları kaldır ({{...}})
        text = re.sub(r'\{\{[^}]*\}\}', '', text)
        
        # Bağlantıları temizle ([[...]])
        text = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', text)  # [[link|text]] -> text
        text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)  # [[link]] -> link
        
        # HTML etiketlerini kaldır
        text = re.sub(r'<[^>]+>', '', text)
        
        # Başlıkları temizle (==...==)
        text = re.sub(r'={2,}([^=]+)={2,}', r'\1', text)
        
        # Kategorileri kaldır
        text = re.sub(r'\[\[Kategori:[^\]]+\]\]', '', text)
        
        # Çoklu boşlukları temizle
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        # Boş satırları kaldır
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        text = '\n'.join(lines)
        
        return text.strip()
    
    def render_page_as_pdf(self, page_title: str, output_pdf: Path) -> bool:
        """
        Wikisource sayfasını PDF olarak kaydet
        
        Not: Bu fonksiyon için wikisource export özelliği kullanılır
        """
        # Wikisource'un PDF export özelliği
        export_url = f"{self.base_url}/wiki/Özel:Kitap"
        
        print(f"   ℹ️ PDF oluşturmak için manuel adım gerekli:")
        print(f"   1. Tarayıcıda aç: {self.base_url}/wiki/{page_title}")
        print(f"   2. Sol menüden 'PDF olarak indir' seçeneğini tıkla")
        print(f"   3. İndirilen PDF'i buraya kaydet: {output_pdf}")
        print(f"   4. Veya screenshot al ve PNG olarak kaydet")
        
        return False
    
    def download_document(self, doc_info: Dict, output_prefix: str) -> bool:
        """
        Belgeyi indir ve kaydet
        """
        print(f"\n📄 İndiriliyor: {doc_info['title']}")
        print(f"   📅 Yıl: {doc_info['year']}")
        print(f"   📝 Tip: {doc_info['type']}")
        
        all_content = []
        
        for page_title in doc_info['pages']:
            print(f"   🔍 Sayfa: {page_title}")
            
            # İçeriği al (ground truth)
            content = self.fetch_page_content(page_title)
            
            if content:
                # Temizle
                cleaned = self.clean_wikitext(content)
                
                if cleaned:
                    all_content.append(cleaned)
                    print(f"   ✅ Transkripsiyon alındı ({len(cleaned)} karakter)")
                else:
                    print(f"   ⚠️ İçerik temizlenemedi")
            else:
                print(f"   ❌ İçerik alınamadı")
            
            time.sleep(1)  # API'yi yormamak için
        
        if not all_content:
            print(f"   ❌ Belge indirilemedi")
            return False
        
        # Ground truth'u kaydet
        combined_text = "\n\n---\n\n".join(all_content)
        gt_file = self.groundtruth_dir / f"{output_prefix}.txt"
        gt_file.write_text(combined_text, encoding='utf-8')
        print(f"   💾 Ground truth kaydedildi: {gt_file.name}")
        
        # Metadata kaydet
        metadata = {
            "title": doc_info['title'],
            "description": doc_info['description'],
            "year": doc_info['year'],
            "type": doc_info['type'],
            "source": "Wikisource",
            "url": f"{self.base_url}/wiki/{doc_info['pages'][0]}",
            "license": "Public Domain / CC0",
            "character_count": len(combined_text),
            "pages": doc_info['pages'],
            "downloaded_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        metadata_file = self.metadata_dir / f"{output_prefix}.json"
        metadata_file.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"   📋 Metadata kaydedildi: {metadata_file.name}")
        
        # Görüntü bilgisi
        print(f"\n   ℹ️ GÖRSELLEŞTİRME GEREKLİ:")
        print(f"   Manuel adımlar:")
        print(f"   1. Tarayıcıda aç: {metadata['url']}")
        print(f"   2. Sayfa screenshot'unu al")
        print(f"   3. Kaydet: {self.images_dir}/{output_prefix}.png")
        print(f"   4. Veya metin görselleştirme aracı kullan")
        
        return True
    
    def fetch_all_documents(self) -> int:
        """
        Tüm Osmanlıca belgeleri indir
        """
        print("=" * 70)
        print("🏛️ GERÇEK OSMANLI TARİHSEL BELGELERİ İNDİRİLİYOR")
        print("=" * 70)
        print()
        
        documents = self.get_ottoman_documents()
        print(f"📚 Toplam {len(documents)} belge bulundu")
        print()
        
        success_count = 0
        
        for i, doc in enumerate(documents, 1):
            output_prefix = f"doc_{i:03d}_{doc['title'].lower().replace(' ', '_').replace('-', '_')}"
            
            try:
                if self.download_document(doc, output_prefix):
                    success_count += 1
            except Exception as e:
                print(f"   ❌ Hata: {e}")
            
            print()
        
        print("=" * 70)
        print(f"✅ İndirme Tamamlandı")
        print(f"   Başarılı: {success_count}/{len(documents)}")
        print(f"   Ground Truth Dosyaları: {self.groundtruth_dir}")
        print(f"   Metadata Dosyaları: {self.metadata_dir}")
        print("=" * 70)
        print()
        print("⚠️ ÖNEMLİ NOT:")
        print("   Ground truth'lar (transkripsiyon) hazır!")
        print("   Görüntüler için manuel adımlar gerekli.")
        print("   Alternatif: Metin-görüntü oluşturucu kullanın.")
        print()
        
        return success_count

def create_text_images():
    """
    Ground truth'lardan görüntü oluştur
    """
    print("📸 Metin Görüntüleri Oluşturuluyor...")
    print()
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        print("   ℹ️ PIL/Pillow kullanılarak görüntüler oluşturulacak")
        print("   ⚠️ Osmanlıca font gerekli (örn: Scheherazade, Amiri)")
        print()
        
        # Bu fonksiyonellik isteğe bağlı, daha sonra genişletilebilir
        return True
        
    except ImportError:
        print("   ⚠️ Pillow kurulu değil")
        print("   Kurulum için: pip install Pillow")
        return False

def main():
    """Ana fonksiyon"""
    print()
    print("🏛️ OSMANLI TARİHSEL BELGE İNDİRİCİ")
    print("=" * 70)
    print()
    
    # Wikisource'tan indir
    fetcher = WikisourceOttomanFetcher()
    success_count = fetcher.fetch_all_documents()
    
    if success_count > 0:
        print("✅ Başarıyla tamamlandı!")
        print()
        print("📂 İndirilen Dosyalar:")
        print(f"   Ground Truth: {fetcher.groundtruth_dir}")
        print(f"   Metadata: {fetcher.metadata_dir}")
        print()
        print("🎯 Sonraki Adımlar:")
        print("   1. Ground truth'ları kontrol edin")
        print("   2. Görüntüler oluşturun (manuel veya otomatik)")
        print("   3. python3 scripts/validate_groundtruth.py çalıştırın")
        print("   4. Model eğitimine başlayın!")
        print()
        return 0
    else:
        print("❌ Hiçbir belge indirilemedi")
        return 1

if __name__ == "__main__":
    sys.exit(main())
