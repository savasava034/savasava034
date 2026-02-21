#!/usr/bin/env python3
"""
PDF/DjVu'dan Eğitim Verisi Hazırlayıcı

İndirilen belgeleri eğitim için hazırlar.
"""

import os
import sys
from pathlib import Path
from PIL import Image
import subprocess
import json

class TrainingDataPreparer:
    """Belgeleri eğitim verisi formatına dönüştürür"""
    
    def __init__(self, source_dir="training-data/collected", 
                 output_images="training-data/images",
                 output_gt="training-data/ground-truth"):
        self.source_dir = Path(source_dir)
        self.images_dir = Path(output_images)
        self.gt_dir = Path(output_gt)
        
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.gt_dir.mkdir(parents=True, exist_ok=True)
    
    def pdf_to_images(self, pdf_file, dpi=300, max_pages=None):
        """
        PDF'i görüntülere dönüştür
        
        Args:
            pdf_file: PDF dosya yolu
            dpi: Çözünürlük
            max_pages: Maksimum sayfa (None = tümü)
        """
        pdf_path = Path(pdf_file)
        if not pdf_path.exists():
            print(f"❌ Dosya bulunamadı: {pdf_file}")
            return []
        
        print(f"\n📄 PDF işleniyor: {pdf_path.name}")
        
        # Çıktı dizini
        doc_name = pdf_path.stem
        
        try:
            # pdftoppm ile PDF'i PNG'ye çevir (poppler-utils gerekli)
            cmd = [
                'pdftoppm',
                '-png',
                '-r', str(dpi),
                str(pdf_path),
                str(self.images_dir / doc_name)
            ]
            
            if max_pages:
                cmd.extend(['-l', str(max_pages)])
            
            print(f"⚙️  Komut: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Oluşturulan dosyaları bul
                created_files = list(self.images_dir.glob(f"{doc_name}-*.png"))
                print(f"✅ {len(created_files)} sayfa dönüştürüldü")
                return created_files
            else:
                print(f"❌ Hata: {result.stderr}")
                return []
                
        except FileNotFoundError:
            print("❌ pdftoppm bulunamadı. Kurulum:")
            print("   Ubuntu/Debian: sudo apt-get install poppler-utils")
            print("   macOS: brew install poppler")
            return []
        except Exception as e:
            print(f"❌ Hata: {e}")
            return []
    
    def create_placeholder_groundtruth(self, image_files):
        """
        Görüntüler için placeholder ground truth dosyaları oluştur
        
        Args:
            image_files: Görüntü dosyaları listesi
        """
        print(f"\n📝 Ground truth placeholder'ları oluşturuluyor...")
        
        for img_file in image_files:
            # Ground truth dosya adı
            gt_file = self.gt_dir / f"{img_file.stem}.gt.txt"
            
            if not gt_file.exists():
                with open(gt_file, 'w', encoding='utf-8') as f:
                    f.write("# TODO: Bu sayfanın transkripsiyon ekleyin\n")
                    f.write("# Osmanlıca metin buraya yazılacak\n")
                    f.write("#\n")
                    f.write("# Araçlar:\n")
                    f.write("# - Transkribus: https://readcoop.eu/transkribus/\n")
                    f.write("# - Manuel transkripsiyon\n")
                    f.write("#\n")
                    f.write("# Görüntü: {}\n".format(img_file.name))
        
        print(f"✅ {len(image_files)} ground truth dosyası oluşturuldu")
        print(f"📁 Konum: {self.gt_dir}")
        print("\n⚠️  DİKKAT: Ground truth dosyalarını manuel olarak doldurmanız gerekiyor!")
    
    def optimize_images(self, image_dir=None):
        """
        Görüntüleri OCR için optimize et
        
        Args:
            image_dir: Görüntü dizini (None = varsayılan)
        """
        if image_dir is None:
            image_dir = self.images_dir
        
        print(f"\n🔧 Görüntüler optimize ediliyor...")
        
        from scripts.preprocess import preprocess_image
        
        optimized_dir = image_dir.parent / f"{image_dir.name}_optimized"
        optimized_dir.mkdir(exist_ok=True)
        
        image_files = list(image_dir.glob("*.png"))
        
        for img_file in image_files:
            output_file = optimized_dir / img_file.name
            
            try:
                preprocess_image(
                    str(img_file),
                    str(output_file),
                    denoise=True,
                    deskew=True,
                    binarize=True,
                    enhance_contrast=True
                )
                print(f"✅ {img_file.name}")
            except Exception as e:
                print(f"❌ {img_file.name}: {e}")
        
        print(f"\n✅ Optimize edilmiş görüntüler: {optimized_dir}")


def create_dataset_readme(output_dir):
    """
    Veri seti için README oluştur
    """
    readme_file = Path(output_dir) / "DATASET_README.md"
    
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write("# Osmanlıca Eğitim Veri Seti\n\n")
        f.write("Bu veri seti açık kaynak Osmanlıca belgelerinden oluşturulmuştur.\n\n")
        
        f.write("## Kaynak\n\n")
        f.write("- Archive.org (Public Domain)\n")
        f.write("- Wikisource (CC0 / Public Domain)\n")
        f.write("- Diğer açık kaynak koleksiyonlar\n\n")
        
        f.write("## Lisans\n\n")
        f.write("Bu belgeler kamu malıdır (Public Domain) veya açık lisanslıdır.\n")
        f.write("Kullanım, dağıtım ve değiştirme serbesttir.\n\n")
        
        f.write("## Kullanım\n\n")
        f.write("```bash\n")
        f.write("# Model eğitimi\n")
        f.write("python scripts/train_tesseract.py \\\n")
        f.write("    --action finetune \\\n")
        f.write("    --base-model ara \\\n")
        f.write("    --iterations 10000\n")
        f.write("```\n\n")
        
        f.write("## Ground Truth\n\n")
        f.write("⚠️ **ÖNEMLİ**: Ground truth dosyaları manuel transkripsiyon gerektirir!\n\n")
        f.write("Her görüntü için `.gt.txt` dosyasını düzenleyin:\n")
        f.write("1. Görüntüyü açın\n")
        f.write("2. Metni doğru bir şekilde transkribe edin\n")
        f.write("3. UTF-8 formatında kaydedin\n\n")
        
        f.write("## İstatistikler\n\n")
        
        # İstatistikleri hesapla
        images_dir = Path(output_dir) / "../images"
        if images_dir.exists():
            image_files = list(images_dir.glob("*.png"))
            f.write(f"- Görüntü sayısı: {len(image_files)}\n")
        
        f.write("\n## Katkıda Bulunma\n\n")
        f.write("Ground truth transkripsiyon katkılarınızı bekliyoruz!\n")
    
    print(f"\n📄 README oluşturuldu: {readme_file}")


def main():
    """Ana işlev"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Belgeleri eğitim verisi formatına hazırla')
    parser.add_argument('--pdf', help='İşlenecek PDF dosyası')
    parser.add_argument('--dpi', type=int, default=300, help='Çözünürlük (DPI)')
    parser.add_argument('--max-pages', type=int, help='Maksimum sayfa sayısı')
    parser.add_argument('--optimize', action='store_true', help='Görüntüleri optimize et')
    
    args = parser.parse_args()
    
    preparer = TrainingDataPreparer()
    
    if args.pdf:
        # PDF'i işle
        image_files = preparer.pdf_to_images(args.pdf, args.dpi, args.max_pages)
        
        if image_files:
            # Ground truth placeholder'ları oluştur
            preparer.create_placeholder_groundtruth(image_files)
            
            # Optimize et
            if args.optimize:
                preparer.optimize_images()
            
            # README oluştur
            create_dataset_readme("training-data")
            
            print("\n" + "="*60)
            print("  BAŞARILI!")
            print("="*60)
            print(f"\n✅ {len(image_files)} sayfa hazırlandı")
            print(f"📁 Görüntüler: training-data/images/")
            print(f"📝 Ground truth: training-data/ground-truth/")
            print("\n⚠️  SONRAKİ ADIM: Ground truth dosyalarını manuel olarak doldurun!")
            print("   Her .gt.txt dosyasını açıp Osmanlıca metni transkribe edin.")
    else:
        print("Kullanım: python scripts/prepare_training_data.py --pdf <dosya.pdf>")
        print("\nÖrnek:")
        print("python scripts/prepare_training_data.py --pdf training-data/collected/document.pdf --max-pages 50")


if __name__ == '__main__':
    main()
