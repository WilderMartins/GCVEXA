import subprocess
import tempfile
import shutil
import os
from pathlib import Path

class SemgrepService:
    def __init__(self):
        self.scan_output_path = None

    def run_scan(self, repo_url: str) -> str:
        """
        Clona um repositório, executa o Semgrep via Docker e retorna o caminho do arquivo de resultados JSON.
        """
        temp_dir = tempfile.mkdtemp()
        print(f"Clonando {repo_url} para {temp_dir}...")

        try:
            # 1. Clonar o repositório
            subprocess.run(["git", "clone", "--depth", "1", repo_url, temp_dir], check=True)

            # 2. Executar o Semgrep via Docker
            output_filename = "semgrep_results.json"
            self.scan_output_path = os.path.join(temp_dir, output_filename)

            # O diretório de trabalho do container será /src
            # Mapeamos o temp_dir para /src
            docker_command = [
                "docker", "run", "--rm",
                "-v", f"{temp_dir}:/src",
                "semgrep/semgrep",
                "semgrep", "scan", "--json", "-o", f"/src/{output_filename}", "/src"
            ]

            print("Executando o container do Semgrep...")
            subprocess.run(docker_command, check=True, capture_output=True, text=True)

            print(f"Scan do Semgrep concluído. Resultados em: {self.scan_output_path}")
            return self.scan_output_path

        except subprocess.CalledProcessError as e:
            print(f"Erro durante a execução do Semgrep: {e.stderr}")
            raise RuntimeError(f"Falha ao escanear o repositório: {e.stderr}") from e
        except Exception as e:
            print(f"Uma exceção inesperada ocorreu: {e}")
            raise
        # O 'finally' block para limpeza será chamado pelo método que usa este serviço.

    def cleanup(self):
        """
        Limpa o diretório temporário.
        """
        if self.scan_output_path:
            temp_dir = os.path.dirname(self.scan_output_path)
            if os.path.exists(temp_dir):
                print(f"Limpando diretório temporário: {temp_dir}")
                shutil.rmtree(temp_dir)
