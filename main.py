from fastapi import FastAPI,UploadFile,Form, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from typing import Annotated
import sqlite3


con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

# 테이블이 없으면 생성한다.
cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
	id INTEGER PRIMARY KEY,
	title TEXT NOT NULL,
	image BLOB,
	price INTEGER NOT NULL,
	description TEXT,
	place TEXT NOT NULL,
	createAt INTEGER NOT NULL
);
            """)
app = FastAPI()
# 시크릿정보는 액세스토큰을 어떻게 인코딩할지 정하는 것. 
# 노출되면 디코딩될 수 있으니 노출되지 않도록하자.
SECRET = 'super-coding'
#시크릿, 토큰이 어디서 발급될건지 정하기
manager = LoginManager(SECRET, '/login') 

@app.post('/items')
async def create_item(image:UploadFile, 
                title:Annotated[str,Form()], 
                price:Annotated[int,Form()],  
                description:Annotated[str,Form()], 
                place:Annotated[str,Form()],
                createAt:Annotated[int,Form()]
                ):
    # print(image, title, price, description, place)
    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO items 
                (title,image, price ,description, place, createAt) 
                VALUES 
                ('{title}', '{image_bytes.hex()}', {price} , '{description}','{place}', {createAt})
                """)
    con.commit()
    return '200'

# 이미지불러오기
@app.get('/images/{item_id}')
async def get_image(item_id):
    cur = con.cursor()
    #  16진법으로 가져옴
    image_bytes = cur.execute(f"""
                              SELECT image FROM items WHERE id = {item_id}
                              """).fetchone()[0] #몇 번째 하나만 가져올 때
    return Response(content=bytes.fromhex(image_bytes), media_type="image/*")
    # 16진법으로 된 것을 바꿔서 컨텐츠로 리스폰스 하겠다

# 아이템 불러오기
@app.get("/items")
async def get_items():
    con.row_factory = sqlite3.Row
    #  ㄴ 컬럼명도 같이 가져오는 문법
    cur = con.cursor() #  커넥션의 현재 위치를 커서라고 함. 위치를 업데이트를 해줘야함
    rows = cur.execute(f"""
                       SELECT * FROM items;
                       """).fetchall()
    # fetchall() : 데이터를 가지고오는 문법
  
    return JSONResponse( jsonable_encoder(dict(row) for row in rows))

  
    
# 회원가입 --------------------------------------
@app.post("/signup")
def signup(id:Annotated[str, Form()], 
           password:Annotated[str, Form()],
           name:Annotated[str,Form()],
           email:Annotated[str,Form()]):

    cur.execute(f"""
               INSERT INTO users
               (id, name, email, password)
               VALUES ('{id}' ,'{name}','{email}','{password}') 
                """)
    con.commit()
    return '200'

# 로그인 --------------------------------------
@manager.user_loader()
def query_user(id):
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(f"""
                       SELECT * FROM users WHERE id='{id}'
                       """).fetchone() #하나만 가지고 오기
    return user

    
@app.post("/login")
def signup(id:Annotated[str, Form()], 
           password:Annotated[str, Form()]):
    user = query_user(id)
    
    if not user:
        raise InvalidCredentialsException
        # InvalidCredentialsException : 유효하지 않은 계정정보에 대한 에러처리를 할 수있는 문법이 있음
        # raise : 에러메세지 던져줌
    elif password != user['password']:
        raise InvalidCredentialsException
  
    # 엑세스 토큰 발급하기
    access_token = manager.create_access_token(data={
        'id': user['id'],
        'name':user['name'],
        'email' : user['email']
    })
    return {'access_token': access_token}



# pip install python-multipart
# pip install pastapi-login


# 정적 파일들을 서버에 올림
app.mount("/", StaticFiles(directory="frontEnd", html=True), name="frontEnd")
