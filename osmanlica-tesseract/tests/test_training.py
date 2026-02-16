#!/usr/bin/env python3
"""
Eğitim Modülü Testleri

Bu dosya, train_tesseract.py modülündeki fonksiyonları test eder.
"""

import unittest
import os
import sys
import tempfile
import json

# Modülü import et
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.train_tesseract import (
    TesseractTrainer,
    create_training_config
)


class TestTesseractTrainer(unittest.TestCase):
    """TesseractTrainer sınıfı testleri"""
    
    def setUp(self):
        """Her test öncesi çalışır"""
        self.temp_dir = tempfile.mkdtemp()
        self.trainer = TesseractTrainer(
            language_code='test_lang',
            training_data_dir=os.path.join(self.temp_dir, 'training'),
            output_dir=os.path.join(self.temp_dir, 'output')
        )
    
    def tearDown(self):
        """Her test sonrası temizlik"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_trainer_initialization(self):
        """Trainer başlatma testi"""
        self.assertEqual(self.trainer.language_code, 'test_lang')
        self.assertTrue(os.path.exists(self.trainer.training_data_dir))
        self.assertTrue(os.path.exists(self.trainer.output_dir))
    
    def test_prepare_training_data(self):
        """Eğitim verisi hazırlama testi"""
        images_dir = os.path.join(self.temp_dir, 'images')
        gt_dir = os.path.join(self.temp_dir, 'gt')
        
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(gt_dir, exist_ok=True)
        
        # Test dosyası oluştur
        test_image = os.path.join(images_dir, 'test.png')
        open(test_image, 'a').close()
        
        # Fonksiyon çağrısı hata vermemeli
        try:
            self.trainer.prepare_training_data(images_dir, gt_dir)
        except Exception as e:
            self.fail(f"prepare_training_data failed: {e}")


class TestTrainingConfig(unittest.TestCase):
    """Eğitim yapılandırması testleri"""
    
    def test_create_training_config(self):
        """Yapılandırma dosyası oluşturma testi"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            config_path = tmp.name
        
        try:
            create_training_config(config_path)
            
            # Dosyanın oluşturulduğunu kontrol et
            self.assertTrue(os.path.exists(config_path))
            
            # İçeriği kontrol et
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self.assertIn('language_code', config)
            self.assertIn('training_params', config)
            self.assertIn('character_set', config)
            
            # Parametre kontrolü
            self.assertEqual(config['language_code'], 'osmanlica')
            self.assertIn('max_iterations', config['training_params'])
            
        finally:
            if os.path.exists(config_path):
                os.unlink(config_path)
    
    def test_config_structure(self):
        """Yapılandırma yapısı testi"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            config_path = tmp.name
        
        try:
            create_training_config(config_path)
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Gerekli alanların varlığını kontrol et
            required_keys = [
                'language_code',
                'fonts',
                'training_params',
                'character_set',
                'preprocessing'
            ]
            
            for key in required_keys:
                self.assertIn(key, config, f"'{key}' eksik")
            
            # training_params alt alanları
            training_params_keys = ['max_iterations', 'learning_rate', 'target_error_rate']
            for key in training_params_keys:
                self.assertIn(key, config['training_params'])
            
            # preprocessing alt alanları
            preproc_keys = ['denoise', 'deskew', 'binarize', 'enhance_contrast']
            for key in preproc_keys:
                self.assertIn(key, config['preprocessing'])
        
        finally:
            if os.path.exists(config_path):
                os.unlink(config_path)


class TestCharacterSet(unittest.TestCase):
    """Karakter seti testleri"""
    
    def test_character_set_coverage(self):
        """Karakter seti kapsama testi"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            config_path = tmp.name
        
        try:
            create_training_config(config_path)
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            char_set = config['character_set']
            
            # Temel Arapça harfleri
            basic_arabic = 'ابتثجحخدذرزسشصضطظعغفقكلمنهوي'
            for char in basic_arabic:
                self.assertIn(char, char_set, f"'{char}' eksik")
            
            # Osmanlıca özel karakterler
            ottoman_chars = 'پچژگ'
            for char in ottoman_chars:
                self.assertIn(char, char_set, f"Osmanlıca '{char}' eksik")
        
        finally:
            if os.path.exists(config_path):
                os.unlink(config_path)


class TestTrainingParameters(unittest.TestCase):
    """Eğitim parametreleri testleri"""
    
    def test_iteration_count(self):
        """İterasyon sayısı testi"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            config_path = tmp.name
        
        try:
            create_training_config(config_path)
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            max_iter = config['training_params']['max_iterations']
            
            # Makul bir iterasyon sayısı
            self.assertGreater(max_iter, 1000)
            self.assertLess(max_iter, 100000)
        
        finally:
            if os.path.exists(config_path):
                os.unlink(config_path)
    
    def test_learning_rate(self):
        """Öğrenme oranı testi"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            config_path = tmp.name
        
        try:
            create_training_config(config_path)
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            lr = config['training_params']['learning_rate']
            
            # Makul bir öğrenme oranı
            self.assertGreater(lr, 0.00001)
            self.assertLess(lr, 0.1)
        
        finally:
            if os.path.exists(config_path):
                os.unlink(config_path)
    
    def test_target_error_rate(self):
        """Hedef hata oranı testi"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            config_path = tmp.name
        
        try:
            create_training_config(config_path)
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            error_rate = config['training_params']['target_error_rate']
            
            # Makul bir hata oranı (%0-20 arası)
            self.assertGreaterEqual(error_rate, 0.0)
            self.assertLessEqual(error_rate, 0.2)
        
        finally:
            if os.path.exists(config_path):
                os.unlink(config_path)


if __name__ == '__main__':
    unittest.main()
