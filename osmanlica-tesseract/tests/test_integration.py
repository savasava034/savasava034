#!/usr/bin/env python3
"""
Entegrasyon Testleri

Bu dosya, modüller arası etkileşimleri test eder.
"""

import unittest
import os
import sys
import tempfile
import shutil

# Modülleri import et
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.osmanlica_ocr import OsmanlicaOCR
from scripts.preprocess import preprocess_image
from scripts.evaluate import calculate_accuracy


class TestEndToEndPipeline(unittest.TestCase):
    """Uçtan uca pipeline testleri"""
    
    def setUp(self):
        """Her test öncesi çalışır"""
        self.test_data_dir = os.path.join(
            os.path.dirname(__file__), '..', 'sample-data'
        )
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Her test sonrası temizlik"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_preprocess_then_ocr(self):
        """Ön işleme + OCR pipeline testi"""
        sample_image = os.path.join(
            self.test_data_dir, 'images', 'sample001_besmele.png'
        )
        
        if not os.path.exists(sample_image):
            self.skipTest("Sample image not found")
        
        # 1. Ön işleme
        processed_path = os.path.join(self.temp_dir, 'processed.png')
        processed = preprocess_image(
            sample_image,
            processed_path,
            denoise=True,
            binarize=True,
            enhance_contrast=True
        )
        
        self.assertIsNotNone(processed)
        self.assertTrue(os.path.exists(processed_path))
        
        # 2. OCR
        ocr = OsmanlicaOCR()
        text = ocr.extract_text(processed_path)
        
        self.assertIsNotNone(text)
        self.assertIsInstance(text, str)
    
    def test_ocr_then_evaluate(self):
        """OCR + Değerlendirme pipeline testi"""
        sample_image = os.path.join(
            self.test_data_dir, 'images', 'sample001_besmele.png'
        )
        gt_file = os.path.join(
            self.test_data_dir, 'ground-truth', 'sample001_besmele.txt'
        )
        
        if not os.path.exists(sample_image) or not os.path.exists(gt_file):
            self.skipTest("Sample files not found")
        
        # 1. OCR
        ocr = OsmanlicaOCR()
        extracted_text = ocr.extract_text(sample_image)
        
        # 2. Ground truth oku
        with open(gt_file, 'r', encoding='utf-8') as f:
            ground_truth = f.read().strip()
        
        # 3. Değerlendirme
        accuracy = calculate_accuracy(extracted_text, ground_truth)
        
        self.assertIsInstance(accuracy, dict)
        self.assertIn('char_accuracy', accuracy)
        self.assertIn('word_accuracy', accuracy)
        self.assertIn('cer', accuracy)
    
    def test_full_pipeline_all_samples(self):
        """Tüm örneklerle tam pipeline testi"""
        images_dir = os.path.join(self.test_data_dir, 'images')
        gt_dir = os.path.join(self.test_data_dir, 'ground-truth')
        
        if not os.path.exists(images_dir) or not os.path.exists(gt_dir):
            self.skipTest("Sample directories not found")
        
        ocr = OsmanlicaOCR()
        results = []
        
        for image_file in os.listdir(images_dir):
            if image_file.endswith('.png'):
                image_path = os.path.join(images_dir, image_file)
                base_name = os.path.splitext(image_file)[0]
                gt_file = os.path.join(gt_dir, f"{base_name}.txt")
                
                if os.path.exists(gt_file):
                    # OCR
                    text = ocr.extract_text(image_path)
                    
                    # Ground truth
                    with open(gt_file, 'r', encoding='utf-8') as f:
                        gt_text = f.read().strip()
                    
                    # Değerlendirme
                    accuracy = calculate_accuracy(text, gt_text)
                    
                    results.append({
                        'file': image_file,
                        'accuracy': accuracy
                    })
        
        # En az bir sonuç olmalı
        self.assertGreater(len(results), 0)
        
        # Ortalama doğruluk hesapla
        avg_char_acc = sum(r['accuracy']['char_accuracy'] for r in results) / len(results)
        
        # En az %20 doğruluk bekliyoruz (çok düşük eşik)
        self.assertGreater(avg_char_acc, 20.0)


class TestPreprocessingIntegration(unittest.TestCase):
    """Ön işleme entegrasyon testleri"""
    
    def setUp(self):
        """Her test öncesi çalışır"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Her test sonrası temizlik"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_multiple_preprocessing_methods(self):
        """Çoklu ön işleme yöntemleri testi"""
        sample_image = os.path.join(
            os.path.dirname(__file__), '..', 'sample-data',
            'images', 'sample001_besmele.png'
        )
        
        if not os.path.exists(sample_image):
            self.skipTest("Sample image not found")
        
        methods = [
            {'denoise': True, 'binarize': False},
            {'denoise': False, 'binarize': True},
            {'denoise': True, 'binarize': True},
            {'enhance_contrast': True, 'sharpen': True}
        ]
        
        for i, method_params in enumerate(methods):
            output_path = os.path.join(self.temp_dir, f'processed_{i}.png')
            
            processed = preprocess_image(
                sample_image,
                output_path,
                **method_params
            )
            
            self.assertIsNotNone(processed)
            self.assertTrue(os.path.exists(output_path))


class TestBatchProcessing(unittest.TestCase):
    """Toplu işleme entegrasyon testleri"""
    
    def test_batch_ocr_with_preprocessing(self):
        """Ön işlemeli toplu OCR testi"""
        test_data_dir = os.path.join(
            os.path.dirname(__file__), '..', 'sample-data', 'images'
        )
        
        if not os.path.exists(test_data_dir):
            self.skipTest("Sample directory not found")
        
        ocr = OsmanlicaOCR(preprocess=True)
        results = ocr.batch_process(test_data_dir)
        
        self.assertIsInstance(results, list)
        
        # Her sonuç bir dict olmalı
        for result in results:
            self.assertIn('filename', result)
            self.assertIn('text', result)


class TestAccuracyTracking(unittest.TestCase):
    """Doğruluk takip testleri"""
    
    def test_accuracy_improvement_tracking(self):
        """Doğruluk iyileştirme takibi testi"""
        sample_image = os.path.join(
            os.path.dirname(__file__), '..', 'sample-data',
            'images', 'sample001_besmele.png'
        )
        gt_file = os.path.join(
            os.path.dirname(__file__), '..', 'sample-data',
            'ground-truth', 'sample001_besmele.txt'
        )
        
        if not os.path.exists(sample_image) or not os.path.exists(gt_file):
            self.skipTest("Sample files not found")
        
        with open(gt_file, 'r', encoding='utf-8') as f:
            ground_truth = f.read().strip()
        
        # Farklı konfigürasyonlarla OCR
        configs = [
            {'preprocess': False},
            {'preprocess': True}
        ]
        
        accuracies = []
        
        for config in configs:
            ocr = OsmanlicaOCR(**config)
            text = ocr.extract_text(sample_image)
            acc = calculate_accuracy(text, ground_truth)
            accuracies.append(acc['char_accuracy'])
        
        # En az bir config çalışmalı
        self.assertGreater(len(accuracies), 0)


if __name__ == '__main__':
    unittest.main()
