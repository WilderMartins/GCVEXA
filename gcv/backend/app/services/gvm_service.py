from gvm.connections import UnixSocketConnection, TLSConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
from ..core.encryption import decrypt_data
from ..models.scanner_config import ScannerConfig

# IDs padrão do OpenVAS. Idealmente, seriam configuráveis.
OPENVAS_SCANNER_ID = "08b69003-5fc2-4037-a479-93b440211c73"
FULL_AND_FAST_CONFIG_ID = "daba56c8-73ec-11df-a475-002264764cea"

class GVMService:
    def __init__(self, config: ScannerConfig):
        self.url = config.url
        self.username = config.username
        self.password = decrypt_data(config.encrypted_password)
        self.connection = self._get_connection()
        self.transform = EtreeTransform()

    def _get_connection(self):
        if self.url.startswith('unix://'):
            return UnixSocketConnection(path=self.url.replace('unix://', ''))
        else:
            from urllib.parse import urlparse
            parsed_url = urlparse(self.url)
            hostname = parsed_url.hostname
            port = parsed_url.port or 9390
            return TLSConnection(hostname=hostname, port=port)

    def connect(self):
        gmp = Gmp(self.connection)
        gmp.connect()
        gmp.authenticate(self.username, self.password)
        return gmp

    def test_connection(self):
        try:
            with self.connect() as gmp:
                version = gmp.get_version()
                return True, version.find('version').text
        except Exception as e:
            return False, str(e)

    def find_or_create_target(self, gmp: Gmp, host: str):
        response = gmp.get_targets(filter_string=f"hosts={host}")
        targets = response.xpath('target')
        if targets:
            return targets[0].get('id')

        # Se não encontrou, cria um novo
        response = gmp.create_target(name=f"Target for {host}", hosts=[host])
        return response.get('id')

    def create_scan_task(self, gmp: Gmp, name: str, target_id: str):
        response = gmp.create_task(
            name=name,
            config_id=FULL_AND_FAST_CONFIG_ID,
            target_id=target_id,
            scanner_id=OPENVAS_SCANNER_ID
        )
        task_id = response.get('id')
        gmp.start_task(task_id)
        return task_id

    def get_scan_report(self, gmp: Gmp, task_id: str):
        # 1. Obter o ID do relatório associado à tarefa concluída
        response = gmp.get_tasks(task_id=task_id)
        report_id = response.find('.//report').get('id')
        if not report_id:
            raise ValueError("Scan report not found or scan not finished.")

        # 2. Obter o relatório completo em formato XML
        report = gmp.get_report(report_id=report_id, details=True)

        # 3. Parsear o XML para extrair as vulnerabilidades
        vulnerabilities = []
        results = report.findall('.//results/result')
        for result in results:
            vuln_data = {
                "name": result.find('name').text,
                "host": result.find('host').text,
                "port": f"{result.find('port').text}",
                "severity": result.find('severity').text,
                "description": result.find('description').text,
                "cvss_score": float(result.find('.//nvt/cvss_base').text)
            }
            vulnerabilities.append(vuln_data)

        return vulnerabilities
