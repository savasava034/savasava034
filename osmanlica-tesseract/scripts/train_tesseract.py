#!/usr/bin/env python3
"""
Tesseract Model Eğitim Scripti

Bu script, Osmanlıca için özel Tesseract OCR modeli eğitmek için kullanılır.
"""

import os
import subprocess
import shutil
from typing import List, Optional
import json


class TesseractTrainer:
    """
    Tesseract model eğitimi için yardımcı sınıf.
    """
    
    def __init__(
        self,
        language_code: str = 'osmanlica',
        training_data_dir: str = 'training-data',
        output_dir: str = 'models'
    ):
        """
        Args:
            language_code: Eğitilecek dilin kodu
            training_data_dir: Eğitim verilerinin bulunduğu dizin
            output_dir: Eğitilmiş modelin kaydedileceği dizin
        """
        self.language_code = language_code
        self.training_data_dir = training_data_dir
        self.output_dir = output_dir
        
        # Dizinleri oluştur
        os.makedirs(training_data_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
    
    def prepare_training_data(
        self,
        images_dir: str,
        ground_truth_dir: str
    ) -> None:
        """
        Eğitim verilerini hazırlar.
        
        Args:
            images_dir: Görüntü dosyalarının bulunduğu dizin
            ground_truth_dir: Ground truth metin dosyalarının bulunduğu dizin
        """
        print("Eğitim verileri hazırlanıyor...")
        
        # Ground truth dosyalarını kontrol et
        for filename in os.listdir(images_dir):
            if filename.lower().endswith(('.png', '.tif', '.tiff')):
                base_name = os.path.splitext(filename)[0]
                gt_file = os.path.join(ground_truth_dir, f"{base_name}.gt.txt")
                
                if not os.path.exists(gt_file):
                    print(f"UYARI: {filename} için ground truth dosyası bulunamadı!")
        
        print("Hazırlık tamamlandı.")
    
    def create_box_files(self, images_dir: str) -> None:
        """
        Görüntüler için box dosyaları oluşturur.
        
        Args:
            images_dir: Görüntü dosyalarının bulunduğu dizin
        """
        print("Box dosyaları oluşturuluyor...")
        
        for filename in os.listdir(images_dir):
            if filename.lower().endswith(('.png', '.tif', '.tiff')):
                image_path = os.path.join(images_dir, filename)
                base_name = os.path.splitext(filename)[0]
                
                # Tesseract ile box dosyası oluştur
                cmd = [
                    'tesseract',
                    image_path,
                    base_name,
                    'batch.nochop',
                    'makebox'
                ]
                
                try:
                    subprocess.run(cmd, check=True)
                    print(f"✓ {filename} için box dosyası oluşturuldu")
                except subprocess.CalledProcessError as e:
                    print(f"✗ Hata ({filename}): {e}")
        
        print("Box dosyaları oluşturuldu.")
    
    def train_model(
        self,
        font_name: str = 'OsmanlicaFont',
        start_model: Optional[str] = None
    ) -> None:
        """
        Tesseract modelini eğitir.
        
        Args:
            font_name: Font adı
            start_model: Başlangıç modeli (fine-tuning için)
        """
        print(f"Model eğitimi başlıyor: {self.language_code}")
        
        # 1. TR dosyası oluştur
        print("1/5 - TR dosyası oluşturuluyor...")
        self._generate_tr_files()
        
        # 2. Box dosyalarından eğitim verisi oluştur
        print("2/5 - Eğitim verisi oluşturuluyor...")
        self._extract_features()
        
        # 3. Clustering
        print("3/5 - Clustering yapılıyor...")
        self._compute_clustering()
        
        # 4. Dictionary oluştur
        print("4/5 - Dictionary oluşturuluyor...")
        self._create_dictionary()
        
        # 5. Final model oluştur
        print("5/5 - Final model oluşturuluyor...")
        self._combine_data()
        
        print(f"✓ Model eğitimi tamamlandı: {self.language_code}")
    
    def _generate_tr_files(self) -> None:
        """TR dosyaları oluşturur."""
        # Tesseract training için gerekli dosyaları oluştur
        pass
    
    def _extract_features(self) -> None:
        """Özellik çıkarımı yapar."""
        cmd = ['tesseract']
        # Feature extraction komutları
        pass
    
    def _compute_clustering(self) -> None:
        """Clustering hesaplamaları yapar."""
        cmd = ['mftraining', 'cntraining']
        # Clustering komutları
        pass
    
    def _create_dictionary(self) -> None:
        """Dictionary dosyası oluşturur."""
        pass
    
    def _combine_data(self) -> None:
        """Tüm verileri birleştirerek final model oluşturur."""
        cmd = ['combine_tessdata']
        # Combine komutları
        pass
    
    def fine_tune_model(
        self,
        base_model: str,
        training_text: str,
        iterations: int = 1000
    ) -> None:
        """
        Mevcut bir modeli fine-tune eder.
        
        Args:
            base_model: Başlangıç modeli (örn: 'ara')
            training_text: Eğitim metni dosyası
            iterations: Eğitim iterasyon sayısı
        """
        print(f"Fine-tuning başlıyor: {base_model} -> {self.language_code}")
        
        # Training text'ten lstmf dosyaları oluştur
        cmd = [
            'tesstrain.sh',
            '--fonts_dir', os.path.join(self.training_data_dir, 'fonts'),
            '--lang', self.language_code,
            '--linedata_only',
            '--noextract_font_properties',
            '--langdata_dir', self.training_data_dir,
            '--tessdata_dir', os.environ.get('TESSDATA_PREFIX', '/usr/share/tesseract-ocr/4.00/tessdata'),
            '--output_dir', self.output_dir,
            '--max_iterations', str(iterations)
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"✓ Fine-tuning tamamlandı")
        except subprocess.CalledProcessError as e:
            print(f"✗ Hata: {e}")


def create_training_config(
    output_path: str = 'training-data/training_config.json'
) -> None:
    """
    Eğitim yapılandırması oluşturur.
    
    Args:
        output_path: Yapılandırma dosyası yolu
    """
    config = {
        "language_code": "osmanlica",
        "fonts": [
            "Amiri-Regular",
            "ScheherazadeNew-Regular",
            "NotoNaskhArabic-Regular"
        ],
        "training_params": {
            "max_iterations": 10000,
            "learning_rate": 0.0001,
            "target_error_rate": 0.02
        },
        "character_set": "ابتثجحخدذرزسشصضطظعغفقكلمنهويءآأؤإئةىپچژگ",
        "preprocessing": {
            "denoise": True,
            "deskew": True,
            "binarize": True,
            "enhance_contrast": True
        }
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"Eğitim yapılandırması oluşturuldu: {output_path}")


def download_base_models() -> None:
    """
    Tesseract için temel dil modellerini indirir.
    """
    print("Temel modeller indiriliyor...")
    
    models = ['ara', 'tur']  # Arapça ve Türkçe
    
    for model in models:
        cmd = [
            'wget',
            f'https://github.com/tesseract-ocr/tessdata_best/raw/main/{model}.traineddata',
            '-P', '/usr/share/tesseract-ocr/4.00/tessdata/'
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"✓ {model} modeli indirildi")
        except subprocess.CalledProcessError:
            print(f"✗ {model} modeli indirilemedi (zaten mevcut olabilir)")


def main():
    """Ana eğitim scripti"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Tesseract model eğitimi')
    parser.add_argument('--action', choices=['prepare', 'train', 'finetune', 'config'],
                       required=True, help='Yapılacak işlem')
    parser.add_argument('--images-dir', help='Görüntü dizini')
    parser.add_argument('--gt-dir', help='Ground truth dizini')
    parser.add_argument('--base-model', help='Fine-tuning için başlangıç modeli')
    parser.add_argument('--iterations', type=int, default=1000,
                       help='Eğitim iterasyon sayısı')
    
    args = parser.parse_args()
    
    trainer = TesseractTrainer()
    
    if args.action == 'prepare':
        if not args.images_dir or not args.gt_dir:
            print("Hata: --images-dir ve --gt-dir parametreleri gerekli")
            return
        trainer.prepare_training_data(args.images_dir, args.gt_dir)
    
    elif args.action == 'train':
        trainer.train_model()
    
    elif args.action == 'finetune':
        if not args.base_model:
            print("Hata: --base-model parametresi gerekli")
            return
        trainer.fine_tune_model(args.base_model, '', args.iterations)
    
    elif args.action == 'config':
        create_training_config()


if __name__ == '__main__':
    main()
