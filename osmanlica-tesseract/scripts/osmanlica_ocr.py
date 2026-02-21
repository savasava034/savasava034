#!/usr/bin/env python3
"""
Osmanlıca OCR - Ana OCR Sınıfı

Bu modül, Osmanlıca metinleri tanımak için optimize edilmiş bir OCR sınıfı sağlar.
Tesseract OCR motorunu kullanır ve Osmanlıca için özel ön işleme adımları içerir.
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image
from typing import Optional, Dict, List, Tuple
import os


class OsmanlicaOCR:
    """
    Osmanlıca metinler için optimize edilmiş OCR sınıfı.
    
    Bu sınıf, Tesseract OCR motorunu kullanarak Osmanlıca (Arap harfli Türkçe)
    metinleri yüksek doğrulukla tanır.
    
    Attributes:
        language (str): Tesseract dil kodu (varsayılan: 'ara+tur')
        config (str): Tesseract yapılandırma parametreleri
        preprocess (bool): Görüntü ön işleme aktif mi?
    """
    
    def __init__(
        self,
        language: str = 'ara+tur',
        custom_model: Optional[str] = None,
        preprocess: bool = True
    ):
        """
        OsmanlicaOCR sınıfını başlatır.
        
        Args:
            language: Tesseract dil kodu
            custom_model: Özel eğitilmiş model yolu
            preprocess: Görüntü ön işleme yapılsın mı?
        """
        self.language = language
        self.preprocess = preprocess
        
        # Özel model varsa kullan
        if custom_model and os.path.exists(custom_model):
            tessdata_dir = os.path.dirname(custom_model)
            os.environ['TESSDATA_PREFIX'] = tessdata_dir
            self.language = os.path.basename(custom_model).replace('.traineddata', '')
        
        # Tesseract yapılandırması
        self.config = self._get_tesseract_config()
        
    def _get_tesseract_config(self) -> str:
        """
        Osmanlıca için optimize edilmiş Tesseract yapılandırması.
        
        Returns:
            Yapılandırma string'i
        """
        config = '--oem 3 --psm 6'  # LSTM motor, tek metin bloğu
        
        # Sağdan sola yazım için ek ayarlar
        config += ' -c textord_heavy_nr=1'
        config += ' -c tessedit_char_whitelist=ابتثجحخدذرزسشصضطظعغفقكلمنهويءآأؤإئةىپچژگ۱۲۳۴۵۶۷۸۹۰'
        
        return config
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Görüntüyü OCR için optimize eder.
        
        Args:
            image: OpenCV formatında görüntü
            
        Returns:
            İşlenmiş görüntü
        """
        # Gri tonlamaya çevir
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Gürültü azaltma
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Kontrast artırma (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)
        
        # Adaptive thresholding (ikili görüntüye çevirme)
        binary = cv2.adaptiveThreshold(
            enhanced,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )
        
        # Morfolojik işlemler (ince çizgileri kalınlaştırma)
        kernel = np.ones((1, 1), np.uint8)
        processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        return processed
    
    def deskew_image(self, image: np.ndarray) -> np.ndarray:
        """
        Eğri görüntüyü düzeltir.
        
        Args:
            image: OpenCV formatında görüntü
            
        Returns:
            Düzeltilmiş görüntü
        """
        # Koordinatları bul
        coords = np.column_stack(np.where(image > 0))
        
        # Eğim açısını hesapla
        angle = cv2.minAreaRect(coords)[-1]
        
        if angle < -45:
            angle = 90 + angle
        elif angle > 45:
            angle = angle - 90
        
        # Görüntüyü döndür
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image,
            M,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )
        
        return rotated
    
    def extract_text(
        self,
        image_path: str,
        return_confidence: bool = False
    ) -> str:
        """
        Görüntüden Osmanlıca metin çıkarır.
        
        Args:
            image_path: Görüntü dosyası yolu
            return_confidence: Güven skoru dönülsün mü?
            
        Returns:
            Tanınan metin (ve opsiyonel güven skoru)
        """
        # Görüntüyü yükle
        image = cv2.imread(image_path)
        
        if image is None:
            raise ValueError(f"Görüntü yüklenemedi: {image_path}")
        
        # Ön işleme uygula
        if self.preprocess:
            processed = self.preprocess_image(image)
            processed = self.deskew_image(processed)
        else:
            processed = image
        
        # PIL formatına çevir
        pil_image = Image.fromarray(processed)
        
        # OCR uygula
        if return_confidence:
            data = pytesseract.image_to_data(
                pil_image,
                lang=self.language,
                config=self.config,
                output_type=pytesseract.Output.DICT
            )
            
            # Metni ve güven skorunu hesapla
            text = ' '.join([word for word in data['text'] if word.strip()])
            confidences = [conf for conf in data['conf'] if conf != -1]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return text, avg_confidence
        else:
            text = pytesseract.image_to_string(
                pil_image,
                lang=self.language,
                config=self.config
            )
            
            return text.strip()
    
    def extract_text_with_boxes(
        self,
        image_path: str
    ) -> List[Dict[str, any]]:
        """
        Görüntüden metin ve her kelimenin konumunu çıkarır.
        
        Args:
            image_path: Görüntü dosyası yolu
            
        Returns:
            Her kelime için konum ve metin içeren liste
        """
        # Görüntüyü yükle
        image = cv2.imread(image_path)
        
        if image is None:
            raise ValueError(f"Görüntü yüklenemedi: {image_path}")
        
        # Ön işleme
        if self.preprocess:
            processed = self.preprocess_image(image)
        else:
            processed = image
        
        # PIL formatına çevir
        pil_image = Image.fromarray(processed)
        
        # OCR verilerini al
        data = pytesseract.image_to_data(
            pil_image,
            lang=self.language,
            config=self.config,
            output_type=pytesseract.Output.DICT
        )
        
        # Kelimeleri ve konumları topla
        results = []
        n_boxes = len(data['text'])
        
        for i in range(n_boxes):
            if int(data['conf'][i]) > 0:  # Sadece güvenilir sonuçlar
                results.append({
                    'text': data['text'][i],
                    'confidence': data['conf'][i],
                    'x': data['left'][i],
                    'y': data['top'][i],
                    'width': data['width'][i],
                    'height': data['height'][i]
                })
        
        return results
    
    def batch_process(
        self,
        image_dir: str,
        output_dir: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Bir dizindeki tüm görüntüleri işler.
        
        Args:
            image_dir: Görüntülerin bulunduğu dizin
            output_dir: Çıktıların kaydedileceği dizin (opsiyonel)
            
        Returns:
            Dosya adı -> metin dictionary'si
        """
        results = {}
        
        # Desteklenen görüntü formatları
        extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.bmp']
        
        # Dizindeki tüm görüntüleri işle
        for filename in os.listdir(image_dir):
            if any(filename.lower().endswith(ext) for ext in extensions):
                image_path = os.path.join(image_dir, filename)
                
                try:
                    text = self.extract_text(image_path)
                    results[filename] = text
                    
                    # Çıktıyı kaydet
                    if output_dir:
                        os.makedirs(output_dir, exist_ok=True)
                        output_path = os.path.join(
                            output_dir,
                            f"{os.path.splitext(filename)[0]}.txt"
                        )
                        with open(output_path, 'w', encoding='utf-8') as f:
                            f.write(text)
                
                except Exception as e:
                    print(f"Hata ({filename}): {str(e)}")
                    results[filename] = None
        
        return results


def main():
    """Örnek kullanım"""
    import sys
    
    if len(sys.argv) < 2:
        print("Kullanım: python osmanlica_ocr.py <goruntu-dosyasi>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # OCR nesnesi oluştur
    ocr = OsmanlicaOCR()
    
    # Metni çıkar
    text, confidence = ocr.extract_text(image_path, return_confidence=True)
    
    print(f"Tanınan Metin:\n{text}\n")
    print(f"Güven Skoru: {confidence:.2f}%")


if __name__ == '__main__':
    main()
