import pyotp
import qrcode
import io
import base64
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .... import crud, models, schemas
from ....api import deps
from ....core.encryption import encrypt_data, decrypt_data

router = APIRouter()

@router.post("/setup", response_model=schemas.MFASetupResponse)
def setup_mfa(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Generate a new TOTP secret and QR code for the user to set up MFA.
    """
    if current_user.mfa_enabled:
        raise HTTPException(status_code=400, detail="MFA is already enabled.")

    # Gerar um novo segredo
    temp_secret = pyotp.random_base32()

    # Gerar a URI de provisionamento
    otp_uri = pyotp.totp.TOTP(temp_secret).provisioning_uri(
        name=current_user.email, issuer_name="GCV"
    )

    # Gerar o QR code
    img = qrcode.make(otp_uri)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    qr_code_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {"qr_code": qr_code_b64, "otp_uri": temp_secret} # Retornar o segredo temporário

@router.post("/verify")
def verify_mfa(
    *,
    db: Session = Depends(deps.get_db),
    mfa_in: schemas.MFAVerify,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Verify the TOTP code and enable MFA for the user.
    """
    totp = pyotp.TOTP(mfa_in.temp_secret)
    if not totp.verify(mfa_in.otp_code):
        raise HTTPException(status_code=400, detail="Invalid OTP code.")

    # Salvar o segredo criptografado e habilitar MFA
    current_user.mfa_secret = encrypt_data(mfa_in.temp_secret)
    current_user.mfa_enabled = True
    db.add(current_user)
    db.commit()

    return {"msg": "MFA enabled successfully."}
