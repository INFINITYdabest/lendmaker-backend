from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import UserCreate, UserResponse, VerifyUser, AddPublicKey
from app.models import User
from app.database import db
from app.utils import get_password_hash, verify_password, create_access_token, encode_private_key, get_current_user
from datetime import timedelta
from web3 import Web3

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/verify-or-register", response_model=UserResponse)
def verify_user(user: UserCreate):
    """
    Verifies if a user exists in the database. If not, registers the user.

    Args:
        user (UserCreate): The user details required for verification or registration.

    Returns:
        UserResponse: The response model containing the user details.
    """
    db_user = db.users.find_one({"_id": user.uuid})
    if not db_user:
        user_dict = user.dict()
        user_dict["friends"] = []
        user_dict["_id"] = user.uuid
        user_dict.pop("uuid")
        db.users.insert_one(user_dict)
        return UserResponse(**user_dict)
    return UserResponse(**db_user)

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    """
    Registers a new user.

    This endpoint allows for the registration of a new user by providing the necessary user details.
    It checks if the email or user ID is already registered in the database and raises an HTTPException
    if either is found. If the user is not already registered, it inserts the new user into the database
    and returns the user details.

    Args:
        user (UserCreate): The user details required for registration.

    Returns:
        UserResponse: The response model containing the registered user details.

    Raises:
        HTTPException: If the email is already registered.
        HTTPException: If the user ID is already registered.
    """
    user_dict = user.dict()
    user_dict["friends"] = []
    user_dict["_id"] = user.uuid
    user_dict.pop("uuid")
    if db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.users.find_one({"_id": user.uuid}):
        raise HTTPException(status_code=400, detail="User already registered")
    db.users.insert_one(user_dict)
    return UserResponse(**user_dict)

@router.post("/login")
def login(user: VerifyUser):
    """
    Authenticates a user and returns an access token.

    Args:
        user (VerifyUser): The user details required for authentication.

    Returns:
        dict: A dictionary containing the access token, token type, and user details.
    """
    db_user = db.users.find_one({"_id": user.uuid})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user["_id"]}, expires_delta=access_token_expires)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(**db_user)
    }

@router.post("/add-public-key", response_model=AddPublicKey)
def add_public_key(public_key: AddPublicKey, current_user: User = Depends(get_current_user)):
    """
    Adds a public key to the current user's profile.

    Args:
        public_key (AddPublicKey): The public key to be added.
        current_user (User): The current authenticated user.

    Returns:
        AddPublicKey: The response model containing the added public key.

    Raises:
        HTTPException: If the public key is already present.
    """
    user = db.users.find_one({"_id": current_user.id})
    if user["public_key"]:
        raise HTTPException(status_code=400, detail="Public key already exists")
    db.users.update_one({"_id": current_user.id}, {"$set": {"public_key": Web3.to_checksum_address(public_key.public_key)}})
    return public_key