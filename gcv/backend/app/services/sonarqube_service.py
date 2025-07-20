import subprocess
import tempfile
import shutil
import os
from sonarqube import SonarQubeClient
from ..models.scanner_config import ScannerConfig
from ..core.encryption import decrypt_data

class SonarQubeService:
    def __init__(self, config: ScannerConfig):
        # A URL é a URL da UI do SonarQube, e a senha é um token de usuário com permissões
        self.sonarqube_url = config.url
        self.sonarqube_token = decrypt_data(config.encrypted_password)
        self.client = SonarQubeClient(sonarqube_url=self.sonarqube_url, token=self.sonarqube_token)

    def provision_project_and_run_scan(self, project_key: str, repo_url: str):
        """
        Cria um projeto, clona o repo e executa o sonar-scanner.
        Retorna o project_key para referência futura.
        """
        # 1. Criar o projeto no SonarQube
        try:
            self.client.projects.create_project(project=project_key, name=project_key)
            print(f"Projeto {project_key} criado no SonarQube.")
        except Exception as e:
            # Ignorar se o projeto já existe
            if "already exists" in str(e):
                print(f"Projeto {project_key} já existe no SonarQube.")
            else:
                raise

        # 2. Gerar um token de análise para este projeto
        token_response = self.client.user_tokens.generate_user_token(name=f"token-{project_key}")
        analysis_token = token_response['token']

        # 3. Clonar o repositório
        temp_dir = tempfile.mkdtemp()
        print(f"Clonando {repo_url} para {temp_dir}...")
        try:
            subprocess.run(["git", "clone", "--depth", "1", repo_url, temp_dir], check=True)

            # 4. Executar o sonar-scanner via Docker
            docker_command = [
                "docker", "run", "--rm",
                "--network", "host", # Para acessar o SonarQube rodando localmente
                "-v", f"{temp_dir}:/usr/src",
                "sonarsource/sonar-scanner-cli",
                "sonar-scanner",
                f"-Dsonar.projectKey={project_key}",
                f"-Dsonar.sources=.",
                f"-Dsonar.host.url={self.sonarqube_url}",
                f"-Dsonar.login={analysis_token}"
            ]
            print("Executando o container do sonar-scanner...")
            subprocess.run(docker_command, check=True, capture_output=True, text=True)
            print("Análise do SonarQube concluída.")

            return project_key

        finally:
            # 5. Limpar
            print(f"Limpando diretório temporário: {temp_dir}")
            shutil.rmtree(temp_dir)
            # Revogar o token de análise para não deixar lixo
            self.client.user_tokens.revoke_user_token(name=f"token-{project_key}")

    def get_scan_results(self, project_key: str) -> list:
        """
        Busca os 'issues' de um projeto no SonarQube.
        """
        issues = self.client.issues.search_issues(componentKeys=project_key)
        return list(issues) # A biblioteca retorna um gerador
