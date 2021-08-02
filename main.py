
import ast
import json
import os
from typing import List, Optional

import pandas as pd
import uvicorn
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from fastapi import (Depends, FastAPI, Form, HTTPException, Request, Response,
                     Security)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security.api_key import (APIKey, APIKeyCookie, APIKeyHeader,
                                      APIKeyQuery)
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.status import HTTP_403_FORBIDDEN

import apis
import crud
import models
import schemas
from database import SessionLocal, engine

file = open('passwordkey.key', 'rb')  # Open the file as wb to read bytes
key = file.read()  # The key will be type bytes
file.close()
encryptkey = Fernet(key)

models.Base.metadata.create_all(bind=engine)

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")
COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

with open('test.json') as f:
    lgdirectory= json.load(f)

async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),):

    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Could not validate redentials")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

app.include_router(
    apis.router,
    tags=["APIs"],
    dependencies=[Depends(get_db),Depends(get_api_key)],
    responses={404: {"description": "Not found"}},
)

@app.get("/")
def form_post(request: Request ):
    return templates.TemplateResponse('homepage.html', context={'request': request})

@app.post("/deletewebuser")
def deletewebuser(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)):
    if role == "Admin":
        if email == ADMIN_EMAIL and  password == ADMIN_PASSWORD:
            return RedirectResponse( url=f'/deletebyadmin/' ) 
        else:
            return templates.TemplateResponse('detailsnotfound.html', context={'request': request})

@app.post("/deletebyadmin")
def deletebyadmin(request: Request,db : Session = Depends(get_db)):
    data =  crud.get_all_webusers(db=db)
    return templates.TemplateResponse('deleteuser.html', context={'request': request,"data":data})

@app.post("/checklogin/")
def webuser_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    db : Session = Depends(get_db)
    ):
    enc_password = encryptkey.encrypt(password.encode()).decode("utf-8")
    enc_email = encryptkey.encrypt(email.encode()).decode("utf-8")
    if role == "Admin":
        if email == ADMIN_EMAIL and  password == ADMIN_PASSWORD:
            return RedirectResponse( url=f'/verifiedadmin/'+enc_email ) 
        return templates.TemplateResponse('detailsnotfound.html', context={'request': request})
    db_user = crud.check_webuser_login(db=db , email=email,password=password)

    print(db_user)
    if db_user == None :
        return templates.TemplateResponse('detailsnotfound.html', context={'request': request})
    else:
        if db_user.WebUser_Verified=="0":
            return templates.TemplateResponse('newusercreated.html', context={'request': request}) 
        if role == "Collector":
            return RedirectResponse( url=f'/verifiedcollector/'+enc_email +f'/'+encryptkey.encrypt(db_user.WebUser_District.encode()).decode("utf-8"))
        else:

            enc_district =  encryptkey.encrypt(db_user.WebUser_District.encode()).decode("utf-8")
            enc_subdistrict =  encryptkey.encrypt(db_user.WebUser_SubDistrict.encode()).decode("utf-8")
            return RedirectResponse( url='/database/{}/{}/'.format(enc_district,enc_subdistrict))
   
@app.post("/database/")
def getfarmerdatabase(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    db : Session = Depends(get_db)
    ):
    enc_password = encryptkey.encrypt(password.encode()).decode("utf-8")
    enc_email = encryptkey.encrypt(email.encode()).decode("utf-8")
    if role == "Admin":
        if email == ADMIN_EMAIL and  password == ADMIN_PASSWORD:
            records = crud.get_all(db=db)
            return templates.TemplateResponse("index2.html", {"request": request, "data": records}) 

        return templates.TemplateResponse('detailsnotfound.html', context={'request': request})
    db_user = crud.check_webuser_login(db=db , email=email,password=password)
    if db_user == None :
        return templates.TemplateResponse('detailsnotfound.html', context={'request': request})
    else:
        district = db_user.WebUser_District
        subdistrict = db_user.WebUser_SubDistrict
        if db_user.WebUser_Verified=="0":
            return templates.TemplateResponse('newusercreated.html', context={'request': request}) 
        if role == "Collector":
            records = crud.get_collector_farmers(db=db,district=district)
            return templates.TemplateResponse("index2.html", {"request": request, "data": records})
        else:
            records = crud.get_tehsildar_farmers(db=db,district=district,subdistrict=subdistrict)
            return templates.TemplateResponse("index2.html", {"request": request, "data": records})

@app.post("/addwebuser")
def webuser_add(
    request: Request,
    add_email: str = Form(...),
    add_password: str = Form(...),
    add_role: str = Form(...),
    add_contact: str = Form(...),
    add_name: str = Form(...),
    add_district: str = Form(...),
    add_subdistrict : Optional[str] = Form(None),
    db: Session = Depends(get_db)
    ):
    print(add_role)
    print(add_district,add_subdistrict)
    if add_role == "Collector":
        add_subdistrict="0"
    newWebuser = schemas.WebUser(
        WebUser_Email = add_email,
        WebUser_Name =add_name,
        WebUser_Contact =add_contact,
        WebUser_Password =encryptkey.encrypt(add_password.encode()).decode("utf-8"),
        WebUser_District =add_district,
        WebUser_SubDistrict =add_subdistrict,
        WebUser_Verified ="0",
        WebUser_Role = add_role
    )
    if crud.create_WebUser(db=db, webuser = newWebuser) ==None:
        raise HTTPException(status_code=400 , detail="Details Not Found") 
    else:
        return templates.TemplateResponse('newusercreated.html', context={'request': request})

@app.post("/verifiedadmin/{enc_email}")
def verifiedadmin(enc_email,request: Request,db : Session = Depends(get_db)):
    email=encryptkey.decrypt(bytes(enc_email, 'utf-8') ).decode("utf-8") 
    data =  crud.get_unverfied_webusers(db=db)
    return templates.TemplateResponse('verifiedadmin.html', context={'request': request,"data":data})

@app.post("/verifiedcollector/{enc_email}/{enc_district}")
def verifiedcollector(enc_email,enc_district,request: Request,db : Session = Depends(get_db)):
    email=encryptkey.decrypt(bytes(enc_email, 'utf-8') ).decode("utf-8")
    district = encryptkey.decrypt(bytes(enc_district, 'utf-8') ).decode("utf-8")
    data =  crud.get_unverfied_tehsildar(db=db,district=district)
    return templates.TemplateResponse('verifiedadmin.html', context={'request': request,"data":data})

@app.get("/downloadxml/{id_no}")
def get_farmer_by_id(id_no:str,db:Session = Depends(get_db)):
    data =  crud.getfarmerbyid(db,id_no)
    return Response(content=str(data), media_type="application/xml")

if __name__ == "__main__":
    # release
    uvicorn.run(app, host='0.0.0.0')
    # debug
    # uvicorn.run(app)
    
