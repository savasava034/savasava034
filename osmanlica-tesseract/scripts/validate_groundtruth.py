#!/usr/bin/env python3
"""
Ground Truth Doğrulama Aracı

Ground truth dosyalarının kalitesini kontrol eder.
"""

import os
import sys
from pathlib import Path
import re

class GroundTruthValidator:
    """Ground truth kalite kontrolü"""
    
    def __init__(self, images_dir="training-data/images", 
                 gt_dir="training-data/ground-truth"):
        self.images_dir = Path(images_dir)
        self.gt_dir = Path(gt_dir)
        
        # Osmanlıca karakter seti
        self.valid_chars = set("ابتثجحخدذرزسشصضطظعغفقكلمنهويءآأؤإئةىپچژگ")
        self.valid_chars.update("۰۱۲۳۴۵۶۷۸۹0123456789")
        self.valid_chars.update(".,;:!?-()[]{}\"' \n\r\t")
    
    def check_pairing(self):
        """Görüntü ve ground truth eşleşmesini kontrol et"""
        print("\n🔍 Eşleşme Kontrolü")
        print("="*60)
        
        if not self.images_dir.exists():
            print(f"❌ Görüntü dizini bulunamadı: {self.images_dir}")
            return False
        
        if not self.gt_dir.exists():
            print(f"❌ Ground truth dizini bulunamadı: {self.gt_dir}")
            return False
        
        # Görüntüleri bul
        image_files = {}
        for ext in ['.png', '.jpg', '.jpeg', '.tif', '.tiff']:
            for img in self.images_dir.glob(f"*{ext}"):
                base_name = img.stem
                image_files[base_name] = img
        
        # Ground truth dosyalarını bul
        gt_files = {}
        for gt in self.gt_dir.glob("*.gt.txt"):
            base_name = gt.stem.replace('.gt', '')
            gt_files[base_name] = gt
        
        print(f"📊 Toplam görüntü: {len(image_files)}")
        print(f"📊 Toplam ground truth: {len(gt_files)}")
        
        # Eksik eşleşmeleri bul
        missing_gt = []
        for img_name in image_files:
            if img_name not in gt_files:
                missing_gt.append(img_name)
        
        orphan_gt = []
        for gt_name in gt_files:
            if gt_name not in image_files:
                orphan_gt.append(gt_name)
        
        if missing_gt:
            print(f"\n⚠️  Ground truth eksik ({len(missing_gt)}):")
            for name in missing_gt[:10]:
                print(f"   - {name}")
            if len(missing_gt) > 10:
                print(f"   ... ve {len(missing_gt)-10} tane daha")
        
        if orphan_gt:
            print(f"\n⚠️  Görüntüsü olmayan ground truth ({len(orphan_gt)}):")
            for name in orphan_gt[:10]:
                print(f"   - {name}")
            if len(orphan_gt) > 10:
                print(f"   ... ve {len(orphan_gt)-10} tane daha")
        
        if not missing_gt and not orphan_gt:
            print("\n✅ Tüm eşleşmeler tamam!")
            return True
        
        return False
    
    def check_encoding(self):
        """UTF-8 encoding kontrolü"""
        print("\n🔍 Encoding Kontrolü")
        print("="*60)
        
        gt_files = list(self.gt_dir.glob("*.gt.txt"))
        errors = []
        
        for gt_file in gt_files:
            try:
                with open(gt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Başarılı
            except UnicodeDecodeError:
                errors.append(gt_file.name)
        
        if errors:
            print(f"❌ UTF-8 olmayan dosyalar ({len(errors)}):")
            for name in errors:
                print(f"   - {name}")
            print("\nDüzeltme:")
            print("   1. Dosyayı UTF-8 ile tekrar kaydet")
            print("   2. Veya: iconv -f ISO-8859-9 -t UTF-8 dosya.txt > yeni.txt")
            return False
        
        print(f"✅ Tüm dosyalar UTF-8 ({len(gt_files)} dosya)")
        return True
    
    def check_content(self):
        """İçerik kalitesi kontrolü"""
        print("\n🔍 İçerik Kalitesi Kontrolü")
        print("="*60)
        
        gt_files = list(self.gt_dir.glob("*.gt.txt"))
        
        empty_files = []
        placeholder_files = []
        invalid_chars = {}
        
        for gt_file in gt_files:
            with open(gt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Boş dosya?
            if not content.strip():
                empty_files.append(gt_file.name)
                continue
            
            # Placeholder?
            if 'TODO' in content or '# TODO' in content:
                placeholder_files.append(gt_file.name)
                continue
            
            # Geçersiz karakterler?
            for char in content:
                if char not in self.valid_chars:
                    if gt_file.name not in invalid_chars:
                        invalid_chars[gt_file.name] = []
                    invalid_chars[gt_file.name].append(char)
        
        issues = False
        
        if empty_files:
            print(f"\n⚠️  Boş dosyalar ({len(empty_files)}):")
            for name in empty_files[:10]:
                print(f"   - {name}")
            issues = True
        
        if placeholder_files:
            print(f"\n⚠️  Placeholder dosyalar ({len(placeholder_files)}):")
            for name in placeholder_files[:10]:
                print(f"   - {name}")
            print("   → Bu dosyaları doldurmanız gerekiyor!")
            issues = True
        
        if invalid_chars:
            print(f"\n⚠️  Beklenmeyen karakterler ({len(invalid_chars)} dosya):")
            for name, chars in list(invalid_chars.items())[:5]:
                unique_chars = set(chars)
                print(f"   - {name}: {', '.join(repr(c) for c in list(unique_chars)[:10])}")
            print("   → Bu karakterler Osmanlıca karakter setinde yok")
            issues = True
        
        if not issues:
            print(f"\n✅ Tüm dosyalar temiz ({len(gt_files)} dosya)")
            return True
        
        return False
    
    def check_statistics(self):
        """İstatistikler"""
        print("\n📊 İstatistikler")
        print("="*60)
        
        gt_files = list(self.gt_dir.glob("*.gt.txt"))
        
        total_lines = 0
        total_chars = 0
        total_words = 0
        
        for gt_file in gt_files:
            with open(gt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Placeholder'ları atla
            if 'TODO' in content:
                continue
            
            lines = content.split('\n')
            total_lines += len([l for l in lines if l.strip()])
            total_chars += len(content)
            total_words += len(content.split())
        
        valid_files = len([f for f in gt_files 
                          if 'TODO' not in open(f, 'r', encoding='utf-8').read()])
        
        print(f"Geçerli dosyalar: {valid_files}")
        print(f"Toplam satır: {total_lines}")
        print(f"Toplam karakter: {total_chars}")
        print(f"Toplam kelime: {total_words}")
        
        if valid_files > 0:
            print(f"\nOrtalama:")
            print(f"  Satır/dosya: {total_lines/valid_files:.1f}")
            print(f"  Karakter/dosya: {total_chars/valid_files:.1f}")
            print(f"  Kelime/dosya: {total_words/valid_files:.1f}")
    
    def generate_report(self):
        """Tam rapor oluştur"""
        print("\n" + "="*60)
        print("  GROUND TRUTH KALİTE RAPORU")
        print("="*60)
        
        pairing_ok = self.check_pairing()
        encoding_ok = self.check_encoding()
        content_ok = self.check_content()
        self.check_statistics()
        
        print("\n" + "="*60)
        print("  SONUÇ")
        print("="*60)
        
        if pairing_ok and encoding_ok and content_ok:
            print("\n✅ TÜM KONTROLLER BAŞARILI!")
            print("Model eğitimine başlayabilirsiniz.")
            return True
        else:
            print("\n⚠️  SORUNLAR VAR!")
            print("Yukarıdaki sorunları düzeltin ve tekrar çalıştırın.")
            return False


def main():
    """Ana işlev"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Ground truth kalite kontrolü')
    parser.add_argument('--images', default='training-data/images',
                       help='Görüntü dizini')
    parser.add_argument('--gt', default='training-data/ground-truth',
                       help='Ground truth dizini')
    
    args = parser.parse_args()
    
    validator = GroundTruthValidator(args.images, args.gt)
    success = validator.generate_report()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
