import time
from zapv2 import ZAPv2
from ..models.scanner_config import ScannerConfig
from ..core.encryption import decrypt_data

class ZAPService:
    def __init__(self, config: ScannerConfig):
        # A URL deve ser o endereço do proxy da API do ZAP, ex: http://localhost:8080
        # A "senha" do nosso modelo será a chave da API do ZAP
        self.apikey = decrypt_data(config.encrypted_password)
        self.zap = ZAPv2(apikey=self.apikey, proxies={'http': config.url, 'https': config.url})

    def start_scan(self, target_url: str):
        """
        Inicia um scan completo (Spider + Active Scan) no ZAP.
        Retorna o ID do scan ativo.
        """
        print(f"Iniciando Spider no alvo: {target_url}")
        scan_id = self.zap.spider.scan(target_url)
        # Esperar o Spider terminar
        while int(self.zap.spider.status(scan_id)) < 100:
            print(f"Progresso do Spider: {self.zap.spider.status(scan_id)}%")
            time.sleep(5)
        print("Spider concluído.")

        print(f"Iniciando Active Scan no alvo: {target_url}")
        ascan_id = self.zap.ascan.scan(target_url)
        return ascan_id

    def get_scan_status(self, scan_id: str) -> int:
        """
        Retorna o progresso (0-100) de um Active Scan.
        """
        return int(self.zap.ascan.status(scan_id))

    def get_scan_results(self, target_url: str) -> list:
        """
        Retorna os alertas (vulnerabilidades) encontrados para um alvo.
        """
        return self.zap.core.alerts(baseurl=target_url)
