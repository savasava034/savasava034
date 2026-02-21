#!/usr/bin/env python3
"""
Ön İşleme Modülü Testleri

Bu dosya, preprocess.py modülündeki fonksiyonları test eder.
"""

import unittest
import os
import sys
import numpy as np
import cv2
from pathlib import Path

# Modülü import et
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.preprocess import (
    resize_image,
    denoise_image,
    binarize_image,
    deskew_image,
    enhance_contrast,
    remove_borders,
    sharpen_image,
    remove_shadows,
    preprocess_image
)


class TestPreprocessFunctions(unittest.TestCase):
    """Ön işleme fonksiyonları için test sınıfı"""
    
    def setUp(self):
        """Her test öncesi çalışır - test görüntüsü oluştur"""
        # Basit bir test görüntüsü oluştur (beyaz arka plan, siyah metin)
        self.test_image = np.ones((100, 200), dtype=np.uint8) * 255
        # Ortaya bir dikdörtgen çiz (metin simülasyonu)
        cv2.rectangle(self.test_image, (50, 30), (150, 70), 0, -1)
        
        # Renkli görüntü
        self.test_image_color = cv2.cvtColor(self.test_image, cv2.COLOR_GRAY2BGR)
        
        # Gürültülü görüntü
        self.noisy_image = self.test_image.copy()
        noise = np.random.normal(0, 25, self.test_image.shape).astype(np.uint8)
        self.noisy_image = cv2.add(self.noisy_image, noise)
    
    def test_resize_image(self):
        """Görüntü yeniden boyutlandırma testi"""
        original_shape = self.test_image.shape
        
        # 2x büyütme
        resized = resize_image(self.test_image, target_dpi=144, current_dpi=72)
        
        # Boyutun değiştiğini kontrol et
        self.assertNotEqual(resized.shape, original_shape)
        self.assertIsInstance(resized, np.ndarray)
    
    def test_denoise_image_fastNlMeans(self):
        """fastNlMeans gürültü temizleme testi"""
        denoised = denoise_image(self.noisy_image, method='fastNlMeans')
        
        self.assertIsNotNone(denoised)
        self.assertEqual(denoised.shape, self.noisy_image.shape)
        self.assertEqual(denoised.dtype, np.uint8)
    
    def test_denoise_image_bilateral(self):
        """Bilateral gürültü temizleme testi"""
        denoised = denoise_image(self.noisy_image, method='bilateral')
        
        self.assertIsNotNone(denoised)
        self.assertEqual(denoised.shape, self.noisy_image.shape)
    
    def test_denoise_image_gaussian(self):
        """Gaussian gürültü temizleme testi"""
        denoised = denoise_image(self.noisy_image, method='gaussian')
        
        self.assertIsNotNone(denoised)
        self.assertEqual(denoised.shape, self.noisy_image.shape)
    
    def test_denoise_invalid_method(self):
        """Geçersiz yöntem testi"""
        with self.assertRaises(ValueError):
            denoise_image(self.noisy_image, method='invalid_method')
    
    def test_binarize_otsu(self):
        """Otsu binarizasyon testi"""
        binary = binarize_image(self.test_image, method='otsu')
        
        self.assertIsNotNone(binary)
        # Binary görüntü sadece 0 ve 255 değerlerini içermeli
        unique_values = np.unique(binary)
        self.assertTrue(len(unique_values) <= 2)
    
    def test_binarize_adaptive(self):
        """Adaptive binarizasyon testi"""
        binary = binarize_image(self.test_image, method='adaptive')
        
        self.assertIsNotNone(binary)
        self.assertEqual(binary.shape, self.test_image.shape)
    
    def test_binarize_simple(self):
        """Simple binarizasyon testi"""
        binary = binarize_image(self.test_image, method='simple')
        
        self.assertIsNotNone(binary)
        unique_values = np.unique(binary)
        self.assertTrue(len(unique_values) <= 2)
    
    def test_deskew_image(self):
        """Eğrilik düzeltme testi"""
        deskewed = deskew_image(self.test_image)
        
        self.assertIsNotNone(deskewed)
        self.assertEqual(deskewed.shape, self.test_image.shape)
    
    def test_enhance_contrast_clahe(self):
        """CLAHE kontrast artırma testi"""
        enhanced = enhance_contrast(self.test_image, method='clahe')
        
        self.assertIsNotNone(enhanced)
        self.assertEqual(enhanced.shape, self.test_image.shape)
    
    def test_enhance_contrast_histogram(self):
        """Histogram kontrast artırma testi"""
        enhanced = enhance_contrast(self.test_image, method='histogram')
        
        self.assertIsNotNone(enhanced)
        self.assertEqual(enhanced.shape, self.test_image.shape)
    
    def test_remove_borders(self):
        """Kenar kaldırma testi"""
        cropped = remove_borders(self.test_image, border_size=5)
        
        self.assertIsNotNone(cropped)
        # Boyutun küçüldüğünü kontrol et
        self.assertTrue(cropped.shape[0] < self.test_image.shape[0])
        self.assertTrue(cropped.shape[1] < self.test_image.shape[1])
    
    def test_sharpen_image(self):
        """Keskinleştirme testi"""
        sharpened = sharpen_image(self.test_image)
        
        self.assertIsNotNone(sharpened)
        self.assertEqual(sharpened.shape, self.test_image.shape)
    
    def test_remove_shadows(self):
        """Gölge kaldırma testi"""
        no_shadow = remove_shadows(self.test_image)
        
        self.assertIsNotNone(no_shadow)
        self.assertEqual(no_shadow.shape, self.test_image.shape)
    
    def test_preprocess_image_with_temp_file(self):
        """Tam ön işleme pipeline testi (dosya ile)"""
        # Geçici dosya oluştur
        temp_input = '/tmp/test_input.png'
        temp_output = '/tmp/test_output.png'
        
        cv2.imwrite(temp_input, self.test_image)
        
        try:
            processed = preprocess_image(
                temp_input,
                temp_output,
                denoise=True,
                deskew=True,
                binarize=True,
                enhance_contrast=True
            )
            
            self.assertIsNotNone(processed)
            self.assertTrue(os.path.exists(temp_output))
            
        finally:
            # Temizlik
            if os.path.exists(temp_input):
                os.remove(temp_input)
            if os.path.exists(temp_output):
                os.remove(temp_output)


class TestEdgeCases(unittest.TestCase):
    """Sınır durumları ve hata kontrolü testleri"""
    
    def test_empty_image(self):
        """Boş görüntü testi"""
        empty = np.zeros((10, 10), dtype=np.uint8)
        
        # Fonksiyonlar boş görüntüde hata vermemeli
        result = denoise_image(empty)
        self.assertIsNotNone(result)
    
    def test_very_small_image(self):
        """Çok küçük görüntü testi"""
        tiny = np.ones((5, 5), dtype=np.uint8) * 128
        
        result = binarize_image(tiny, method='simple')
        self.assertIsNotNone(result)
    
    def test_large_border_removal(self):
        """Çok büyük kenar kaldırma testi"""
        small_img = np.ones((20, 20), dtype=np.uint8) * 255
        
        # Görüntüden büyük kenar kaldırma - orijinal dönmeli
        result = remove_borders(small_img, border_size=15)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
