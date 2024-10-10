from fastapi import FastAPI,Form
from typing import Annotated
import sqlite3
import hashlib

# 해시 비밀번호 만들기

# 축약ver
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# 주석 ver
def hash_password(password):
    # 비밀번호를 바이트 형식으로 변환
    password_bytes = password.encode('utf-8')
    # SHA-256 해시 생성
    hash_object = hashlib.sha256(password_bytes)
    # 해시 값을 16진수로 변환
    hashed_password = hash_object.hexdigest()
    return hashed_password


con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()
app = FastAPI()

@app.post("/signup")
def signup(id:Annotated[str, Form()], 
           password:Annotated[str, Form()],
           name:Annotated[str,Form()],
           email:Annotated[str,Form()]):
    hashed = hash_password(password)
    cur.execute(f"""
               INSERT INTO users
               (id, name, email, password)
               VALUES ('{id}' ,'{name}','{email}','{hashed}') 
                """)
    con.commit()
    return '200'