import ssl
import urllib.request
from pathlib import Path


class CertManager:
    def __init__(self):
        self.cert_url = (
            "https://hg-edge.mozilla.org/mozilla-central/file/tip/"
            "security/nss/lib/ckfw/builtins/certdata.txt"
        )
        self.cert_dir = Path.home() / "minimypal_certs"
        self.cert_dir.mkdir(exist_ok=True)
        self.cert_file_txt = self.cert_dir / "certdata.txt"
        self.cert_file_pem = self.cert_dir / "certdata.pem"

    def download_certs(self):
        with urllib.request.urlopen(self.cert_url, timeout=15) as response:
            data = response.read().decode("utf-8")
        self.cert_file_txt.write_text(data, encoding="utf-8")

    def convert_to_pem(self):
        if not self.cert_file_txt.exists():
            return

        # This project does not yet include a real NSS-to-PEM converter.
        # Keep the latest downloaded bundle around without crashing startup.
        content = self.cert_file_txt.read_text(encoding="utf-8")
        self.cert_file_pem.write_text(content, encoding="utf-8")

    def prepare_certs(self):
        try:
            self.download_certs()
            self.convert_to_pem()
        except Exception:
            # Browsing should still work with the platform default trust store.
            pass

    def create_ssl_context(self):
        context = ssl.create_default_context()
        if self.cert_file_pem.exists():
            try:
                context.load_verify_locations(cafile=str(self.cert_file_pem))
            except ssl.SSLError:
                pass
        return context
