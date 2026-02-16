#!/usr/bin/env python3
"""
Test Çalıştırıcı

Tüm testleri çalıştırır ve rapor oluşturur.
"""

import sys
import os
import unittest

def run_all_tests():
    """Tüm testleri çalıştır"""
    
    # Test dizinini path'e ekle
    test_dir = os.path.join(os.path.dirname(__file__), 'tests')
    sys.path.insert(0, test_dir)
    
    print("="*60)
    print("  OSMANICA TESSERACT OCR - TEST SÜİTİ")
    print("="*60)
    print()
    
    # Test loader oluştur
    loader = unittest.TestLoader()
    
    # Testleri bul ve yükle
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    # Test runner oluştur
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Testleri çalıştır
    result = runner.run(suite)
    
    print()
    print("="*60)
    print("  TEST SONUÇLARI")
    print("="*60)
    print(f"Çalıştırılan: {result.testsRun}")
    print(f"Başarılı: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Başarısız: {len(result.failures)}")
    print(f"Hata: {len(result.errors)}")
    print("="*60)
    
    # Başarısızsa hata kodu dön
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
