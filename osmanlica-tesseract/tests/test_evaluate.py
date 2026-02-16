#!/usr/bin/env python3
"""
Değerlendirme Modülü Testleri

Bu dosya, evaluate.py modülündeki fonksiyonları test eder.
"""

import unittest
import os
import sys

# Modülü import et
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.evaluate import (
    calculate_accuracy,
    calculate_levenshtein,
    calculate_wer
)


class TestAccuracyCalculations(unittest.TestCase):
    """Doğruluk hesaplama fonksiyonları testleri"""
    
    def test_calculate_accuracy_perfect_match(self):
        """Tam eşleşme testi"""
        text = "بسم الله الرحمن الرحیم"
        accuracy = calculate_accuracy(text, text)
        
        self.assertEqual(accuracy['char_accuracy'], 100.0)
        self.assertEqual(accuracy['word_accuracy'], 100.0)
        self.assertEqual(accuracy['levenshtein_distance'], 0)
        self.assertEqual(accuracy['cer'], 0.0)
    
    def test_calculate_accuracy_partial_match(self):
        """Kısmi eşleşme testi"""
        predicted = "بسم الله"
        ground_truth = "بسم الله الرحمن"
        
        accuracy = calculate_accuracy(predicted, ground_truth)
        
        # Tam eşleşme değil
        self.assertLess(accuracy['char_accuracy'], 100.0)
        self.assertGreater(accuracy['char_accuracy'], 0.0)
    
    def test_calculate_accuracy_no_match(self):
        """Hiç eşleşme yok testi"""
        predicted = "test"
        ground_truth = "الله"
        
        accuracy = calculate_accuracy(predicted, ground_truth)
        
        # Düşük doğruluk bekleniyor
        self.assertLess(accuracy['char_accuracy'], 50.0)
    
    def test_calculate_levenshtein_same_strings(self):
        """Levenshtein - aynı stringler"""
        distance = calculate_levenshtein("hello", "hello")
        self.assertEqual(distance, 0)
    
    def test_calculate_levenshtein_different_strings(self):
        """Levenshtein - farklı stringler"""
        distance = calculate_levenshtein("kitten", "sitting")
        self.assertEqual(distance, 3)  # 3 değişiklik gerekir
    
    def test_calculate_levenshtein_empty_string(self):
        """Levenshtein - boş string"""
        distance = calculate_levenshtein("", "hello")
        self.assertEqual(distance, 5)
        
        distance = calculate_levenshtein("hello", "")
        self.assertEqual(distance, 5)
    
    def test_calculate_wer_same_words(self):
        """WER - aynı kelimeler"""
        words1 = ["hello", "world"]
        words2 = ["hello", "world"]
        
        wer = calculate_wer(words1, words2)
        self.assertEqual(wer, 0.0)
    
    def test_calculate_wer_different_words(self):
        """WER - farklı kelimeler"""
        predicted = ["hello", "world"]
        ground_truth = ["hello", "there", "world"]
        
        wer = calculate_wer(predicted, ground_truth)
        self.assertGreater(wer, 0.0)
    
    def test_calculate_wer_empty_list(self):
        """WER - boş liste"""
        wer = calculate_wer([], [])
        self.assertEqual(wer, 0.0)


class TestEdgeCases(unittest.TestCase):
    """Sınır durumları testleri"""
    
    def test_empty_strings(self):
        """Boş stringler testi"""
        accuracy = calculate_accuracy("", "")
        
        # Boş stringler için doğruluk kontrolü
        self.assertIsInstance(accuracy, dict)
        self.assertIn('char_accuracy', accuracy)
    
    def test_unicode_arabic(self):
        """Unicode Arapça karakterler testi"""
        arabic1 = "الله"
        arabic2 = "الله"
        
        distance = calculate_levenshtein(arabic1, arabic2)
        self.assertEqual(distance, 0)
    
    def test_mixed_languages(self):
        """Karışık dil testi"""
        text1 = "Hello الله World"
        text2 = "Hello الله World"
        
        accuracy = calculate_accuracy(text1, text2)
        self.assertEqual(accuracy['char_accuracy'], 100.0)


if __name__ == '__main__':
    unittest.main()
