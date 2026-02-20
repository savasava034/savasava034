@echo off
REM Atatürk Arşiv Sistemi - Basit Başlatıcı (Windows)

echo ========================================
echo 🇹🇷 ATATÜRK ARŞİV SİSTEMİ - BAŞLATICI
echo ========================================
echo.

REM Dosya kontrolü
if not exist "interaktif_arayuz.py" (
    echo ⚠️  Dikkat: interaktif_arayuz.py bulunamadı!
    echo.
    echo Lütfen şu klasördeyken çalıştırın:
    echo   ataturk-arsivi\araclar\
    echo.
    echo Örnek:
    echo   cd ataturk-arsivi\araclar
    echo   baslatici.bat
    pause
    exit /b 1
)

REM Python kontrolü
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı!
    echo.
    echo Lütfen Python'u yükleyin:
    echo   https://www.python.org/downloads/
    echo.
    echo Kurulumda "Add Python to PATH" seçeneğini işaretleyin!
    pause
    exit /b 1
)

echo ✅ Python bulundu
python --version
echo.

REM Menü
:menu
echo Ne yapmak istersiniz?
echo.
echo 1. 📥 Örnek verileri yükle (20+ Atatürk sözü)
echo 2. 🖥️  İnteraktif menüyü başlat
echo 3. ℹ️  Sistem bilgisi göster
echo 0. ❌ Çıkış
echo.
set /p choice="Seçiminiz (1-3): "

if "%choice%"=="1" goto load_data
if "%choice%"=="2" goto start_menu
if "%choice%"=="3" goto show_info
if "%choice%"=="0" goto exit
echo ❌ Geçersiz seçim!
goto menu

:load_data
echo.
echo 📥 Örnek veriler yükleniyor...
echo.
python ornek_veri_yukle.py
echo.
echo ✅ İşlem tamamlandı!
echo.
set /p yn="İnteraktif menüyü başlatmak ister misiniz? (e/h): "
if /i "%yn%"=="e" (
    python interaktif_arayuz.py
)
goto end

:start_menu
echo.
echo 🖥️  İnteraktif menü başlatılıyor...
echo.
python interaktif_arayuz.py
goto end

:show_info
echo.
echo ========================================
echo ℹ️  Sistem Bilgisi
echo ========================================
python --version
echo Klasör: %cd%
echo.
if exist "veriler\sozler.json" (
    echo ✅ Veri dosyası mevcut
    python -c "import json; f=open('veriler/sozler.json'); d=json.load(f); print('📊 Kayıtlı söz sayısı:', len(d.get('sozler', [])))" 2>nul
) else (
    echo ⚠️  Veri dosyası henüz oluşturulmamış
    echo 💡 Örnek verileri yüklemek için seçenek 1'i kullanın
)
echo.
pause
goto menu

:exit
echo.
echo 👋 Görüşürüz!
exit /b 0

:end
echo.
echo 👋 Program sonlandı.
pause
