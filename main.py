from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import starlette.status as status
import bcrypt
import sqlite3
import jwt
from datetime import datetime, timedelta
from fastapi.templating import Jinja2Templates
import os
from builtins import sum

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

conn = sqlite3.connect('./databases/database.db')
cursor = conn.cursor()

secret_key = 'muffin'
app.add_middleware(SessionMiddleware, secret_key=secret_key)

templates = Jinja2Templates(directory="templates")

def get_token(request: Request):
    token = request.cookies.get('token')
    return token

databases_folder = "databases"

@app.post("/register")
async def register(request: Request, usernameRegister: str = Form(...), passwordRegister: str = Form(...)):
    cursor.execute('SELECT * FROM users WHERE username = ?', (usernameRegister,))
    existing_user = cursor.fetchone()

    if existing_user:
        return {"message":"User already exists"}

    passwordHashed = bcrypt.hashpw(passwordRegister.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute("INSERT INTO users (userName, password) VALUES (?, ?)", (usernameRegister, passwordHashed))
    conn.commit()
    expiration = datetime.utcnow() + timedelta(minutes=30)
    payload = {
        'user_id': usernameRegister,
        'exp': expiration
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    response = RedirectResponse('/index', status_code=status.HTTP_302_FOUND)
    # Set the token as a cookie in the response
    response.set_cookie(key='token', value=token, httponly=True)

    
    

    # Create a new database for the user
    user_db = os.path.join(databases_folder, f"{usernameRegister}.db")
    new_conn = sqlite3.connect(user_db)

    # Create a new table inside the user's database
    create_table_query = """
    CREATE TABLE IF NOT EXISTS score (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userName TEXT NOT NULL,
        score INTEGER NOT NULL
    )
    """
    new_conn.execute(create_table_query)
    new_conn.commit()

    new_conn.close()


    return response

@app.post("/login")
async def login(request: Request, usernameLogin: str = Form(...), passwordLogin: str = Form(...)):

    cursor.execute('SELECT * FROM users WHERE username = ?', (usernameLogin,))
    user = cursor.fetchone()

    if user:
        stored_password = user[2]

        if bcrypt.checkpw(passwordLogin.encode('utf-8'), stored_password.encode('utf-8')):
            # Generate the JWT token
            expiration = datetime.utcnow() + timedelta(minutes=30)
            payload = {
                'user_id': usernameLogin,
                'exp': expiration
            }
            token = jwt.encode(payload, secret_key, algorithm='HS256')

            response = RedirectResponse('/index', status_code=status.HTTP_302_FOUND)
            # Set the token as a cookie in the response
            response.set_cookie(key='token', value=token, httponly=True)
            return response
        else:
            return RedirectResponse(url='/login', status_code=status.HTTP_302_FOUND)
    else:
        return RedirectResponse(url='/login', status_code=status.HTTP_302_FOUND)


## Get pages
@app.get("/")
async def main():
    return FileResponse('templates/index.html')

@app.get("/login")
async def show_login():
    return FileResponse('templates/login.html')

@app.get("/register")
async def show_register():
    return FileResponse('templates/register.html')

@app.get("/index")
async def show_index(request: Request, token: str = Depends(get_token)):
    if token:
        try:
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = decoded_token.get('user_id')
            # Pass the user_id to the template
            return templates.TemplateResponse("index.html", {"request": request, "user_id": user_id})
        except jwt.ExpiredSignatureError:
            return templates.TemplateResponse("index.html", {"request": request, "user_id": 'Guest'})
        except jwt.InvalidTokenError:
            raise templates.TemplateResponse("index.html", {"request": request, "user_id": 'Guest'})
    else:
        return templates.TemplateResponse("index.html", {"request": request, "user_id": 'Guest'})

@app.get("/get_username")
async def get_username(request: Request, token: str = Depends(get_token)):
    if token:
        try:
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = decoded_token.get('user_id')
            print(user_id)
            return {"username": user_id}
        except jwt.ExpiredSignatureError:
            return {"username": 'Guest'}
        #HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
    else:
        return {"username": 'Guest'}
    
@app.post("/add_score")
async def add_score(request: Request, score_data: dict):
    username = score_data.get('username')
    score = score_data.get('score')

    # Insert a new row with the name and score
    user_db = os.path.join(databases_folder, f"{username}.db")
    conn = sqlite3.connect(user_db)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO score (username, score) VALUES (?, ?)", (username, score))
    conn.commit()

    cursor.close()
    conn.close()

    return

@app.get("/calculate_average")
async def calculate_average(request: Request, username: str = Depends(get_username)):
    if username:
        try:
            username = username['username']
            user_db = os.path.join(databases_folder, f"{username}.db")
            conn = sqlite3.connect(user_db)
            cursor = conn.cursor()

            cursor.execute("SELECT score FROM score")
            scores = cursor.fetchall()

            total_scores = len(scores)
            sum_scores = 0
            sum_scores = sum(score[0] for score in scores)
            average_score = sum_scores / total_scores if total_scores > 0 else 0
            average_score = round(average_score,2)
            cursor.close()
            conn.close()

            return {"average_score": average_score}
        except Exception as e:
            print(e)  # Print the exception for debugging purposes
            return {"average_score": "Error calculating average score"}
    else:
        return {"average_score": "Log in to see average score"}

