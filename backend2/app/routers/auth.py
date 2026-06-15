from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, models, schemas, auth
from app.database import get_db
from datetime import timedelta
from app.limiter import limiter

router = APIRouter(
    tags=["auth"],
)

@router.post("/login", response_model=schemas.Token)
@limiter.limit("10/minute")
def login_for_access_token(request: Request, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Get user role for claims
    role_names = [role.name for role in user.roles]
    primary_role = role_names[0] if role_names else "customer"
    
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": primary_role, "full_name": user.full_name}, 
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": user
    }
