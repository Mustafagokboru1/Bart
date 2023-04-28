from bitcoinlib.services.services import Service
from bitcoinlib.wallets import Wallet

# Bitcoin blok zincirini okumak için Service nesnesi oluştur
service = Service()
service.set_options(rpc_host="localhost", rpc_port=8332, rpc_user="myusername", rpc_password="mypassword")

# Tüm adresleri saklamak için boş bir liste oluştur
addresses = []

# Son 1000 bloğu okumak için bir döngü başlat
for height in range(service.rpc('getblockcount')-999, service.rpc('getblockcount')+1):
    # Blok numarasını ekrana yazdır
    print(f"Blok numarası: {height}")
    # Bloktaki tüm işlemleri döngüye al
    block = service.rpc('getblock', service.rpc('getblockhash', height))
    for txid in block["tx"]:
        tx = service.rpc('getrawtransaction', txid, True)
        # İşlem hash'ini ekrana yazdır
        print(f"İşlem hash'i: {tx['txid']}")
        # İşlemin girdi ve çıktılarını döngüye al
        for input in tx["vin"]:
            if "coinbase" in input:
                continue
            # Girdinin adresini al ve listeye ekle
            address = service.rpc('getaddressfromscript', input["scriptSig"]["asm"].split(" ")[1])
            addresses.append(address)
        for output in tx["vout"]:
            # Çıktının adresini al ve listeye ekle
            address = output["scriptPubKey"]["addresses"][0]
            addresses.append(address)

# Tüm adresleri tarayan bir fonksiyon tanımla
def scan_addresses():
    # Zayıf adresleri saklamak için boş bir sözlük oluştur
    weak_addresses = {}
    # Adres listesini döngüye al
    for address in addresses:
        # Adresin özel anahtarını rastgele sayılardan oluşturmaya çalış
        try:
            wallet = Wallet.create_random()
            wallet.add_private_key(address)
        except:
            continue
        private_key = wallet.private_key(address).to_wif()
        # Özel anahtarın adresi ile eşleşip eşleşmediğini kontrol et
        if wallet.address(address) == address:
            # Eşleşirse, zayıf adres sözlüğüne ekle
            weak_addresses[address] = private_key
    # Zayıf adres sözlüğünü döndür
    return weak_addresses

# Ana program akışı
if __name__ == "__main__":
    # Tüm adresleri tarayan fonksiyonu çağır ve sonucu sakla
    weak_addresses = scan_addresses()
    # Zayıf adresleri kaydetmek için bir dosya aç
    file = open("weak_addresses
