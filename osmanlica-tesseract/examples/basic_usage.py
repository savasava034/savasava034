#!/usr/bin/env python3
"""
Temel Kullanım Örneği

Bu dosya, Osmanlıca OCR'in temel kullanımını gösterir.
"""

import os
import sys

# Script dizinini path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.osmanlica_ocr import OsmanlicaOCR
from scripts.preprocess import preprocess_image


def ornek_1_basit_kullanim():
    """Örnek 1: Basit OCR kullanımı"""
    print("=== Örnek 1: Basit OCR Kullanımı ===\n")
    
    # OCR nesnesi oluştur
    ocr = OsmanlicaOCR()
    
    # Görüntüden metin çıkar
    image_path = "ornek-goruntu.jpg"
    
    if os.path.exists(image_path):
        text = ocr.extract_text(image_path)
        print(f"Tanınan Metin:\n{text}\n")
    else:
        print(f"Örnek görüntü bulunamadı: {image_path}\n")


def ornek_2_guven_skoru():
    """Örnek 2: Güven skoru ile OCR"""
    print("=== Örnek 2: Güven Skoru ile OCR ===\n")
    
    ocr = OsmanlicaOCR()
    image_path = "ornek-goruntu.jpg"
    
    if os.path.exists(image_path):
        text, confidence = ocr.extract_text(image_path, return_confidence=True)
        
        print(f"Tanınan Metin:\n{text}\n")
        print(f"Güven Skoru: {confidence:.2f}%\n")
        
        if confidence > 90:
            print("✓ Çok yüksek güven")
        elif confidence > 70:
            print("✓ Yüksek güven")
        else:
            print("⚠ Düşük güven - görüntü kalitesini kontrol edin")
    else:
        print(f"Örnek görüntü bulunamadı: {image_path}\n")


def ornek_3_on_isleme():
    """Örnek 3: Ön işleme ile OCR"""
    print("=== Örnek 3: Ön İşleme ile OCR ===\n")
    
    image_path = "ornek-goruntu.jpg"
    processed_path = "/tmp/processed.jpg"
    
    if os.path.exists(image_path):
        # Görüntüyü ön işle
        print("Görüntü ön işleniyor...")
        processed = preprocess_image(
            image_path,
            processed_path,
            denoise=True,
            deskew=True,
            binarize=True,
            enhance_contrast=True
        )
        
        print("✓ Ön işleme tamamlandı\n")
        
        # OCR uygula
        ocr = OsmanlicaOCR()
        text = ocr.extract_text(processed_path)
        
        print(f"Tanınan Metin:\n{text}\n")
    else:
        print(f"Örnek görüntü bulunamadı: {image_path}\n")


def ornek_4_kelime_konumlari():
    """Örnek 4: Kelime konumları ile OCR"""
    print("=== Örnek 4: Kelime Konumları ile OCR ===\n")
    
    ocr = OsmanlicaOCR()
    image_path = "ornek-goruntu.jpg"
    
    if os.path.exists(image_path):
        results = ocr.extract_text_with_boxes(image_path)
        
        print(f"Toplam {len(results)} kelime tanındı:\n")
        
        for i, result in enumerate(results[:10], 1):  # İlk 10 kelime
            print(f"{i}. '{result['text']}' - "
                  f"Konum: ({result['x']}, {result['y']}) - "
                  f"Güven: {result['confidence']:.1f}%")
        
        if len(results) > 10:
            print(f"\n... ve {len(results) - 10} kelime daha")
    else:
        print(f"Örnek görüntü bulunamadı: {image_path}\n")


def ornek_5_toplu_isleme():
    """Örnek 5: Toplu görüntü işleme"""
    print("=== Örnek 5: Toplu Görüntü İşleme ===\n")
    
    ocr = OsmanlicaOCR()
    images_dir = "test-images"
    output_dir = "output-texts"
    
    if os.path.exists(images_dir):
        print(f"'{images_dir}' dizinindeki görüntüler işleniyor...\n")
        
        results = ocr.batch_process(images_dir, output_dir)
        
        print(f"\n✓ {len(results)} görüntü işlendi")
        print(f"✓ Çıktılar '{output_dir}' dizinine kaydedildi\n")
        
        # Başarılı ve başarısız işlemleri göster
        successful = sum(1 for v in results.values() if v is not None)
        failed = len(results) - successful
        
        print(f"Başarılı: {successful}")
        print(f"Başarısız: {failed}")
    else:
        print(f"Test görüntü dizini bulunamadı: {images_dir}\n")


def ornek_6_ozel_model():
    """Örnek 6: Özel eğitilmiş model kullanımı"""
    print("=== Örnek 6: Özel Model Kullanımı ===\n")
    
    model_path = "../models/osmanlica.traineddata"
    
    if os.path.exists(model_path):
        # Özel model ile OCR oluştur
        ocr = OsmanlicaOCR(custom_model=model_path)
        
        image_path = "ornek-goruntu.jpg"
        
        if os.path.exists(image_path):
            text = ocr.extract_text(image_path)
            print(f"Özel model ile tanınan metin:\n{text}\n")
        else:
            print(f"Örnek görüntü bulunamadı: {image_path}\n")
    else:
        print(f"Özel model bulunamadı: {model_path}")
        print("Model eğitimi için 'train_tesseract.py' scriptini kullanın.\n")


def main():
    """Tüm örnekleri çalıştır"""
    print("\n" + "="*60)
    print("OSMANICA OCR - KULLANIM ÖRNEKLERİ")
    print("="*60 + "\n")
    
    # Hangi örnekleri çalıştırmak istediğinizi seçin
    ornekler = [
        ornek_1_basit_kullanim,
        ornek_2_guven_skoru,
        ornek_3_on_isleme,
        ornek_4_kelime_konumlari,
        ornek_5_toplu_isleme,
        ornek_6_ozel_model
    ]
    
    for ornek in ornekler:
        try:
            ornek()
        except Exception as e:
            print(f"Hata: {str(e)}\n")
        
        print("-" * 60 + "\n")


if __name__ == '__main__':
    main()
