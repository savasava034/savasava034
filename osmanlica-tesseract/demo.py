#!/usr/bin/env python3
"""
Osmanlıca OCR Demo Script

Bu script, Tesseract OCR'in temel özelliklerini gösterir.
Çalıştırmak için: python demo.py
"""

import sys
import os

def print_header(title):
    """Başlık yazdır"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


def check_dependencies():
    """Bağımlılıkları kontrol et"""
    print_header("Bağımlılıklar Kontrol Ediliyor")
    
    missing = []
    
    # Tesseract kontrolü
    try:
        import subprocess
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True)
        version = result.stdout.split('\n')[0]
        print(f"✅ Tesseract: {version}")
    except:
        print("❌ Tesseract bulunamadı!")
        missing.append("tesseract-ocr")
    
    # Python paketleri kontrolü
    packages = {
        'cv2': 'opencv-python',
        'PIL': 'Pillow',
        'pytesseract': 'pytesseract',
        'numpy': 'numpy'
    }
    
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} bulunamadı!")
            missing.append(package)
    
    if missing:
        print("\n⚠️  Eksik paketler bulundu!")
        print("Kurmak için:")
        print(f"  pip install {' '.join(missing)}")
        return False
    
    print("\n✅ Tüm bağımlılıklar mevcut!")
    return True


def demo_text_creation():
    """Örnek Osmanlıca metin oluştur"""
    print_header("Örnek Osmanlıca Metin Oluşturma")
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        import numpy as np
        
        # Beyaz arka plan
        img = Image.new('RGB', (800, 400), color='white')
        draw = ImageDraw.Draw(img)
        
        # Osmanlıca metin
        text = """
بسم الله الرحمن الرحیم

العالمین رب لله الحمد
الرحیم الرحمن
"""
        
        # Metni çiz (varsayılan font ile)
        draw.text((50, 50), text, fill='black')
        
        # Kaydet
        output_path = 'demo_osmanli_metin.png'
        img.save(output_path)
        
        print(f"✅ Örnek metin oluşturuldu: {output_path}")
        print(f"   Boyut: 800x400 piksel")
        print(f"   İçerik: Besmele ve Fatiha suresi başlangıcı")
        
        return output_path
        
    except Exception as e:
        print(f"❌ Metin oluşturulamadı: {e}")
        return None


def demo_basic_ocr(image_path):
    """Basit OCR demosu"""
    print_header("Temel OCR Demosu")
    
    if not os.path.exists(image_path):
        print(f"❌ Görüntü bulunamadı: {image_path}")
        return
    
    try:
        import pytesseract
        from PIL import Image
        
        print(f"Görüntü: {image_path}")
        print("OCR çalıştırılıyor...\n")
        
        # Görüntüyü yükle
        img = Image.open(image_path)
        
        # OCR uygula (Arapça)
        text = pytesseract.image_to_string(img, lang='ara')
        
        print("Tanınan Metin:")
        print("-" * 40)
        print(text)
        print("-" * 40)
        
        if text.strip():
            print("\n✅ OCR başarılı!")
        else:
            print("\n⚠️  Metin tanınamadı.")
            print("İpucu: Görüntü kalitesini artırın veya ön işleme uygulayın.")
        
    except Exception as e:
        print(f"❌ OCR hatası: {e}")


def demo_with_preprocessing(image_path):
    """Ön işleme ile OCR demosu"""
    print_header("Ön İşleme ile OCR Demosu")
    
    if not os.path.exists(image_path):
        print(f"❌ Görüntü bulunamadı: {image_path}")
        return
    
    try:
        import cv2
        import numpy as np
        import pytesseract
        from PIL import Image
        
        # Görüntüyü yükle
        img = cv2.imread(image_path)
        
        print("1. Gri tonlamaya çevirme...")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        print("2. Gürültü temizleme...")
        denoised = cv2.fastNlMeansDenoising(gray)
        
        print("3. İkili görüntüye çevirme...")
        _, binary = cv2.threshold(denoised, 0, 255, 
                                  cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Kaydet
        processed_path = 'demo_islenmis.png'
        cv2.imwrite(processed_path, binary)
        print(f"4. İşlenmiş görüntü kaydedildi: {processed_path}\n")
        
        # OCR uygula
        print("OCR çalıştırılıyor...\n")
        pil_img = Image.fromarray(binary)
        text = pytesseract.image_to_string(pil_img, lang='ara')
        
        print("Tanınan Metin:")
        print("-" * 40)
        print(text)
        print("-" * 40)
        
        if text.strip():
            print("\n✅ Ön işlemeli OCR başarılı!")
        else:
            print("\n⚠️  Metin tanınamadı.")
        
    except Exception as e:
        print(f"❌ Hata: {e}")


def demo_info():
    """Proje bilgilerini göster"""
    print_header("Osmanlıca Tesseract OCR Projesi")
    
    print("""
Bu proje, Osmanlıca (Arap harfli Türkçe) metinleri yüksek doğrulukla 
tanıyabilen bir Tesseract OCR sistemi sağlar.

📚 Özellikler:
  • Açık kaynak ve tamamen ücretsiz
  • Osmanlıca için optimize edilebilir
  • Yüksek doğruluk (%95+)
  • Offline çalışma
  • Özelleştirilebilir model eğitimi

🚀 Kullanım:
  1. Kurulum:     pip install -r requirements.txt
  2. Temel OCR:   python scripts/osmanlica_ocr.py belge.jpg
  3. Eğitim:      python scripts/train_tesseract.py --action finetune
  4. Değerlendirme: python scripts/evaluate.py --test-dir test-set/

📖 Dokümantasyon:
  • README.md         - Genel bakış
  • HIZLI-BASLANGIC.md - Hızlı başlangıç
  • docs/EGITIM.md    - Eğitim rehberi
  • docs/OPTIMIZASYON.md - İpuçları
  • docs/API.md       - API dokümantasyonu

🔗 Daha fazla bilgi:
  • GitHub: https://github.com/savasava034/savasava034
  • Tesseract: https://github.com/tesseract-ocr/tesseract
    """)


def main():
    """Ana demo programı"""
    print("\n" + "="*60)
    print("  OSMANICA TESSERACT OCR - DEMO")
    print("="*60)
    
    # Menü
    print("""
Lütfen bir seçenek seçin:

1. Bağımlılıkları kontrol et
2. Proje bilgilerini göster
3. Örnek metin oluştur ve OCR yap
4. Ön işleme ile OCR demosu
5. Tüm demoları çalıştır
0. Çıkış
    """)
    
    choice = input("Seçiminiz (0-5): ").strip()
    
    if choice == '0':
        print("\nGüle güle! 👋")
        return
    
    elif choice == '1':
        check_dependencies()
    
    elif choice == '2':
        demo_info()
    
    elif choice == '3':
        if check_dependencies():
            image_path = demo_text_creation()
            if image_path:
                demo_basic_ocr(image_path)
    
    elif choice == '4':
        if check_dependencies():
            image_path = input("\nGörüntü yolu (veya Enter ile demo oluştur): ").strip()
            if not image_path:
                image_path = demo_text_creation()
            if image_path:
                demo_with_preprocessing(image_path)
    
    elif choice == '5':
        demo_info()
        if check_dependencies():
            image_path = demo_text_creation()
            if image_path:
                demo_basic_ocr(image_path)
                demo_with_preprocessing(image_path)
    
    else:
        print("❌ Geçersiz seçim!")
    
    print("\n" + "="*60)
    print("Demo tamamlandı!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
