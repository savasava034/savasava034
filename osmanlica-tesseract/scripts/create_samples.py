#!/usr/bin/env python3
"""
Örnek Osmanlıca Görüntü Oluşturucu

Bu script, test ve demo için örnek Osmanlıca metin görüntüleri oluşturur.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import sys

def create_sample_image(text, filename, size=(800, 200), font_size=48):
    """
    Osmanlıca metin içeren örnek görüntü oluşturur.
    
    Args:
        text: Osmanlıca metin
        filename: Kaydedilecek dosya adı
        size: Görüntü boyutu (genişlik, yükseklik)
        font_size: Font boyutu
    """
    # Beyaz arka plan
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    
    # Font yüklemeyi dene (sistem fontları)
    try:
        # Arapça destekleyen fontları dene
        font_names = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            '/System/Library/Fonts/Supplemental/Arial.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
        ]
        
        font = None
        for font_path in font_names:
            if os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    break
                except:
                    continue
        
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Metni ortaya çiz
    # Sağdan sola yazım için metni ters çevir değil, PIL otomatik halleder
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Metni çiz
    draw.text((x, y), text, fill='black', font=font)
    
    # Kaydet
    img.save(filename, 'PNG', dpi=(300, 300))
    print(f"✓ Oluşturuldu: {filename}")


def create_all_samples():
    """Tüm örnek görüntüleri oluşturur"""
    
    # Örnek Osmanlıca metinler
    samples = [
        {
            'text': 'بسم الله الرحمن الرحیم',
            'filename': 'sample001_besmele.png',
            'ground_truth': 'sample001_besmele.txt'
        },
        {
            'text': 'العالمین رب لله الحمد',
            'filename': 'sample002_hamd.png',
            'ground_truth': 'sample002_hamd.txt'
        },
        {
            'text': 'الرحیم الرحمن',
            'filename': 'sample003_rahman.png',
            'ground_truth': 'sample003_rahman.txt'
        },
        {
            'text': 'الدین یوم مالک',
            'filename': 'sample004_malik.png',
            'ground_truth': 'sample004_malik.txt'
        },
        {
            'text': 'نعبد إیاک',
            'filename': 'sample005_iyyake.png',
            'ground_truth': 'sample005_iyyake.txt'
        }
    ]
    
    # Dizinleri oluştur
    os.makedirs('sample-data/images', exist_ok=True)
    os.makedirs('sample-data/ground-truth', exist_ok=True)
    
    print("\n=== Örnek Osmanlıca Görüntüler Oluşturuluyor ===\n")
    
    for sample in samples:
        # Görüntü oluştur
        image_path = os.path.join('sample-data/images', sample['filename'])
        create_sample_image(sample['text'], image_path)
        
        # Ground truth dosyası oluştur
        gt_path = os.path.join('sample-data/ground-truth', sample['ground_truth'])
        with open(gt_path, 'w', encoding='utf-8') as f:
            f.write(sample['text'])
        print(f"✓ Ground truth: {gt_path}")
    
    print(f"\n✅ {len(samples)} örnek görüntü oluşturuldu!")
    print(f"📁 Konum: sample-data/")


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    create_all_samples()
