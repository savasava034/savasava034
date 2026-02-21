#!/usr/bin/env python3
"""
Görüntü Ön İşleme Modülü

Bu modül, OCR öncesi görüntüleri optimize etmek için çeşitli ön işleme
fonksiyonları sağlar.
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from typing import Optional, Tuple
import os


def resize_image(
    image: np.ndarray,
    target_dpi: int = 300,
    current_dpi: int = 72
) -> np.ndarray:
    """
    Görüntüyü hedef DPI'ya yeniden boyutlandırır.
    
    Args:
        image: OpenCV formatında görüntü
        target_dpi: Hedef DPI değeri
        current_dpi: Mevcut DPI değeri
        
    Returns:
        Yeniden boyutlandırılmış görüntü
    """
    scale_factor = target_dpi / current_dpi
    width = int(image.shape[1] * scale_factor)
    height = int(image.shape[0] * scale_factor)
    
    resized = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)
    return resized


def denoise_image(
    image: np.ndarray,
    method: str = 'fastNlMeans'
) -> np.ndarray:
    """
    Görüntüden gürültüyü temizler.
    
    Args:
        image: OpenCV formatında görüntü
        method: Gürültü temizleme yöntemi ('fastNlMeans', 'bilateral', 'gaussian')
        
    Returns:
        Gürültüsü temizlenmiş görüntü
    """
    # Gri tonlama kontrolü
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    if method == 'fastNlMeans':
        denoised = cv2.fastNlMeansDenoising(gray, h=10)
    elif method == 'bilateral':
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)
    elif method == 'gaussian':
        denoised = cv2.GaussianBlur(gray, (5, 5), 0)
    else:
        raise ValueError(f"Bilinmeyen yöntem: {method}")
    
    return denoised


def binarize_image(
    image: np.ndarray,
    method: str = 'adaptive'
) -> np.ndarray:
    """
    Görüntüyü ikili (siyah-beyaz) formata çevirir.
    
    Args:
        image: OpenCV formatında görüntü (gri tonlama)
        method: Binarizasyon yöntemi ('otsu', 'adaptive', 'simple')
        
    Returns:
        İkili görüntü
    """
    if method == 'otsu':
        _, binary = cv2.threshold(
            image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
    elif method == 'adaptive':
        binary = cv2.adaptiveThreshold(
            image,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )
    elif method == 'simple':
        _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    else:
        raise ValueError(f"Bilinmeyen yöntem: {method}")
    
    return binary


def deskew_image(image: np.ndarray) -> np.ndarray:
    """
    Eğri görüntüyü düzeltir.
    
    Args:
        image: OpenCV formatında görüntü
        
    Returns:
        Düzeltilmiş görüntü
    """
    # Koordinatları bul
    coords = np.column_stack(np.where(image > 0))
    
    if len(coords) == 0:
        return image
    
    # Eğim açısını hesapla
    angle = cv2.minAreaRect(coords)[-1]
    
    if angle < -45:
        angle = 90 + angle
    elif angle > 45:
        angle = angle - 90
    
    # Çok küçük açılar için düzeltme yapma
    if abs(angle) < 0.5:
        return image
    
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


def enhance_contrast(
    image: np.ndarray,
    method: str = 'clahe'
) -> np.ndarray:
    """
    Görüntü kontrastını artırır.
    
    Args:
        image: OpenCV formatında görüntü (gri tonlama)
        method: Kontrast artırma yöntemi ('clahe', 'histogram')
        
    Returns:
        Kontrastı artırılmış görüntü
    """
    if method == 'clahe':
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(image)
    elif method == 'histogram':
        enhanced = cv2.equalizeHist(image)
    else:
        raise ValueError(f"Bilinmeyen yöntem: {method}")
    
    return enhanced


def remove_borders(
    image: np.ndarray,
    border_size: int = 10
) -> np.ndarray:
    """
    Görüntü kenarlarındaki gereksiz kenarlıkları kaldırır.
    
    Args:
        image: OpenCV formatında görüntü
        border_size: Kaldırılacak kenarlık boyutu (piksel)
        
    Returns:
        Kenarlıkları kaldırılmış görüntü
    """
    h, w = image.shape[:2]
    
    if h > 2 * border_size and w > 2 * border_size:
        cropped = image[border_size:h-border_size, border_size:w-border_size]
        return cropped
    
    return image


def sharpen_image(image: np.ndarray) -> np.ndarray:
    """
    Görüntüyü keskinleştirir.
    
    Args:
        image: OpenCV formatında görüntü
        
    Returns:
        Keskinleştirilmiş görüntü
    """
    # Keskinleştirme kernel'i
    kernel = np.array([[-1, -1, -1],
                      [-1,  9, -1],
                      [-1, -1, -1]])
    
    sharpened = cv2.filter2D(image, -1, kernel)
    return sharpened


def remove_shadows(image: np.ndarray) -> np.ndarray:
    """
    Görüntüdeki gölgeleri azaltır.
    
    Args:
        image: OpenCV formatında görüntü (gri tonlama)
        
    Returns:
        Gölgeleri azaltılmış görüntü
    """
    # Görüntüyü dilate et (genişlet)
    dilated = cv2.dilate(image, np.ones((7, 7), np.uint8))
    
    # Median blur uygula
    bg = cv2.medianBlur(dilated, 21)
    
    # Orijinal görüntüden arka planı çıkar
    diff = 255 - cv2.absdiff(image, bg)
    
    # Normalize et
    normalized = cv2.normalize(diff, None, alpha=0, beta=255,
                              norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    
    return normalized


def preprocess_image(
    image_path: str,
    output_path: Optional[str] = None,
    denoise: bool = True,
    deskew: bool = True,
    binarize: bool = True,
    enhance_contrast: bool = True,
    sharpen: bool = False,
    remove_shadow: bool = False
) -> np.ndarray:
    """
    Görüntüye tam ön işleme pipeline'ı uygular.
    
    Args:
        image_path: Giriş görüntü yolu
        output_path: Çıkış görüntü yolu (opsiyonel)
        denoise: Gürültü temizleme
        deskew: Eğrilik düzeltme
        binarize: İkili görüntüye çevirme
        enhance_contrast: Kontrast artırma
        sharpen: Keskinleştirme
        remove_shadow: Gölge kaldırma
        
    Returns:
        İşlenmiş görüntü
    """
    # Görüntüyü yükle
    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError(f"Görüntü yüklenemedi: {image_path}")
    
    # Gri tonlamaya çevir
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    # İşleme adımları
    processed = gray
    
    if remove_shadow:
        processed = remove_shadows(processed)
    
    if denoise:
        processed = denoise_image(processed)
    
    if enhance_contrast:
        processed = enhance_contrast(processed)
    
    if sharpen:
        processed = sharpen_image(processed)
    
    if deskew:
        processed = deskew_image(processed)
    
    if binarize:
        processed = binarize_image(processed)
    
    # Kenarlıkları temizle
    processed = remove_borders(processed)
    
    # Çıkış dosyasına kaydet
    if output_path:
        cv2.imwrite(output_path, processed)
    
    return processed


def batch_preprocess(
    input_dir: str,
    output_dir: str,
    **kwargs
) -> None:
    """
    Bir dizindeki tüm görüntüleri işler.
    
    Args:
        input_dir: Giriş görüntü dizini
        output_dir: Çıkış dizini
        **kwargs: preprocess_image fonksiyonuna geçirilecek parametreler
    """
    # Çıkış dizinini oluştur
    os.makedirs(output_dir, exist_ok=True)
    
    # Desteklenen formatlar
    extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.bmp']
    
    # Tüm görüntüleri işle
    for filename in os.listdir(input_dir):
        if any(filename.lower().endswith(ext) for ext in extensions):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            try:
                print(f"İşleniyor: {filename}")
                preprocess_image(input_path, output_path, **kwargs)
            except Exception as e:
                print(f"Hata ({filename}): {str(e)}")


def main():
    """Örnek kullanım"""
    import sys
    
    if len(sys.argv) < 3:
        print("Kullanım: python preprocess.py <girdi-dosyasi> <cikti-dosyasi>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # Görüntüyü işle
    processed = preprocess_image(input_path, output_path)
    
    print(f"İşleme tamamlandı: {output_path}")


if __name__ == '__main__':
    main()
