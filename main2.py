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
@app.post("/users/login")
def login_user(user: UserCreate):
    user_record = mock_db.get(user.email)
    if not user_record or not pwd_context.verify(user.password, user_record["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    
    return {"message": "Login successful", "username": user_record["username"]}
# API ENDPOINT: Get user
@app.get("/users/{email}", response_model=UserResponse)
def get_user(email: str):
    user_record = mock_db.get(email)
    if not user_record:
        raise HTTPException(status_code=404, detail="User not found.")
    
    return UserResponse(username=user_record["username"], email=user_record["email"])
# API ENDPOINT: Delete user
@app.delete("/users/{email}")
def delete_user(email: str):
    if email not in mock_db:
        raise HTTPException(status_code=404, detail="User not found.")
    
    del mock_db[email]
    return {"message": "User deleted successfully"}
# API ENDPOINT: Update user
@app.put("/users/{email}", response_model=UserResponse)
def update_user(email: str, user: UserCreate):
    if email not in mock_db:
        raise HTTPException(status_code=404, detail="User not found.")
    
    # Update user data
    mock_db[email]["username"] = user.username
    mock_db[email]["email"] = user.email
    return UserResponse(username=user.username, email=user.email)
@app.put("/users2/{email}", response_model=UserResponse)
def update_user(email: str, user: UserCreate):
    if email not in mock_db:
        raise HTTPException(status_code=404, detail="User not found.")
    
    # Update user data
    mock_db[email]["username"] = user.username
    # mock_db[email]["email"] = user.email
    return UserResponse(username=user.username, email=user.email)
# API ENDPOINT: List all users
@app.get("/users")
def list_users():
    return [UserResponse(username=user["username"], email=user["email"]) for user in mock_db.values()]