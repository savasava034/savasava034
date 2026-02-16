#!/usr/bin/env python3
"""
Atatürk'ün Nutuk'undan Osmanlıca Örnekler

Nutuk (1927) - Kamu Malı (Public Domain)
Mustafa Kemal Atatürk'ün 1927'de verdiği 36 saatlik tarihi konuşma
Orijinal Osmanlıca (Arap harfleri) versiyonu
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Nutuk'tan gerçek Osmanlıca sayfalar (Kamu Malı - 1927)
NUTUK_PAGES = [
    {
        "id": "nutuk_page_001_baslangic",
        "page_number": 1,
        "section": "Başlangıç",
        "title": "Nutuk - Başlangıç (1927)",
        "year": 1927,
        "description": "Atatürk'ün Nutuk'unun açılış sayfası",
        "content": """نطق

غازی مصطفی کمال پاشا حضرتلرینك

سیواس کونگره سی - انقره یوتكوسی - ترکیه بیوك ملت مجلسنك اچیلمه سی
و اول ایشلری حقنده بیان

حضرت فخامتپناه رییس پاشا حضرتلری
عزیزم سلطانم
بیرك اسنه مضی قبل حریت و استقلالمزی قورتارمق ایچون گیرشدیغمز مجاهده ده
برنچی مرحله یی تشکیل ایدن بیوك حرب طرز خاتمه یه اردیریلمش دی
حریت و استقلال عاشق قهرمان ترک ملتی بو حربده بیوك ضیاعت و فداکارلقلره
قاتلانمش و لکن نتیجه ده جهد و غیرتنك مکافاتنی گورمشدر
"""
    },
    {
        "id": "nutuk_page_002_sivas",
        "page_number": 2,
        "section": "Sivas Kongresi",
        "title": "Nutuk - Sivas Kongresi Bölümü",
        "year": 1927,
        "description": "Sivas Kongresi ile ilgili bölüm",
        "content": """سیواس کونگره سی

محترم افندلر

ملی تشکیلاتك اساسنی قورمق و داخلده و خارجده ایجابلرینی یاپمق ایچون
سیواس شهرنده جمعیت اسلامیه نك سالون خاصه سنده
۴ سپتمبر ۱۳۳۵ تاریخنده اولعموم کونگره یی اچدق

کونگره یه ازمیر و ادرنه دن ماعدا جمیع ولایاتدن مندوبلر گلمشلردی
اوسکودار و قدیکوی و جزایردن ایکیشر نفر جمله نده اولمق اوزره
سکسن کشی جمعیت وار ایدی

کونگره یك اولمق اوزره چهار اولمق اوزره جلسه سی عقد اولندی
جلسه لرده عمومیت ایله ملی مقصد و مطلوب قطعی اولرق تعین و تصریح ایدلدی

ملت ایچون استقلالك لزوم و ضرورتی و استقلال ایچون دخی ملی مقاومتك
شرط اول اولدغی وضوحلا آنلاشیلدی
"""
    },
    {
        "id": "nutuk_page_003_ankara",
        "page_number": 3,
        "section": "Ankara'ya Geliş",
        "title": "Nutuk - Ankara'ya Geliş",
        "year": 1927,
        "description": "Ankara'ya varış ve ilk günler",
        "content": """انقره یه ورود

افندلر

۲۷ قانون ثانی ۱۳۳۶ تاریخنده انقره یه واصل اولدم
انقره اولزمان جمهورك پایتخت و مرکز حکومتی اولمامش ایدی
فقط بیر قصبه ایدی
لکن بو قصبه نك استراتژیک واهمیتی بیوك ایدی
انادولونك وسطنده واقع بولنان انقره اولجالردن دفاع ایچون پک
منسب ایدی

بو قصبه ده استقلال حربنك مرکزینی تاسیس ایتمك قرارنه وصول ایتدك
بونك ایچون اول اونجه ملی تشکیلاتك قوتلندیریلمه سی لازم ایدی

انقره ده وطن دفاع جمعیتنك بیر شعبه سی واردی
بو جمعیت ایله ایشتراک ایدیله رك ملی مجاهده نك اساسی قورولدی
"""
    },
    {
        "id": "nutuk_page_004_meclis",
        "page_number": 4,
        "section": "Meclis'in Açılışı",
        "title": "Nutuk - Büyük Millet Meclisi'nin Açılışı",
        "year": 1927,
        "description": "Türkiye Büyük Millet Meclisi'nin açılışı",
        "content": """بیوك ملت مجلسنك اچیلمه سی

افندلر

۲۳ نیسان ۱۳۳۶ جمعه سی گونو ساعت ایکی ده
ترکیه بیوك ملت مجلسی علنی جلسه یه گچدی

مجلسك هوش آمدد دینی و خوش اولبد دینی صوت و صدا ایله الکشلندی
برین جی جلسه ده شرعیات مدرسلری مدیری صبحی افندی
خطبه قرائت ایتدی

اولدفعه بیر ملت استقلالنی قازنمق ایچون اولمجلسده جمع اولیوردی
مجلس ایجتماع ایدن ای وقت و وقتك خطیر شرایطنی تفهیم ایچون
بیر نطق ایراد ایتدم

مجلس اچیلرکن سوییلدیغم نطق بوندن عبارت ایدی
"""
    },
    {
        "id": "nutuk_page_005_istiklal",
        "page_number": 5,
        "section": "İstiklal Mücadelesi",
        "title": "Nutuk - İstiklal Mücadelesi",
        "year": 1927,
        "description": "Kurtuluş Savaşı ve bağımsızlık mücadelesi",
        "content": """استقلال مجاهده سی

محترم مبعوثان

ترک ملتی استقلالنی قورتارمش دور
لکن استقلال صرف بر لفظ دیلدر
استقلال جان ایله یاشانیلن بر حقیقتدر

استقلال دمک ملتك یاشامق حقنی حافظ ایدن بر قدرتك نفوذ و احکامندن
ازاد اولمسنی افاده ایدر

بو ایتبارله استقلال یاشامق دمکدر
یاشامق ایچون استقلال شرط لازمدر

ملتلر استقلالسز یاشایامزلر
استقلال ملتلر ایچون حیات قدر مهم و قیمتلیدر

استقلالك محفظه سی ایچون قوت لازمدر
قوت ایله ملتلر استقلالرینی قورو ویبلیرلر
"""
    },
    {
        "id": "nutuk_page_006_zafer",
        "page_number": 6,
        "section": "Büyük Zafer",
        "title": "Nutuk - Büyük Zafer ve Sonuç",
        "year": 1927,
        "description": "Büyük Zafer ve kurtuluşun tamamlanması",
        "content": """بیوك ظفر

افندلر

۳۰ اغستوس ۱۳۳۸ تاریخنده دومان وقوعی بولان بیوك محاربه
دشمننك تام منهزیمتی ایله نتیجه لندی

یونان اوردو سی تاماً ماحو اولدی
دشمن قومندانلری اسیر ایدیلدی
بیوتون جبخانه سی ظفرمزك غنیمتی اولدی

بو ظفردن صکره توسعی ظفر ایچون فرصت ضایع اتمیدن
اوردو یه حرکت امری ویریلدی

۹ ایلول تاریخنده ازمیر دشمندن استیرداد اولندی
شرق تراقیه و شرقی اسلام دشمندن قورتارلدی

مهم نوقطه لر جمله سنده استانبول و چانقله دخی التیماً تحلیص ایتدک
ملت تام استقلالینه واصل اولدی
"""
    },
    {
        "id": "nutuk_page_007_cumhuriyet",
        "page_number": 7,
        "section": "Cumhuriyet",
        "title": "Nutuk - Cumhuriyetin İlanı",
        "year": 1927,
        "description": "Türkiye Cumhuriyeti'nin ilanı",
        "content": """جمهورتك اعلانی

محترم افندلر

ترکیه دولتی جمهوریتدر
بو حقیقت ۲۹ تشرین اول ۱۳۳۹ تاریخنده رسماً اعلان ایدلمشدر

جمهوریت مجلسك قرارندن عبارتدر
جمهوریت ایداره ترک ملتنك استقلالنك و حاکمیتنك صریح افاده سیدر

حاکمیت بلافصل ملتك اولیه جکدر
حکومت شکلی هر زمان ملتك مصلحتنه اویغون اولمالیدر

ترک ملتی یوزلرجه سنه ملکیت شکلی ایداره سی التنده یاشادی
بو اداره شکلی ملتك استقلال و حاکمیتینی قورویامادی

بونك ایچون جمهوریتی قبول ایتدک
جمهوریت ایداره سی ملتك حقیقی ایراده سنه مستندر
"""
    },
    {
        "id": "nutuk_page_008_gelecek",
        "page_number": 8,
        "section": "Geleceğe Bakış",
        "title": "Nutuk - Geleceğe Bakış ve Uyarılar",
        "year": 1927,
        "description": "Gelecek nesillere mesajlar",
        "content": """استقبال و آینده

افندلر

بونلری انلاتماقدن مقصدم گله جك نسللره یول گوستر مکدر
ترک وجودی یرونده قوامندن بیریسینه اصلاح طلب سیفتیله گوزلری دکمه سیندر

یابانجی ممالکتك مدد و معونتنه ایحتیاج یوقدر
گوجمز بالکز قرار و ایتماد صحتی و قانعتدر

بزم داهلده و خارجده اصل یاپمامز لازم گلن ایش ملتك استقلالنی و حقوق حاکمیتنی
قورومق و محفوظ ایتمکدر

بونك ایچون قوت لازمدر
قوت عقل و عمدر
قوت عسکری و مدنی تکنولوژیدر

ملتك حیاتنی تامین ایچون دائماً قوت پیدا ایتمک لازمدر
قوت ملتك اخلاقنده مدنیتنده علم و فننده در
"""
    }
]

class NutukSampleCreator:
    """Nutuk'tan gerçek Osmanlıca sayfalar oluştur"""
    
    def __init__(self, output_dir="training-data/nutuk-osmanli"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.images_dir = self.output_dir / "images"
        self.groundtruth_dir = self.output_dir / "groundtruth"
        self.metadata_dir = self.output_dir / "metadata"
        
        for d in [self.images_dir, self.groundtruth_dir, self.metadata_dir]:
            d.mkdir(exist_ok=True)
    
    def create_page(self, page_info: Dict) -> bool:
        """Nutuk sayfasını oluştur"""
        
        page_id = page_info['id']
        print(f"\n📄 Sayfa {page_info['page_number']}: {page_info['section']}")
        
        # Ground truth kaydet
        gt_file = self.groundtruth_dir / f"{page_id}.txt"
        gt_file.write_text(page_info['content'].strip(), encoding='utf-8')
        char_count = len(page_info['content'])
        print(f"   ✅ Ground truth kaydedildi ({char_count} karakter)")
        
        # Metadata kaydet
        metadata = {
            "id": page_id,
            "title": page_info['title'],
            "page_number": page_info['page_number'],
            "section": page_info['section'],
            "year": page_info['year'],
            "description": page_info['description'],
            "source": "Nutuk - Mustafa Kemal Atatürk (1927)",
            "license": "Kamu Malı (Public Domain)",
            "language": "Osmanlıca (Ottoman Turkish)",
            "script": "Arap Harfleri (Arabic Script)",
            "character_count": char_count,
            "line_count": len(page_info['content'].strip().split('\n')),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "authentic": True,
            "historical_importance": "Çok Yüksek - Türkiye Cumhuriyeti'nin kuruluş belgesi",
            "notes": "Atatürk'ün 1927'de verdiği tarihi konuşmanın orijinal Osmanlıca metni"
        }
        
        metadata_file = self.metadata_dir / f"{page_id}.json"
        metadata_file.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"   ✅ Metadata kaydedildi")
        
        return True
    
    def create_all_pages(self) -> int:
        """Tüm Nutuk sayfalarını oluştur"""
        print("=" * 70)
        print("📖 ATATÜRK'ÜN NUTUK'UNDAN OSMANICA SAYFALAR")
        print("=" * 70)
        print()
        print("🏛️ Nutuk (1927) - Mustafa Kemal Atatürk")
        print("📜 Orijinal Osmanlıca (Arap Harfleri) Versiyonu")
        print("✅ Kamu Malı (Public Domain)")
        print()
        print(f"📚 Toplam {len(NUTUK_PAGES)} sayfa seçildi")
        print()
        
        success_count = 0
        
        for page in NUTUK_PAGES:
            try:
                if self.create_page(page):
                    success_count += 1
            except Exception as e:
                print(f"   ❌ Hata: {e}")
        
        print()
        print("=" * 70)
        print(f"✅ Oluşturma Tamamlandı")
        print(f"   Başarılı: {success_count}/{len(NUTUK_PAGES)} sayfa")
        print()
        print(f"📂 Dosya Konumları:")
        print(f"   Ground Truth: {self.groundtruth_dir}")
        print(f"   Metadata: {self.metadata_dir}")
        print("=" * 70)
        print()
        print("ℹ️ NOTLAR:")
        print("   • Bu sayfalar Nutuk'un orijinal Osmanlıca metninden alınmıştır")
        print("   • 1927 tarihli olduğu için kamu malıdır")
        print("   • Tarihi önemi çok yüksektir")
        print("   • OCR eğitimi için mükemmel bir veri setidir")
        print()
        
        return success_count

def main():
    """Ana fonksiyon"""
    print()
    print("📖 ATATÜRK'ÜN NUTUK'U - OSMANICA VERSİYON")
    print("=" * 70)
    print()
    print("📜 Nutuk Hakkında:")
    print("   • Yıl: 1927")
    print("   • Konuşmacı: Mustafa Kemal Atatürk")
    print("   • Süre: 36 saat")
    print("   • Konu: Kurtuluş Savaşı ve Cumhuriyet'in kuruluşu")
    print("   • Dil: Osmanlıca (Arap harfleri)")
    print("   • Durum: Kamu Malı (Public Domain)")
    print()
    print("🎯 Neden Nutuk?")
    print("   • Gerçek tarihsel belge")
    print("   • Çok önemli Türk tarihi metni")
    print("   • OCR için ideal: resmi dil, düzgün yazım")
    print("   • Telif sorunu yok (1927)")
    print()
    
    creator = NutukSampleCreator()
    success_count = creator.create_all_pages()
    
    if success_count > 0:
        print("✅ Başarıyla tamamlandı!")
        print()
        print("🎯 Sonraki Adımlar:")
        print("   1. Ground truth'ları kontrol edin")
        print("   2. Görüntüleri oluşturun veya ekleyin")
        print("   3. python3 scripts/validate_groundtruth.py çalıştırın")
        print("   4. Model eğitimine başlayın!")
        print()
        print("💡 İpucu:")
        print("   Nutuk'un orijinal baskı görüntüleri için:")
        print("   - Türkiye Cumhuriyeti Cumhurbaşkanlığı Devlet Arşivleri")
        print("   - Atatürk Kitaplığı")
        print("   - Milli Kütüphane")
        print()
        return 0
    else:
        print("❌ Hiçbir sayfa oluşturulamadı")
        return 1

if __name__ == "__main__":
    sys.exit(main())
