#!/usr/bin/env python3
"""
OCR Modülü Testleri

Bu dosya, osmanlica_ocr.py modülündeki fonksiyonları test eder.
"""

import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Modülü import et
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.osmanlica_ocr import OsmanlicaOCR


class TestOCRBasics(unittest.TestCase):
    """OCR temel fonksiyonları testleri"""
    
    def setUp(self):
        """Her test öncesi çalışır"""
        self.ocr = OsmanlicaOCR()
        self.test_data_dir = os.path.join(
            os.path.dirname(__file__), '..', 'sample-data'
        )
    
    def test_ocr_initialization(self):
        """OCR nesnesinin başlatılması testi"""
        self.assertIsNotNone(self.ocr)
        self.assertTrue(hasattr(self.ocr, 'extract_text'))
    
    def test_extract_text_from_sample(self):
        """Örnek görüntüden metin çıkarma testi"""
        sample_image = os.path.join(
            self.test_data_dir, 'images', 'sample001_besmele.png'
        )
        
        if os.path.exists(sample_image):
            text = self.ocr.extract_text(sample_image)
            
            self.assertIsNotNone(text)
            self.assertIsInstance(text, str)
            # En az bir karakter bekliyoruz
            self.assertGreater(len(text), 0)
    
    def test_extract_text_confidence(self):
        """OCR güven skoru testi"""
        sample_image = os.path.join(
            self.test_data_dir, 'images', 'sample001_besmele.png'
        )
        
        if os.path.exists(sample_image):
            text, confidence = self.ocr.extract_text_with_confidence(sample_image)
            
            self.assertIsInstance(confidence, (int, float))
            self.assertGreaterEqual(confidence, 0)
            self.assertLessEqual(confidence, 100)
    
    def test_extract_text_invalid_path(self):
        """Geçersiz dosya yolu testi"""
        with self.assertRaises((FileNotFoundError, Exception)):
            self.ocr.extract_text('/non/existent/path.png')
    
    def test_multiple_languages(self):
        """Çoklu dil desteği testi"""
        ocr_ara = OsmanlicaOCR(lang='ara')
        self.assertEqual(ocr_ara.lang, 'ara')
        
        ocr_tur = OsmanlicaOCR(lang='tur')
        self.assertEqual(ocr_tur.lang, 'tur')


class TestOCRPreprocessing(unittest.TestCase):
    """OCR ön işleme testleri"""
    
    def setUp(self):
        """Her test öncesi çalışır"""
        self.ocr = OsmanlicaOCR(preprocess=True)
    
    def test_with_preprocessing(self):
        """Ön işleme ile OCR testi"""
        sample_image = os.path.join(
            os.path.dirname(__file__), '..', 'sample-data', 
            'images', 'sample001_besmele.png'
        )
        
        if os.path.exists(sample_image):
            text = self.ocr.extract_text(sample_image)
            self.assertIsNotNone(text)
    
    def test_without_preprocessing(self):
        """Ön işleme olmadan OCR testi"""
        ocr_no_preproc = OsmanlicaOCR(preprocess=False)
        
        sample_image = os.path.join(
            os.path.dirname(__file__), '..', 'sample-data', 
            'images', 'sample001_besmele.png'
        )
        
        if os.path.exists(sample_image):
            text = ocr_no_preproc.extract_text(sample_image)
            self.assertIsNotNone(text)


class TestBatchProcessing(unittest.TestCase):
    """Toplu işleme testleri"""
    
    def setUp(self):
        """Her test öncesi çalışır"""
        self.ocr = OsmanlicaOCR()
        self.test_data_dir = os.path.join(
            os.path.dirname(__file__), '..', 'sample-data', 'images'
        )
    
    def test_batch_process_directory(self):
        """Dizin toplu işleme testi"""
        if os.path.exists(self.test_data_dir):
            results = self.ocr.batch_process(self.test_data_dir)
            
            self.assertIsInstance(results, list)
            # En az bir sonuç bekliyoruz
            if len(results) > 0:
                self.assertIn('filename', results[0])
                self.assertIn('text', results[0])
    
    def test_batch_process_empty_dir(self):
        """Boş dizin toplu işleme testi"""
        with tempfile.TemporaryDirectory() as tmpdir:
            results = self.ocr.batch_process(tmpdir)
            self.assertEqual(len(results), 0)


class TestAccuracyComparison(unittest.TestCase):
    """Doğruluk karşılaştırma testleri"""
    
    def setUp(self):
        """Her test öncesi çalışır"""
        self.ocr = OsmanlicaOCR()
        self.test_data_dir = os.path.join(
            os.path.dirname(__file__), '..', 'sample-data'
        )
    
    def test_compare_with_ground_truth(self):
        """Ground truth ile karşılaştırma testi"""
        sample_image = os.path.join(
            self.test_data_dir, 'images', 'sample001_besmele.png'
        )
        gt_file = os.path.join(
            self.test_data_dir, 'ground-truth', 'sample001_besmele.txt'
        )
        
        if os.path.exists(sample_image) and os.path.exists(gt_file):
            extracted_text = self.ocr.extract_text(sample_image)
            
            with open(gt_file, 'r', encoding='utf-8') as f:
                ground_truth = f.read().strip()
            
            # Metinlerin benzerliğini kontrol et
            self.assertIsNotNone(extracted_text)
            self.assertIsNotNone(ground_truth)
            
            # Basit benzerlik kontrolü
            similarity = len(set(extracted_text) & set(ground_truth)) / max(
                len(set(extracted_text)), len(set(ground_truth))
            ) * 100 if extracted_text and ground_truth else 0
            
            # En az %20 benzerlik bekliyoruz (çok düşük bir eşik)
            self.assertGreater(similarity, 20.0)


class TestEdgeCases(unittest.TestCase):
    """Sınır durumları testleri"""
    
    def setUp(self):
        """Her test öncesi çalışır"""
        self.ocr = OsmanlicaOCR()
    
    def test_very_small_image(self):
        """Çok küçük görüntü testi"""
        # Bu test için geçici çok küçük bir görüntü oluşturulmalı
        # Şimdilik atlayalım
        pass
    
    def test_corrupted_image(self):
        """Bozuk görüntü dosyası testi"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp.write(b'not an image')
            tmp_path = tmp.name
        
        try:
            with self.assertRaises(Exception):
                self.ocr.extract_text(tmp_path)
        finally:
            os.unlink(tmp_path)
    
    def test_empty_image(self):
        """Boş beyaz görüntü testi"""
        # Bu test için geçici boş bir görüntü oluşturulmalı
        pass


if __name__ == '__main__':
    unittest.main()
