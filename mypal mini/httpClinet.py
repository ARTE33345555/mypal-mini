# http_client.py
import os
import ssl
import urllib.request
from pathlib import Path

class CertManager:
    def __init__(self):
        # URL Mozilla certdata.txt
        self.cert_url = (
            "https://hg-edge.mozilla.org/mozilla-central/file/tip/"
            "security/nss/lib/ckfw/builtins/certdata.txt"
        )
        # Папка для хранения сертификатов
        self.cert_dir = Path.home() / "minimypal_certs"
        self.cert_dir.mkdir(exist_ok=True)
        self.cert_file_txt = self.cert_dir / "certdata.txt"
        self.cert_file_pem = self.cert_dir / "certdata.pem"

    # Скачать certdata.txt
    def download_certs(self):
        print("Downloading certdata.txt from Mozilla...")
        with urllib.request.urlopen(self.cert_url) as response:
            data = response.read().decode("utf-8")
        self.cert_file_txt.write_text(data)
        print(f"Saved certdata.txt to {self.cert_file_txt}")

    # Конвертировать certdata.txt в PEM (здесь упрощённо)
    def convert_to_pem(self):
        print("Converting certdata.txt to PEM...")
        content = self.cert_file_txt.read_text()
        # В реальности нужен парсер NSS certdata → PEM
        # Для примера просто сохраняем в файл
        self.cert_file_pem.write_text(content)
        print(f"Saved PEM to {self.cert_file_pem}")

    # Создать HTTPS-контекст с нашими сертификатами
    def create_ssl_context(self):
        context = ssl.create_default_context()
        # Подгружаем PEM сертификаты
        context.load_verify_locations(cafile=str(self.cert_file_pem))
        return context


# Пример использования
if __name__ == "__main__":
    manager = CertManager()
    
    # 1. Скачать сертификаты
    manager.download_certs()
    
    # 2. Конвертировать в PEM
    manager.convert_to_pem()
    
    # 3. Создать SSL-контекст
    context = manager.create_ssl_context()
    
    # 4. Пример HTTPS-запроса с обновлёнными сертификатами
    import urllib.request
    url = "https://www.google.com"
    with urllib.request.urlopen(url, context=context) as response:
        print("Status code:", response.getcode())
        print("First 200 chars of page:", response.read(200).decode())