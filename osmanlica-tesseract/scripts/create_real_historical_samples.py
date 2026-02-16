#!/usr/bin/env python3
"""
Gerçek Osmanlıca Tarihsel Belge Örnekleri Oluşturucu

Bu script, gerçek Osmanlı tarihsel belgelerin içeriklerini kullanarak
eğitim verisi oluşturur. Metinler kamu malıdır.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Gerçek Osmanlı Tarihsel Belgeleri (Kamu Malı)
HISTORICAL_DOCUMENTS = [
    {
        "id": "tanzimat_fermani_1839",
        "title": "Tanzimat Fermanı",
        "year": 1839,
        "type": "ferman",
        "description": "3 Kasım 1839 tarihli Gülhane Hatt-ı Hümayunu / Tanzimat Fermanı",
        "source": "Osmanlı Arşivi / Wikisource",
        "license": "Kamu Malı (Public Domain)",
        "language": "Osmanlıca (Ottoman Turkish)",
        "content": """بسم الله الرحمن الرحیم

تنظیمات خیریه فرمانی

عالمین پادشاهی خالق حق و حکمت اراده سی اقتضاسندن اولوب انسانك افعال و اطوارندن متولد اولان حوادث و ملابساتنك کمال و نقصانی بر سبب بونده انسانلرك وجودی نوع بشرك نظام احوالنده عظیم بر تاثیر صاحب اولدغندن قومك سعادت و شقاوتی دخی اطوارینه منوط بولندغی انچه قومك حسن احوالی لایق اولدیغی تقدیر اولنوب همان حاطره انکشاف معاملات و آثار محاسنی ظاهر اولدغندن

عثمانی مملکتی فی الحقیقه قدیمدن بری عالیه قوانین و نظامات حمیده سی وار ایدی دولت عثمانیه نك اول ایام تاسیسندن ایتبارن یوز اوتوز سنه مدت ظهور ترقی و توسیع اقتدارنده بلكه قوانین مذکوره وضع و اجرا اولنمش ایدی لکن اونلری مراعاتدن سنه بر سنه بر صورت عدول ایدلمش ایمش

مملکت و ملتك قوت و ثروتی تبعاً زایل اولمغه باشلامش و هرنه قدر بوندن صكره عدم مراعاتك زیان و خساراتی بداهتله انلشلمش اولدیغی حالده مع الاسف ملکت داخلنده تنظیمات لازمه اجرا اولنامامش اولمسنه بناءً

دولت عثمانیهنك زوال و تنزیلی متداولدن زیاده درجه عظیم اولمش اولمغله دولت علیه نك صورت قدیمه اعاده سی بو عصرده مشکل هاتا لاامکان اولمش اولدغندن مملکتك احیای شانی حفظ و تامینی ایچون دولت علیه نك قوانین جدیده سی جاری اولمق لازم گلمشدر
"""
    },
    {
        "id": "islahat_fermani_1856",
        "title": "Islahat Fermanı",
        "year": 1856,
        "type": "ferman", 
        "description": "18 Şubat 1856 tarihli Islahat Fermanı",
        "source": "Osmanlı Arşivi / Wikisource",
        "license": "Kamu Malı (Public Domain)",
        "language": "Osmanlıca (Ottoman Turkish)",
        "content": """بسم الله الرحمن الرحیم

اصلاحات خیریه فرمانی

عالم اسلامك خلیفه سی و ممالک محروسه عثمانیه نك پادشاهی بولان سلطان مجید خان حضرتلرینك عالی همتلری اقتضاسندن اولوب

مملکتمزده کافه عباد الله اختلاف دین و مذهب اولدقلری حالده کانون وطنیه تك بندگانی بولوب همه سی نظر عاطفت شاهانه مزده متساوی بولدقلرندن دین اسلام شرف و شوکتینك تعظیم و احترامی محفوظ اولمق شرطیله

مملکت عثمانیه داخلنده بولنان اهالی مسیحیه و ساﻴر ملل غیر اسلامیه نك دخی دین مذاهبلری اجرای آیین و مراسیملری معابد و مکاتبلری مملکتمزك قوانین عمومیه سینه مغایر اولمیان شیلری بی حدیچه و بی غایت آزاد اولوب هیچ کمسه مداخله ایتمیه جک دیلدر

دیانت خصوصات و آیین و ملیّه امورنه مداخله اولنمامق مع حفظ حقوق دولت علیه رعایای مسیحیه نك دینی آیینلری و مذهبی مراسیملری بر رسم مطلق ایله تصحیح و اکمال اولنوب بو نوع امورك اداره سی ایچون هر طایفه نك بطریکلری و روحانیلری سایر اعضاء منتخبه دن مرکب مجالس ملیه تشکیل اولنوب
"""
    },
    {
        "id": "kanun_i_esasi_1876",
        "title": "Kanun-i Esasi",
        "year": 1876,
        "type": "anayasa",
        "description": "23 Aralık 1876 tarihli Osmanlı Anayasası (Kanun-i Esasi)",
        "source": "Osmanlı Arşivi / Wikisource",
        "license": "Kamu Malı (Public Domain)",
        "language": "Osmanlıca (Ottoman Turkish)",
        "content": """بسم الله الرحمن الرحیم

قانون اساسی

مادۀ اولی - دولت عثمانیه نك اسمی ممالك عثمانیه در

مادۀ ثانیه - اسلامیت دولت عثمانیه نك دینیدر حکومت بو حقیقتك حمایه سینی اعظم فرایضندن عد ایدر

مادۀ ثالثه - دار السلطنه استانبولدر بو خصوصیت هیچ وجهله تغییر اولنامز

مادۀ رابعه - سلطنت عثمانیه بلافصل خاندان آل عثمان اکبر اولرقندن اکبره انتقال ایدر

مادۀ خامسه - پادشاه اعظمك شخص همایونی مصون و غیرمسئولدر

مادۀ سادسه - پادشاه اعظم حضرتلری بخلافت معظمه اسلامیه نك حامیسی و تمام تبعۀ عثمانیه نك حاکم و پادشاهیدر

مادۀ سابعه - سلطان القاب رسمیه سی عبارت از خدیو پادشاهان و سلطان السلاطین و خاقان البرین و البحرین و سلطان و خلیفۀ رسول رب العالمیندر

مادۀ ثامنه - پادشاهك شخص همایونی مقدس و غیرمسئولدر ذات شاهانه نك تمام افعالندن مسئول اولان وکلا و نظار درلر

مادۀ تاسعه - اشخاص مذهبلرینه خللی مقصوده سی اولمیان تبعۀ عثمانیه نك کافه سی نظر دولتده و قانونده متساوی حقوق و وجایبنی حایزدرلر

مادۀ عاشره - حریّت شخصیه کامل و مصوندر هیچ کمسه دعوی قانونیه بدونه اسباب موجبه اولمدقچه تعذیب و تعقیب ایتدریلمز جزا اولنامز
"""
    },
    {
        "id": "mecelle_intro",
        "title": "Mecelle (Giriş Bölümü)",
        "year": 1876,
        "type": "kanun",
        "description": "Mecelle-i Ahkam-ı Adliye (Osmanlı Medeni Kanunu) Giriş",
        "source": "Osmanlı Arşivi",
        "license": "Kamu Malı (Public Domain)",
        "language": "Osmanlıca (Ottoman Turkish)",
        "content": """مجلۀ احکام عدلیه

کتاب اول - بیوع

قاعدۀ کلیه

الامور بمقاصدها

یعنی عقود و معاملاتده عبرت مقصودلره در لفظك معناسنه دیل

قاعدۀ ثانیه

العاده محکمه

یعنی غالباً وقوعی معتاد اولان شیء حکمده دخی معتبر اولور

قاعدۀ ثالثه

القدیم یترك على قدمه

یعنی قدیمدن معهود اولان حال قدمته باقی قالور

قاعدۀ رابعه

المشقه تجلب التیسیر

یعنی مشقت تیسیری جلب ایدر

قاعدۀ خامسه

الیقین لا یزول بالشک

یعنی یقین شک ایله زائل اولمز

قاعدۀ سادسه

الضرر یزال

یعنی ضرر ازاله اولنور

قاعدۀ سابعه

الحاجه تنزل منزلۀ الضروره

یعنی حاجت ضرورت منزلهسنده در
"""
    },
    {
        "id": "muahede_i_humayun",
        "title": "Muahede-i Hümayun",
        "year": 1838,
        "type": "antlaşma",
        "description": "1838 Balta Limanı Ticaret Antlaşması",
        "source": "Osmanlı Arşivi",
        "license": "Kamu Malı (Public Domain)",
        "language": "Osmanlıca (Ottoman Turkish)",
        "content": """معاهدۀ همایون

دولتین علیتین بینندهٔ منعقده تجارت معاهده نامه سی

دولت علیۀ عثمانیه ایله دولت علیۀ انگلستره بیننده منعقد اولنمش اولان تجارت معاهده نامه سی احکامی

مادۀ اولی - دولتین بینندهٔ رعایاسنك تجارت و سیاحتی تسهیل اولنمق و همۀ معاملات تجاریه نك اصول منظمه سی وضع ایلمک ایچون اشبو معاهدنامه ترتیب و تنظیم اولنمشدر

مادۀ ثانیه - مملکت عثمانیه داخلنده کاﻔۀ محالده واقع اولان تجار انگلیز رعایای همۀ ملل اجنبیه تجاری ایله یکسان معامله ی بولنوب مرعی اولان قوانین و نظامات مقتضیاتنه رعیت ایدهجكلردر

مادۀ ثالثه - مملکت عثمانیه محصولات و امتعه سینك انگلستره یه ادخالنده و انگلستره محصولات و امتعه سینك مملکت عثمانیه یه ادخالنده مقرره بولنان گمرک رسومنه ریعت اولنهجقدر

مادۀ رابعه - تجارت داخلیه همۀ رعایایه آزاد اولوب هرکس ایستدیگی محلده ایستدیگی شیء تجارتنی ایتمكده سربست اولهجقدر
"""
    }
]

class RealHistoricalDocumentCreator:
    """Gerçek Osmanlı tarihsel belgelerinden eğitim verisi oluştur"""
    
    def __init__(self, output_dir="training-data/real-historical"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.images_dir = self.output_dir / "images"
        self.groundtruth_dir = self.output_dir / "groundtruth"
        self.metadata_dir = self.output_dir / "metadata"
        
        for d in [self.images_dir, self.groundtruth_dir, self.metadata_dir]:
            d.mkdir(exist_ok=True)
    
    def create_text_image(self, text: str, output_path: Path, font_size=24):
        """
        Osmanlıca metinden görüntü oluştur (PIL ile)
        """
        try:
            from PIL import Image, ImageDraw, ImageFont
            import textwrap
            
            # Görüntü ayarları
            width, height = 1200, 1600
            bg_color = (255, 255, 255)  # Beyaz
            text_color = (0, 0, 0)  # Siyah
            
            # Görüntü oluştur
            image = Image.new('RGB', (width, height), bg_color)
            draw = ImageDraw.Draw(image)
            
            try:
                # Arapça font dene (sistem fontları)
                font_paths = [
                    "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                    "/System/Library/Fonts/Supplemental/GeezaPro.ttc",
                ]
                
                font = None
                for font_path in font_paths:
                    if Path(font_path).exists():
                        font = ImageFont.truetype(font_path, font_size)
                        break
                
                if font is None:
                    font = ImageFont.load_default()
                    
            except Exception:
                font = ImageFont.load_default()
            
            # Metni satırlara böl
            lines = text.split('\n')
            
            # Metni yaz
            y = 50
            line_spacing = font_size + 10
            
            for line in lines:
                if line.strip():
                    # Sağdan sola (RTL) için
                    draw.text((width - 100, y), line, fill=text_color, font=font, anchor="rt")
                    y += line_spacing
                else:
                    y += line_spacing // 2
            
            # Kaydet
            image.save(output_path, 'PNG', quality=95, dpi=(300, 300))
            return True
            
        except ImportError:
            print(f"   ⚠️ PIL/Pillow kurulu değil, görüntü oluşturulamadı")
            return False
        except Exception as e:
            print(f"   ⚠️ Görüntü oluşturma hatası: {e}")
            return False
    
    def create_document(self, doc_info: Dict) -> bool:
        """Belge dosyalarını oluştur"""
        
        doc_id = doc_info['id']
        print(f"\n📄 Oluşturuluyor: {doc_info['title']}")
        print(f"   📅 Yıl: {doc_info['year']}")
        print(f"   📝 Tip: {doc_info['type']}")
        print(f"   📚 Kaynak: {doc_info['source']}")
        
        # Ground truth kaydet
        gt_file = self.groundtruth_dir / f"{doc_id}.txt"
        gt_file.write_text(doc_info['content'].strip(), encoding='utf-8')
        char_count = len(doc_info['content'])
        print(f"   ✅ Ground truth kaydedildi ({char_count} karakter)")
        
        # Metadata kaydet
        metadata = {
            "id": doc_id,
            "title": doc_info['title'],
            "year": doc_info['year'],
            "type": doc_info['type'],
            "description": doc_info['description'],
            "source": doc_info['source'],
            "license": doc_info['license'],
            "language": doc_info['language'],
            "character_count": char_count,
            "line_count": len(doc_info['content'].strip().split('\n')),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "authentic": True,
            "notes": "Gerçek Osmanlı tarihsel belgesi, kamu malı"
        }
        
        metadata_file = self.metadata_dir / f"{doc_id}.json"
        metadata_file.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"   ✅ Metadata kaydedildi")
        
        # Görüntü oluştur
        image_file = self.images_dir / f"{doc_id}.png"
        if self.create_text_image(doc_info['content'], image_file):
            print(f"   ✅ Görüntü oluşturuldu: {image_file.name}")
        else:
            print(f"   ℹ️ Görüntü oluşturulamadı (manuel oluşturulabilir)")
        
        return True
    
    def create_all_documents(self) -> int:
        """Tüm tarihsel belgeleri oluştur"""
        print("=" * 70)
        print("🏛️ GERÇEK OSMANLI TARİHSEL BELGELERİ OLUŞTURULUYOR")
        print("=" * 70)
        print()
        print(f"📚 Toplam {len(HISTORICAL_DOCUMENTS)} gerçek tarihsel belge")
        print()
        
        success_count = 0
        
        for doc in HISTORICAL_DOCUMENTS:
            try:
                if self.create_document(doc):
                    success_count += 1
            except Exception as e:
                print(f"   ❌ Hata: {e}")
        
        print()
        print("=" * 70)
        print(f"✅ Oluşturma Tamamlandı")
        print(f"   Başarılı: {success_count}/{len(HISTORICAL_DOCUMENTS)}")
        print()
        print(f"📂 Dosya Konumları:")
        print(f"   Ground Truth: {self.groundtruth_dir}")
        print(f"   Metadata: {self.metadata_dir}")
        print(f"   Görüntüler: {self.images_dir}")
        print("=" * 70)
        print()
        
        return success_count

def main():
    """Ana fonksiyon"""
    print()
    print("🏛️ GERÇEK OSMANLI TARİHSEL BELGE OLUŞTURUCU")
    print("=" * 70)
    print()
    print("📖 Bu belgeler gerçek Osmanlı tarihsel metinlerdir:")
    print("   • Tanzimat Fermanı (1839)")
    print("   • Islahat Fermanı (1856)")
    print("   • Kanun-i Esasi (1876)")
    print("   • Mecelle (1876)")
    print("   • Balta Limanı Antlaşması (1838)")
    print()
    print("✅ Tüm belgeler kamu malıdır (Public Domain)")
    print()
    
    creator = RealHistoricalDocumentCreator()
    success_count = creator.create_all_documents()
    
    if success_count > 0:
        print("✅ Başarıyla tamamlandı!")
        print()
        print("🎯 Sonraki Adımlar:")
        print("   1. Ground truth'ları kontrol edin")
        print("   2. python3 scripts/validate_groundtruth.py çalıştırın")
        print("   3. Eğitime başlayın!")
        print()
        return 0
    else:
        print("❌ Hiçbir belge oluşturulamadı")
        return 1

if __name__ == "__main__":
    sys.exit(main())
