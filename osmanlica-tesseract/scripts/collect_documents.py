#!/usr/bin/env python3
"""
Osmanlıca Belge İndirici ve Hazırlayıcı

Bu script, açık kaynak Osmanlıca belgelerini indirir ve eğitim için hazırlar.
"""

import os
import requests
from pathlib import Path
import json
from typing import List, Dict
import time

# Açık kaynak Osmanlıca belge kaynakları
OPEN_SOURCES = {
    "archive_org": {
        "name": "Internet Archive - Ottoman Turkish Books",
        "collections": [
            "ottoman-turkish",
            "osmanliturkcekitaplar",
            "turkishmanuscripts",
        ],
        "api_base": "https://archive.org/services/search/v1/scrape"
    },
    "wikisource": {
        "name": "Wikisource - Ottoman Turkish",
        "url": "https://tr.wikisource.org/wiki/Kategori:Osmanlıca_metinler",
        "api": "https://tr.wikisource.org/w/api.php"
    },
    "hathitrust": {
        "name": "HathiTrust Digital Library",
        "search": "https://babel.hathitrust.org/cgi/ls?a=srchls&q1=ottoman+turkish&lmt=ft",
        "note": "Public domain books only"
    }
}

class OttomanDocumentCollector:
    """Açık kaynak Osmanlıca belgelerini toplayan sınıf"""
    
    def __init__(self, output_dir="training-data/collected"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.images_dir = self.output_dir / "images"
        self.metadata_dir = self.output_dir / "metadata"
        
        self.images_dir.mkdir(exist_ok=True)
        self.metadata_dir.mkdir(exist_ok=True)
    
    def search_archive_org(self, query="ottoman turkish", max_results=50):
        """
        Archive.org'da Osmanlıca belgeler ara
        
        Args:
            query: Arama sorgusu
            max_results: Maksimum sonuç sayısı
        """
        print(f"\n🔍 Archive.org'da aranıyor: '{query}'")
        
        # Archive.org Advanced Search API
        params = {
            "q": f"{query} AND mediatype:texts",
            "fl[]": ["identifier", "title", "creator", "year", "language"],
            "rows": max_results,
            "page": 1
        }
        
        try:
            response = requests.get(OPEN_SOURCES["archive_org"]["api_base"], params=params)
            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])
                
                print(f"✅ {len(items)} belge bulundu")
                
                # Sonuçları kaydet
                results_file = self.metadata_dir / "archive_org_results.json"
                with open(results_file, 'w', encoding='utf-8') as f:
                    json.dump(items, f, indent=2, ensure_ascii=False)
                
                return items
            else:
                print(f"❌ Hata: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Hata: {e}")
            return []
    
    def get_recommended_sources(self):
        """
        Elle seçilmiş, kaliteli açık kaynak Osmanlıca kaynaklar
        """
        recommendations = [
            {
                "source": "Archive.org",
                "id": "kitbuttevhid00sade",
                "title": "Kitab-üt Tevhid",
                "url": "https://archive.org/details/kitbuttevhid00sade",
                "pages": 200,
                "quality": "high",
                "license": "Public Domain",
                "format": "DjVu, PDF",
                "notes": "19. yüzyıl Osmanlıca matbu eser, net baskı"
            },
            {
                "source": "Archive.org",
                "id": "mevlidiveysihan00gazi",
                "title": "Mevlidi Veysi Han",
                "url": "https://archive.org/details/mevlidiveysihan00gazi",
                "pages": 150,
                "quality": "high",
                "license": "Public Domain"
            },
            {
                "source": "Archive.org",
                "id": "gulistn00saadi",
                "title": "Gülistan (Osmanlıca tercüme)",
                "url": "https://archive.org/details/gulistn00saadi",
                "pages": 300,
                "quality": "high",
                "license": "Public Domain"
            },
            {
                "source": "Wikisource",
                "title": "Tanzimat Fermanı",
                "url": "https://tr.wikisource.org/wiki/Tanzimat_Fermanı",
                "pages": 5,
                "quality": "high",
                "transcription": "Available",
                "license": "CC0"
            }
        ]
        
        return recommendations
    
    def download_archive_org_item(self, identifier, max_pages=None):
        """
        Archive.org'dan belge indir
        
        Args:
            identifier: Archive.org item ID
            max_pages: Maksimum sayfa sayısı (None = tümü)
        """
        print(f"\n📥 İndiriliyor: {identifier}")
        
        # Metadata al
        metadata_url = f"https://archive.org/metadata/{identifier}"
        try:
            response = requests.get(metadata_url)
            if response.status_code != 200:
                print(f"❌ Metadata alınamadı: {response.status_code}")
                return False
            
            metadata = response.json()
            title = metadata.get('metadata', {}).get('title', identifier)
            
            print(f"📖 Başlık: {title}")
            
            # PDF veya DjVu dosyasını bul
            files = metadata.get('files', [])
            pdf_file = None
            djvu_file = None
            
            for file in files:
                name = file.get('name', '')
                if name.endswith('.pdf'):
                    pdf_file = name
                elif name.endswith('.djvu'):
                    djvu_file = name
            
            download_file = pdf_file or djvu_file
            
            if not download_file:
                print("❌ PDF veya DjVu dosyası bulunamadı")
                return False
            
            # İndir
            download_url = f"https://archive.org/download/{identifier}/{download_file}"
            print(f"⬇️  İndiriliyor: {download_url}")
            
            # Dosya adı
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            output_file = self.output_dir / f"{identifier}_{safe_title}.{download_file.split('.')[-1]}"
            
            # İndirme (büyük dosyalar için streaming)
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                
                with open(output_file, 'wb') as f:
                    downloaded = 0
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size:
                            percent = (downloaded / total_size) * 100
                            print(f"\r⏳ İlerleme: {percent:.1f}%", end='')
            
            print(f"\n✅ İndirildi: {output_file}")
            
            # Metadata kaydet
            metadata_file = self.metadata_dir / f"{identifier}_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            return output_file
            
        except Exception as e:
            print(f"❌ Hata: {e}")
            return False
    
    def generate_collection_report(self):
        """
        Toplanan belgeler hakkında rapor oluştur
        """
        report_file = self.output_dir / "COLLECTION_REPORT.md"
        
        # Dosyaları tara
        pdf_files = list(self.output_dir.glob("*.pdf"))
        djvu_files = list(self.output_dir.glob("*.djvu"))
        metadata_files = list(self.metadata_dir.glob("*_metadata.json"))
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Toplanan Osmanlıca Belgeler Raporu\n\n")
            f.write(f"**Tarih**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Özet\n\n")
            f.write(f"- PDF Dosyaları: {len(pdf_files)}\n")
            f.write(f"- DjVu Dosyaları: {len(djvu_files)}\n")
            f.write(f"- Toplam: {len(pdf_files) + len(djvu_files)} belge\n\n")
            
            f.write("## İndirilen Belgeler\n\n")
            
            for pdf in pdf_files:
                f.write(f"- 📄 {pdf.name}\n")
            
            for djvu in djvu_files:
                f.write(f"- 📄 {djvu.name}\n")
            
            f.write("\n## Sonraki Adımlar\n\n")
            f.write("1. PDF/DjVu dosyalarını PNG görüntülere dönüştürün\n")
            f.write("2. Ground truth transkripsiyon oluşturun\n")
            f.write("3. training-data/images/ ve training-data/ground-truth/ dizinlerine ekleyin\n")
            f.write("4. Model eğitimini başlatın\n")
        
        print(f"\n📊 Rapor oluşturuldu: {report_file}")


def main():
    """Ana script"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Osmanlıca belge toplayıcı')
    parser.add_argument('--action', choices=['search', 'download', 'recommend'], 
                       default='recommend',
                       help='Yapılacak işlem')
    parser.add_argument('--query', default='ottoman turkish',
                       help='Arama sorgusu')
    parser.add_argument('--identifier', 
                       help='Archive.org belge ID')
    
    args = parser.parse_args()
    
    collector = OttomanDocumentCollector()
    
    if args.action == 'search':
        results = collector.search_archive_org(args.query)
        print(f"\n✅ {len(results)} sonuç bulundu")
        print("📁 Sonuçlar: training-data/collected/metadata/archive_org_results.json")
    
    elif args.action == 'download':
        if not args.identifier:
            print("❌ --identifier parametresi gerekli")
            return
        
        collector.download_archive_org_item(args.identifier)
    
    elif args.action == 'recommend':
        recommendations = collector.get_recommended_sources()
        
        print("\n" + "="*60)
        print("  ÖNERİLEN KALİTELİ OSMANICA KAYNAKLAR")
        print("="*60 + "\n")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['title']}")
            print(f"   📍 Kaynak: {rec['source']}")
            print(f"   🔗 URL: {rec['url']}")
            print(f"   📄 Sayfa: {rec['pages']}")
            print(f"   ⭐ Kalite: {rec['quality']}")
            print(f"   📜 Lisans: {rec['license']}")
            if 'id' in rec:
                print(f"   🆔 ID: {rec['id']}")
            print()
        
        print("İndirmek için:")
        print("python scripts/collect_documents.py --action download --identifier <ID>")
        
        collector.generate_collection_report()


if __name__ == '__main__':
    main()
