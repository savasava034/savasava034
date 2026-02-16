#!/usr/bin/env python3
"""
Model Değerlendirme Scripti

Bu script, eğitilmiş Tesseract modelinin doğruluğunu değerlendirir.
"""

import os
import sys
import json
from typing import Dict, List, Tuple, Optional
import difflib
from pathlib import Path

# OCR modülünü import et
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.osmanlica_ocr import OsmanlicaOCR


def calculate_accuracy(predicted: str, ground_truth: str) -> Dict[str, float]:
    """
    OCR sonuçlarının doğruluğunu hesaplar.
    
    Args:
        predicted: OCR tarafından tanınan metin
        ground_truth: Gerçek metin
        
    Returns:
        Doğruluk metrikleri
    """
    # Karakter seviyesi doğruluk
    pred_chars = list(predicted.replace(' ', ''))
    gt_chars = list(ground_truth.replace(' ', ''))
    
    matcher = difflib.SequenceMatcher(None, pred_chars, gt_chars)
    char_accuracy = matcher.ratio() * 100
    
    # Kelime seviyesi doğruluk
    pred_words = predicted.split()
    gt_words = ground_truth.split()
    
    word_matcher = difflib.SequenceMatcher(None, pred_words, gt_words)
    word_accuracy = word_matcher.ratio() * 100
    
    # Levenshtein mesafesi
    levenshtein_distance = calculate_levenshtein(predicted, ground_truth)
    
    # Character Error Rate (CER)
    cer = (levenshtein_distance / len(ground_truth)) * 100 if len(ground_truth) > 0 else 0
    
    # Word Error Rate (WER)
    wer = calculate_wer(pred_words, gt_words)
    
    return {
        'char_accuracy': char_accuracy,
        'word_accuracy': word_accuracy,
        'levenshtein_distance': levenshtein_distance,
        'cer': cer,
        'wer': wer
    }


def calculate_levenshtein(s1: str, s2: str) -> int:
    """
    İki string arasındaki Levenshtein mesafesini hesaplar.
    
    Args:
        s1: İlk string
        s2: İkinci string
        
    Returns:
        Levenshtein mesafesi
    """
    if len(s1) < len(s2):
        return calculate_levenshtein(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # j+1 yerine j kullan çünkü current_row j'den başlıyor
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def calculate_wer(predicted_words: List[str], ground_truth_words: List[str]) -> float:
    """
    Word Error Rate (WER) hesaplar.
    
    Args:
        predicted_words: Tahmin edilen kelimeler
        ground_truth_words: Gerçek kelimeler
        
    Returns:
        WER yüzdesi
    """
    if len(ground_truth_words) == 0:
        return 0.0
    
    # Edit distance hesapla
    d = [[0] * (len(ground_truth_words) + 1) for _ in range(len(predicted_words) + 1)]
    
    for i in range(len(predicted_words) + 1):
        d[i][0] = i
    for j in range(len(ground_truth_words) + 1):
        d[0][j] = j
    
    for i in range(1, len(predicted_words) + 1):
        for j in range(1, len(ground_truth_words) + 1):
            if predicted_words[i-1] == ground_truth_words[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = min(
                    d[i-1][j] + 1,    # deletion
                    d[i][j-1] + 1,    # insertion
                    d[i-1][j-1] + 1   # substitution
                )
    
    wer = (d[len(predicted_words)][len(ground_truth_words)] / len(ground_truth_words)) * 100
    return wer


def evaluate_model(
    test_dir: str,
    ground_truth_dir: str,
    model_path: Optional[str] = None
) -> Dict[str, any]:
    """
    Modeli test seti üzerinde değerlendirir.
    
    Args:
        test_dir: Test görüntülerinin bulunduğu dizin
        ground_truth_dir: Ground truth metinlerin bulunduğu dizin
        model_path: Özel model yolu (opsiyonel)
        
    Returns:
        Değerlendirme sonuçları
    """
    # OCR nesnesi oluştur
    if model_path:
        ocr = OsmanlicaOCR(custom_model=model_path)
    else:
        ocr = OsmanlicaOCR()
    
    results = []
    
    # Test görüntülerini işle
    for filename in os.listdir(test_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff', '.bmp')):
            image_path = os.path.join(test_dir, filename)
            
            # Ground truth dosyasını bul
            base_name = os.path.splitext(filename)[0]
            gt_path = os.path.join(ground_truth_dir, f"{base_name}.txt")
            
            if not os.path.exists(gt_path):
                print(f"UYARI: {filename} için ground truth bulunamadı, atlanıyor...")
                continue
            
            # Ground truth'u oku
            with open(gt_path, 'r', encoding='utf-8') as f:
                ground_truth = f.read().strip()
            
            # OCR uygula
            try:
                predicted, confidence = ocr.extract_text(image_path, return_confidence=True)
                
                # Doğruluğu hesapla
                accuracy = calculate_accuracy(predicted, ground_truth)
                accuracy['confidence'] = confidence
                accuracy['filename'] = filename
                
                results.append(accuracy)
                
                print(f"✓ {filename}: Char={accuracy['char_accuracy']:.2f}%, "
                      f"Word={accuracy['word_accuracy']:.2f}%, "
                      f"Conf={confidence:.2f}%")
                
            except Exception as e:
                print(f"✗ Hata ({filename}): {str(e)}")
    
    # Ortalama metrikleri hesapla
    if results:
        avg_metrics = {
            'avg_char_accuracy': sum(r['char_accuracy'] for r in results) / len(results),
            'avg_word_accuracy': sum(r['word_accuracy'] for r in results) / len(results),
            'avg_cer': sum(r['cer'] for r in results) / len(results),
            'avg_wer': sum(r['wer'] for r in results) / len(results),
            'avg_confidence': sum(r['confidence'] for r in results) / len(results),
            'total_samples': len(results),
            'individual_results': results
        }
    else:
        avg_metrics = {}
    
    return avg_metrics


def print_evaluation_report(metrics: Dict[str, any]) -> None:
    """
    Değerlendirme raporunu ekrana yazdırır.
    
    Args:
        metrics: Değerlendirme metrikleri
    """
    print("\n" + "="*60)
    print("MODEL DEĞERLENDIRME RAPORU")
    print("="*60)
    
    if not metrics:
        print("Değerlendirme sonucu bulunamadı!")
        return
    
    print(f"\nToplam Test Örneği: {metrics['total_samples']}")
    print(f"\nOrtalama Karakter Doğruluğu: {metrics['avg_char_accuracy']:.2f}%")
    print(f"Ortalama Kelime Doğruluğu: {metrics['avg_word_accuracy']:.2f}%")
    print(f"Ortalama CER (Character Error Rate): {metrics['avg_cer']:.2f}%")
    print(f"Ortalama WER (Word Error Rate): {metrics['avg_wer']:.2f}%")
    print(f"Ortalama Güven Skoru: {metrics['avg_confidence']:.2f}%")
    
    # En iyi ve en kötü sonuçlar
    if metrics['individual_results']:
        best = max(metrics['individual_results'], key=lambda x: x['char_accuracy'])
        worst = min(metrics['individual_results'], key=lambda x: x['char_accuracy'])
        
        print(f"\nEn İyi Sonuç: {best['filename']} "
              f"(Char: {best['char_accuracy']:.2f}%)")
        print(f"En Kötü Sonuç: {worst['filename']} "
              f"(Char: {worst['char_accuracy']:.2f}%)")
    
    print("\n" + "="*60)


def save_evaluation_report(
    metrics: Dict[str, any],
    output_path: str = 'evaluation_report.json'
) -> None:
    """
    Değerlendirme raporunu JSON dosyasına kaydeder.
    
    Args:
        metrics: Değerlendirme metrikleri
        output_path: Çıkış dosya yolu
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    
    print(f"\nRapor kaydedildi: {output_path}")


def main():
    """Ana değerlendirme scripti"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Tesseract model değerlendirmesi')
    parser.add_argument('--test-dir', required=True,
                       help='Test görüntülerinin bulunduğu dizin')
    parser.add_argument('--gt-dir', required=True,
                       help='Ground truth metinlerin bulunduğu dizin')
    parser.add_argument('--model', help='Değerlendirilecek model yolu')
    parser.add_argument('--output', default='evaluation_report.json',
                       help='Çıkış rapor dosyası')
    
    args = parser.parse_args()
    
    # Modeli değerlendir
    print(f"Model değerlendiriliyor...")
    metrics = evaluate_model(args.test_dir, args.gt_dir, args.model)
    
    # Raporu yazdır
    print_evaluation_report(metrics)
    
    # Raporu kaydet
    save_evaluation_report(metrics, args.output)


if __name__ == '__main__':
    main()
