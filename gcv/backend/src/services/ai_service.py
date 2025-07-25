import google.generativeai as genai
from ..core.config import settings
from ..models.vulnerability import Vulnerability

genai.configure(api_key=settings.GEMINI_API_KEY)

def summarize_vulnerability(vulnerability: Vulnerability) -> str:
    """
    Generates a summary and remediation plan for a vulnerability using Gemini.
    """
    if settings.GEMINI_API_KEY == "your_gemini_api_key_here":
        return "Error: Gemini API key not configured."

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Você é um especialista em cibersegurança. A vulnerabilidade a seguir foi encontrada:

    - Título: {vulnerability.name}
    - Descrição: {vulnerability.description}
    - CVSS Score: {vulnerability.cvss_score}
    - Severidade: {vulnerability.severity}

    Sua tarefa é:
    1. Resumir esta vulnerabilidade em 3 frases simples e diretas.
    2. Sugerir um plano de remediação genérico e acionável para um desenvolvedor.

    Formate a resposta de forma clara.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Lidar com possíveis erros da API do Gemini
        return f"Error communicating with AI service: {e}"
