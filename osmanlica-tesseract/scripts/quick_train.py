#!/usr/bin/env python3
"""
Hızlı Eğitim Scripti

Bu script, örnek verilerle hızlı bir eğitim yapmak için kullanılır.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
import json
from datetime import datetime

# Modülleri import et
from osmanlica_ocr import OsmanlicaOCR
from preprocess import preprocess_image
from evaluate import calculate_accuracy, evaluate_model


def check_tesseract_installed():
    """Tesseract'ın kurulu olup olmadığını kontrol eder."""
    try:
        result = subprocess.run(
            ['tesseract', '--version'],
            capture_output=True,
            text=True
        )
        print(f"✓ Tesseract kurulu: {result.stdout.split()[1]}")
        return True
    except FileNotFoundError:
        print("✗ Tesseract kurulu değil!")
        print("  Kurulum için: sudo apt-get install tesseract-ocr")
        return False


def download_arabic_model():
    """Arapça temel modelini indirir."""
    print("\n=== Arapça Model İndiriliyor ===")
    
    tessdata_dir = os.environ.get('TESSDATA_PREFIX', '/usr/share/tesseract-ocr/4.00/tessdata')
    ara_model = os.path.join(tessdata_dir, 'ara.traineddata')
    
    if os.path.exists(ara_model):
        print(f"✓ Arapça model zaten mevcut: {ara_model}")
        return True
    
    print(f"Arapça model indiriliyor...")
    cmd = [
        'wget',
        'https://github.com/tesseract-ocr/tessdata_best/raw/main/ara.traineddata',
        '-O', ara_model
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✓ Arapça model indirildi: {ara_model}")
        return True
    except Exception as e:
        print(f"✗ Model indirme hatası: {e}")
        return False


def preprocess_training_data(input_dir, output_dir):
    """Eğitim verilerini ön işlemeden geçirir."""
    print("\n=== Eğitim Verileri Ön İşleme ===")
    
    os.makedirs(output_dir, exist_ok=True)
    
    processed_count = 0
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.tif', '.tiff')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            try:
                preprocess_image(
                    input_path,
                    output_path,
                    denoise=True,
                    deskew=True,
                    binarize=True,
                    enhance_contrast=True
                )
                processed_count += 1
                print(f"  ✓ {filename}")
            except Exception as e:
                print(f"  ✗ {filename}: {e}")
    
    print(f"\n✓ {processed_count} görüntü işlendi")
    return processed_count


def evaluate_on_samples(lang='ara'):
    """Örnek veriler üzerinde değerlendirme yapar."""
    print(f"\n=== Değerlendirme ({lang} modeli) ===")
    
    images_dir = 'sample-data/images'
    gt_dir = 'sample-data/ground-truth'
    
    if not os.path.exists(images_dir) or not os.path.exists(gt_dir):
        print("✗ Örnek veriler bulunamadı!")
        return None
    
    ocr = OsmanlicaOCR(lang=lang, preprocess=True)
    
    results = []
    
    for image_file in sorted(os.listdir(images_dir)):
        if image_file.endswith('.png'):
            image_path = os.path.join(images_dir, image_file)
            base_name = os.path.splitext(image_file)[0]
            gt_file = os.path.join(gt_dir, f"{base_name}.txt")
            
            if os.path.exists(gt_file):
                # OCR
                extracted_text = ocr.extract_text(image_path)
                
                # Ground truth
                with open(gt_file, 'r', encoding='utf-8') as f:
                    ground_truth = f.read().strip()
                
                # Değerlendirme
                accuracy = calculate_accuracy(extracted_text, ground_truth)
                
                results.append({
                    'file': image_file,
                    'extracted': extracted_text,
                    'ground_truth': ground_truth,
                    'accuracy': accuracy
                })
                
                print(f"\n{image_file}:")
                print(f"  Çıkarılan: {extracted_text[:50]}...")
                print(f"  Gerçek:    {ground_truth[:50]}...")
                print(f"  Karakter Doğruluğu: {accuracy['char_accuracy']:.2f}%")
                print(f"  Kelime Doğruluğu:   {accuracy['word_accuracy']:.2f}%")
    
    if results:
        avg_char_acc = sum(r['accuracy']['char_accuracy'] for r in results) / len(results)
        avg_word_acc = sum(r['accuracy']['word_accuracy'] for r in results) / len(results)
        avg_cer = sum(r['accuracy']['cer'] for r in results) / len(results)
        
        print(f"\n=== ORTALAMA SONUÇLAR ===")
        print(f"Karakter Doğruluğu: {avg_char_acc:.2f}%")
        print(f"Kelime Doğruluğu:   {avg_word_acc:.2f}%")
        print(f"CER (Character Error Rate): {avg_cer:.2f}%")
        
        return {
            'results': results,
            'averages': {
                'char_accuracy': avg_char_acc,
                'word_accuracy': avg_word_acc,
                'cer': avg_cer
            }
        }
    
    return None


def save_results(results, output_file='training_results.json'):
    """Sonuçları JSON dosyasına kaydeder."""
    timestamp = datetime.now().isoformat()
    
    output = {
        'timestamp': timestamp,
        'results': results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Sonuçlar kaydedildi: {output_file}")


def compare_models():
    """Farklı modelleri karşılaştırır."""
    print("\n=== MODEL KARŞILAŞTIRMA ===")
    
    models = ['ara']  # Şimdilik sadece Arapça
    
    all_results = {}
    
    for model in models:
        print(f"\n--- {model} modeli test ediliyor ---")
        results = evaluate_on_samples(lang=model)
        if results:
            all_results[model] = results['averages']
    
    if all_results:
        print("\n=== KARŞILAŞTIRMA SONUÇLARI ===")
        for model, avg in all_results.items():
            print(f"\n{model} modeli:")
            print(f"  Karakter: {avg['char_accuracy']:.2f}%")
            print(f"  Kelime:   {avg['word_accuracy']:.2f}%")
            print(f"  CER:      {avg['cer']:.2f}%")
    
    return all_results


def main():
    parser = argparse.ArgumentParser(description='Hızlı Tesseract eğitim ve test scripti')
    parser.add_argument(
        '--action',
        choices=['check', 'download', 'preprocess', 'evaluate', 'compare', 'all'],
        default='all',
        help='Yapılacak işlem'
    )
    parser.add_argument(
        '--lang',
        default='ara',
        help='Kullanılacak dil modeli'
    )
    parser.add_argument(
        '--input-dir',
        default='sample-data/images',
        help='Girdi görüntü dizini'
    )
    parser.add_argument(
        '--output-dir',
        default='sample-data/processed',
        help='İşlenmiş görüntü dizini'
    )
    parser.add_argument(
        '--save-results',
        action='store_true',
        help='Sonuçları JSON dosyasına kaydet'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("OSMANICA TESSERACT - HIZLI EĞİTİM VE TEST")
    print("=" * 60)
    
    results = None
    
    if args.action in ['check', 'all']:
        if not check_tesseract_installed():
            return 1
    
    if args.action in ['download', 'all']:
        if not download_arabic_model():
            print("\n⚠️  Model indirme başarısız, ancak devam ediliyor...")
    
    if args.action in ['preprocess', 'all']:
        preprocess_training_data(args.input_dir, args.output_dir)
    
    if args.action in ['evaluate', 'all']:
        results = evaluate_on_samples(lang=args.lang)
    
    if args.action == 'compare':
        results = compare_models()
    
    if results and args.save_results:
        save_results(results)
    
    print("\n" + "=" * 60)
    print("İŞLEM TAMAMLANDI")
    print("=" * 60)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
