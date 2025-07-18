from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import pyotp

from fastapi import Request
from starlette.responses import HTMLResponse, RedirectResponse
from .... import crud, schemas
from ....core import security
from ....core.encryption import decrypt_data
from ....core.oauth import oauth
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

@router.get('/login/google')
async def login_google(request: Request):
    redirect_uri = request.url_for('auth_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/auth/google')
async def auth_google(request: Request, db: Session = Depends(deps.get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        return HTMLResponse(f'<h1>Error: {e}</h1>')

    user_info = token.get('userinfo')
    if not user_info:
        return HTMLResponse('<h1>Could not retrieve user info.</h1>')

    email = user_info['email']
    user = crud.user.get_user_by_email(db, email=email)

    if not user:
        new_user = schemas.UserCreate(
            email=email,
            full_name=user_info.get('name', ''),
            password=security.get_password_hash(pyotp.random_base32()) # Senha aleatória, já que o login é social
        )
        user = crud.user.create_user(db, obj_in=new_user)

    access_token_expires = timedelta(minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.email,
        expires_delta=access_token_expires,
        data={"roles": [role.name for role in user.roles]}
    )

    # Redirecionar para o frontend com o token
    # Idealmente, a URL base do frontend viria das configurações
    frontend_url = f"http://localhost:5173/login/callback?token={access_token}"
    return RedirectResponse(url=frontend_url)
