from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext

app = FastAPI()

# In-memory mock "database"
mock_db = {}

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic model for user creation
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    username: str
    email: EmailStr

# BUSINESS LOGIC: Check if user exists and add to DB
def create_user(user_data: UserCreate) -> UserResponse:
    if user_data.email in mock_db:
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed_password = pwd_context.hash(user_data.password)
    user_record = {
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": hashed_password,
    }

    # Save to mock DB
    mock_db[user_data.email] = user_record
    return UserResponse(username=user_data.username, email=user_data.email)

# API ENDPOINT: Create user
@app.post("/users", response_model=UserResponse)
def register_user(user: UserCreate):
    return create_user(user)
