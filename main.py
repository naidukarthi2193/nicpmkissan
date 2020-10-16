
from typing import List
import pandas as pd
import uvicorn
import ast
from fastapi.responses import HTMLResponse
from fastapi import Depends, FastAPI, HTTPException ,Request,Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from fastapi.templating import Jinja2Templates
import json
from dotenv import load_dotenv
import os
from starlette.status import HTTP_403_FORBIDDEN

models.Base.metadata.create_all(bind=engine)

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")
COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN")

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
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/delete")
def delete(db: Session = Depends(get_db),api_key: APIKey = Depends(get_api_key)):
    db.query(models.Farmer).delete()
    db.commit()
    return { "status" : "databse Cleared"}

@app.get("/",response_class=HTMLResponse)
def read_root(request: Request,db: Session = Depends(get_db),):
    records = db.query(models.Farmer).all()
    return templates.TemplateResponse("index2.html", {"request": request, "data": records})

@app.get("/data/", response_model=List[schemas.Farmer])
def show_farmer(db: Session = Depends(get_db),api_key: APIKey = Depends(get_api_key)):
    records = db.query(models.Farmer).all()
    return records

@app.post("/add/" , response_model = schemas.Farmer)
def add_farmer(farmer: schemas.Farmer,db: Session = Depends(get_db),api_key: APIKey = Depends(get_api_key)):
    db_user = crud.check_aadhar(db=db , aadhar=farmer.Identity_Proof_No)
    if db_user:
        raise HTTPException(status_code=400 , detail="Farmer already registered")
    return crud.create_user(db=db , farmer=farmer)

@app.get("/check")
def check_farmer(aadhar: str ,db : Session = Depends(get_db),api_key: APIKey = Depends(get_api_key)):
    db_user = crud.check_aadhar(db=db , aadhar=aadhar)
    if db_user:
        raise HTTPException(status_code=400 , detail="Farmer already registered")
    else:
        return { "status" : "Not Registed"}

@app.get("/districts")
def get_districts(api_key: APIKey = Depends(get_api_key)):
    districtslist = list()
    for districts in lgdirectory:
        dist = dict()
        dist['code'] = districts['dis_code']
        dist['name'] = districts['dis_name']
        districtslist.append(dist)
    return districtslist

@app.get("/subdistrict/{dis_code}")
def get_subdistricts(dis_code,api_key: APIKey = Depends(get_api_key)):
    subdistrictslist = list()
    for districts in lgdirectory:
        if districts['dis_code'] == int(dis_code):
            for subdistricts in districts['subdistricts']:
                subdict= dict()
                subdict['code'] = subdistricts['subdis_code']
                subdict['name'] = subdistricts['subdis_name']
                subdistrictslist.append(subdict)
            break
    return subdistrictslist

@app.get("/village/{dis_code}/{subdis_code}")
def get_villages(dis_code,subdis_code,api_key: APIKey = Depends(get_api_key)):
    villageslist = list()
    for districts in lgdirectory:
        if districts['dis_code'] == int(dis_code):
            for subdistricts in districts['subdistricts']:
                if subdistricts['subdis_code'] == int(subdis_code):
                    for villages in subdistricts['villages']:
                        vill_dict = dict()
                        vill_dict['name'] = villages['village_name']
                        vill_dict['code'] = villages['village_code']
                        villageslist.append(vill_dict)
                    break
    return villageslist

@app.get("/block/{dis_code}")
def get_blocks(dis_code,api_key: APIKey = Depends(get_api_key)):
    blocklist = list()
    for districts in lgdirectory:
        if districts['dis_code'] == int(dis_code):
            for block in districts['blocks']:
                block_dict= dict()
                block_dict['code'] = block['block_code']
                block_dict['name'] = block['block_name']
                blocklist.append(block_dict)
            break
    return blocklist

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0')