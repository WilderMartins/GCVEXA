from pydantic import BaseModel

class MFASetupResponse(BaseModel):
    qr_code: str  # Base64 encoded image
    otp_uri: str

class MFAVerify(BaseModel):
    otp_code: str
    # O segredo temporário é enviado do backend para o frontend e de volta
    # para que não precisemos armazená-lo no DB antes da verificação.
    temp_secret: str

class MFALogin(BaseModel):
    otp_code: str
    # Um token temporário emitido após a verificação da senha
    temp_auth_token: str
