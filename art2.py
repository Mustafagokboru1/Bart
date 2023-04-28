from bitcoinlib.wallets import Wallet
from bitcoinlib.transactions import Transaction

# Yeni bir cüzdan oluştur
wallet = Wallet.create("my_wallet_31")

# Bitcoin blok zincirini okumak için blok yükleyiciyi oluştur
block_fetcher = wallet.get_block_fetcher()

# Son 1000 bloğu okumak için bir döngü başlat
for block_height in range(block_fetcher.height - 1000, block_fetcher.height):
    # Blok nesnesini getir
    block = block_fetcher.get(block_height)
    # Blokta bulunan tüm işlemleri döngüye al
    for txid in block.txids:
        # İşlem nesnesini getir
        tx = Transaction.get(txid)
        # İşlemin girdi ve çıktılarını döngüye al
        for input in tx.inputs:
            # Girdinin adresini al ve listeye ekle
            address = input.address
            wallet.add_address(address)
        for output in tx.outputs:
            # Çıktının adresini al ve listeye ekle
            address = output.address
            wallet.add_address(address)

# Tüm adresleri tarayan bir fonksiyon tanımla
def scan_addresses():
    # Zayıf adresleri saklamak için boş bir sözlük oluştur
    weak_addresses = {}
    # Adres listesini döngüye al
    for address in wallet.addresses:
        # Adresin özel anahtarını rastgele sayılardan oluşturmaya çalış
        try:
            private_key = wallet.create_key(address).wif()
        except:
            continue
        # Özel anahtarın adresi ile eşleşip eşleşmediğini kontrol et
        if wallet.create_key(private_key).address() == address:
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
