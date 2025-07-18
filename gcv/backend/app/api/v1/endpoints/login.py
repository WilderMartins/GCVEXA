from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import pyotp

from .... import crud, schemas
from ....core import security
from ....core.encryption import decrypt_data
from ....api import deps

router = APIRouter()

@router.post("/login/access-token")
def login_access_token(
    response: Response,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login.
    Handles password verification and MFA step-up.
    """
    user = crud.user.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # Se MFA estiver habilitado, iniciar o fluxo de segundo fator
    if user.mfa_enabled:
        temp_token_expires = timedelta(minutes=5)
        temp_token = security.create_access_token(
            subject=user.email,
            expires_delta=temp_token_expires,
            data={"mfa_pending": True}
        )
        response.status_code = status.HTTP_202_ACCEPTED
        return {"mfa_required": True, "temp_auth_token": temp_token}

    # Se MFA não estiver habilitado, emitir o token de acesso final
    access_token_expires = timedelta(minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.email,
        expires_delta=access_token_expires,
        data={"roles": [role.name for role in user.roles]}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/login/mfa", response_model=schemas.Token)
def login_mfa(
    *,
    db: Session = Depends(deps.get_db),
    mfa_in: schemas.MFALogin,
):
    """
    Verify MFA code and issue final access token.
    """
    try:
        payload = security.jwt.decode(
            mfa_in.temp_auth_token, security.settings.SECRET_KEY, algorithms=[security.settings.ALGORITHM]
        )
        if not payload.get("mfa_pending"):
            raise HTTPException(status_code=400, detail="Invalid temporary token.")

        email = payload.get("sub")
        user = crud.user.get_user_by_email(db, email=email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

    except security.jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired temporary token.")

    # Verificar o código TOTP
    decrypted_secret = decrypt_data(user.mfa_secret)
    totp = pyotp.TOTP(decrypted_secret)
    if not totp.verify(mfa_in.otp_code):
        raise HTTPException(status_code=400, detail="Invalid OTP code.")

    # Emitir o token de acesso final
    access_token_expires = timedelta(minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.email,
        expires_delta=access_token_expires,
        data={"roles": [role.name for role in user.roles]}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.post("/users/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
):
    """
    Create new user.
    """
    user = crud.user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create_user(db=db, obj_in=user_in)
    return user

@router.get("/users/me", response_model=schemas.User)
def read_users_me(
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get current user.
    """
    return current_user
