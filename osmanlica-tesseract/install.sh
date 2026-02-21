#!/bin/bash
# Osmanlıca Tesseract OCR - Kurulum Scripti

echo "=================================================="
echo "  Osmanlıca Tesseract OCR - Kurulum"
echo "=================================================="
echo ""

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# İşletim sistemi kontrolü
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
else
    OS="other"
fi

echo "İşletim Sistemi: $OS"
echo ""

# 1. Tesseract kurulumu
echo "1. Tesseract OCR kurulumu..."
echo ""

if command -v tesseract &> /dev/null; then
    echo -e "${GREEN}✓${NC} Tesseract zaten kurulu"
    tesseract --version | head -1
else
    echo -e "${YELLOW}⚠${NC} Tesseract bulunamadı. Kuruluyor..."
    
    if [ "$OS" == "linux" ]; then
        sudo apt-get update
        sudo apt-get install -y tesseract-ocr tesseract-ocr-ara tesseract-ocr-tur
        echo -e "${GREEN}✓${NC} Tesseract kuruldu"
    elif [ "$OS" == "mac" ]; then
        if command -v brew &> /dev/null; then
            brew install tesseract tesseract-lang
            echo -e "${GREEN}✓${NC} Tesseract kuruldu"
        else
            echo -e "${RED}✗${NC} Homebrew bulunamadı. Lütfen manuel olarak kurun:"
            echo "    https://github.com/tesseract-ocr/tesseract"
            exit 1
        fi
    else
        echo -e "${RED}✗${NC} Desteklenmeyen işletim sistemi"
        echo "Lütfen manuel olarak kurun: https://github.com/tesseract-ocr/tesseract"
        exit 1
    fi
fi

echo ""

# 2. Python kontrolü
echo "2. Python kontrolü..."
echo ""

if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓${NC} Python3 mevcut"
    python3 --version
else
    echo -e "${RED}✗${NC} Python3 bulunamadı!"
    echo "Lütfen Python 3.7+ kurun: https://www.python.org/"
    exit 1
fi

echo ""

# 3. pip kontrolü
echo "3. pip kontrolü..."
echo ""

if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓${NC} pip3 mevcut"
else
    echo -e "${RED}✗${NC} pip3 bulunamadı!"
    echo "Lütfen pip kurun: python3 -m ensurepip"
    exit 1
fi

echo ""

# 4. Python paketlerini kur
echo "4. Python paketleri kuruluyor..."
echo ""

pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Python paketleri kuruldu"
else
    echo -e "${RED}✗${NC} Paket kurulumunda hata!"
    exit 1
fi

echo ""

# 5. Dizin yapısını kontrol et
echo "5. Dizin yapısı kontrol ediliyor..."
echo ""

mkdir -p training-data/{images,ground-truth,fonts}
mkdir -p models
mkdir -p examples

echo -e "${GREEN}✓${NC} Dizinler hazır"
echo ""

# 6. Tesseract dil dosyalarını kontrol et
echo "6. Tesseract dil dosyaları kontrol ediliyor..."
echo ""

if tesseract --list-langs 2>/dev/null | grep -q "ara"; then
    echo -e "${GREEN}✓${NC} Arapça dil dosyası mevcut"
else
    echo -e "${YELLOW}⚠${NC} Arapça dil dosyası bulunamadı"
    echo "Kurulum: sudo apt-get install tesseract-ocr-ara"
fi

if tesseract --list-langs 2>/dev/null | grep -q "tur"; then
    echo -e "${GREEN}✓${NC} Türkçe dil dosyası mevcut"
else
    echo -e "${YELLOW}⚠${NC} Türkçe dil dosyası bulunamadı"
    echo "Kurulum: sudo apt-get install tesseract-ocr-tur"
fi

echo ""

# Kurulum tamamlandı
echo "=================================================="
echo -e "${GREEN}✓ Kurulum Tamamlandı!${NC}"
echo "=================================================="
echo ""
echo "Sonraki adımlar:"
echo ""
echo "1. Demo çalıştır:"
echo "   python3 demo.py"
echo ""
echo "2. Hızlı başlangıç:"
echo "   cat HIZLI-BASLANGIC.md"
echo ""
echo "3. İlk OCR:"
echo "   python3 scripts/osmanlica_ocr.py belge.jpg"
echo ""
echo "4. Dokümantasyon:"
echo "   cat README.md"
echo ""
echo "=================================================="
