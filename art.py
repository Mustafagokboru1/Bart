from bitcoinlib.wallets import Wallet

# Tüm adresleri saklamak için boş bir liste oluştur
addresses = []

# Son 1000 bloğu okumak için bir döngü başlat
for block_height in range(blockchain.height - 1000, blockchain.height):
    block_hash = blockchain[block_height]['hash']
    # Blok hash'inden bloğu getir
    block = NetworkAPI.get_block(block_hash)
    # Bloktaki tüm işlemleri döngüye al
    for tx in block['tx']:
        # İşlem hash'ini ekrana yazdır
        print(f"İşlem hash'i: {tx}")
        # İşlemin girdi ve çıktılarını döngüye al
        tx_data = NetworkAPI.get_tx(tx)
        for input in tx_data['vin']:
            # Girdinin adresini al ve listeye ekle
            address = input['addr']
            if address:
                addresses.append(address)
        for output in tx_data['vout']:
            # Çıktının adresini al ve listeye ekle
            address = output['scriptPubKey']['addresses'][0]
            if address:
                addresses.append(address)

# Tüm adresleri tarayan bir fonksiyon tanımla
def scan_addresses():
    # Zayıf adresleri saklamak için boş bir sözlük oluştur
    weak_addresses = {}
    # Adres listesini döngüye al
    for address in addresses:
        # Adresin özel anahtarını rastgele sayılardan oluşturmaya çalış
        try:
            wallet = Wallet.create_random(address, 'mainnet')
            private_key = wallet.get_key().wif()
        except:
            continue
        # Özel anahtarın adresi ile eşleşip eşleşmediğini kontrol et
        if wallet.get_key().address() == address:
            # Eşleşirse, zayıf adres sözlüğüne ekle
            weak_addresses[address] = private_key
    # Zayıf adres sözlüğünü döndür
    return weak_addresses

# Ana program akışı
if __name__ == "__main__":
    # Tüm adresleri tarayan fonksiyonu çağır ve sonucu sakla
    weak_addresses = scan_addresses()
    # Zayıf adresleri kaydetmek için bir dosya aç
    file = open("weak_addresses.txt", "w")
    # Zayıf adresleri ekrana yazdır ve dosyaya kaydet
    print("Zayıf adresler bulundu:")
    for address, private_key in weak_addresses.items():
        print(f"Adres: {address}")
        print(f"Özel anahtar: {private_key}")
        file.write(f"{address},{private_key}\n")
    # Dosyayı kapat
    file.close()
