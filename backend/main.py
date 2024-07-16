from fastapi import FastAPI, HTTPException, Query, File, UploadFile, Depends, Header
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import sqlite3
import jwt
import os
import aiofiles
import hashlib

app = FastAPI()

# Database connection setup
DATABASE_FILE = 'database.db'

# JWT settings
SECRET_KEY = "62f263cddc7e49b91ab1bcc15b620d53da8a9da0"
SECRET_FILE_KEY = "1e8ca8a5645f660a493a"
UPLOAD_FOLDER = "uploads/"  # Folder to store uploaded files
ALGORITHM = 'HS256'

# Function to generate signature for a given filename
def generate_signature(filename: str) -> str:
    return hashlib.sha256((SECRET_FILE_KEY + filename).encode()).hexdigest()

def generate_signature_bytes(filename: bytes) -> str:
    return hashlib.sha256(SECRET_FILE_KEY.encode() + filename).hexdigest()

# Authentication
security = HTTPBearer()


# Models
class User(BaseModel):
    email: str
    password: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed, "*" allows all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Adjust as needed
    allow_headers=["*"],  # Adjust as needed, "*" allows all headers
)

# Routes
@app.post("/signup")
async def signup(user: User):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (user.email,))
        existing_user = cursor.fetchone()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (user.email, user.password))
        conn.commit()
        return {"message": "User created successfully"}


@app.post("/signin")
async def signin(user: User):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (user.email,))
        db_user = cursor.fetchone()
        
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if db_user[2] != user.password:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = jwt.encode({"email": user.email}, SECRET_KEY, algorithm=ALGORITHM)
        return {"token": token}


@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...), token: HTTPAuthorizationCredentials = Depends(security)):

    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")

    try:
        decoded_token = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Token is invalid")

    filename = file.filename

    filename = filename.replace("../", "")
    filename = filename.replace("..", "")
    filename = filename.replace(" ", "")

    
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (decoded_token["email"],))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        cursor.execute('INSERT INTO files (user_id, filename) VALUES (?, ?)', (user[0], filename))
        conn.commit()
    
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(filepath):
        return {"message": "File already exists"}
    
    async with aiofiles.open(filepath, "wb") as f:
        contents = await file.read()  # Read the file asynchronously
        await f.write(contents)
    
    return {"message": "File uploaded successfully", "filename": filename}


@app.get("/files")
async def get_files(token: HTTPAuthorizationCredentials = Depends(security)):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")

    try:
        decoded_token = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Token is invalid")

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (decoded_token["email"],))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        cursor.execute('SELECT * FROM files WHERE user_id = ?', (user[0],))
        files = cursor.fetchall()

        json_files = [{"id": file[0], "user_id": file[1], "filename": file[2], "signature": generate_signature(file[2])} for file in files]

        return json_files

@app.get("/file")
async def download_file(
    filename: bytes = Query(..., description="Name of the file to download"),
    signature: str = Query(..., description="Signature of the file"),
    token: Optional[str] = Header(None, description="JWT Authorization Token"),
):
    if signature != generate_signature_bytes(filename):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Construct file path
    file_path = os.path.join(UPLOAD_FOLDER.encode(), filename)

    # Check if file exists
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path.decode(), filename=filename.decode())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)