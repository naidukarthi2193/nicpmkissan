from typing import List
import pandas as pd
import uvicorn
import smtplib
import ast
from fastapi.responses import HTMLResponse
from fastapi import Depends, FastAPI, HTTPException ,Request,Security,Form,APIRouter,Response
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
from cryptography.fernet import Fernet
router = APIRouter()
with open('test.json') as f:
    lgdirectory= json.load(f)
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@router.get("/districts",tags=["APIs"])
def get_lgdirectory_districts():
    districtslist = list()
    for districts in lgdirectory:
        dist = dict()
        dist['code'] = districts['dis_code']
        dist['name'] = districts['dis_name']
        districtslist.append(dist)
    return districtslist

@router.get("/subdistrict/{dis_code}",tags=["APIs"])
def get_lgdirectory_subdistricts(dis_code):
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

@router.get("/village/{dis_code}/{subdis_code}",tags=["APIs"])
def get_lgdirectory_villages(dis_code,subdis_code):
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

@router.get("/block/{dis_code}",tags=["APIs"])
def get_lgdirectory_blocks(dis_code):
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

@router.post("/add/" , response_model = schemas.Farmer,tags=["APIs"])
def add_new_farmer(farmer: schemas.Farmer,db : Session = Depends(get_db)):
    db_user = crud.check_aadhar(db=db , aadhar=farmer.Identity_Proof_No)
    if db_user:
        raise HTTPException(status_code=400 , detail="Farmer already registered")
    return crud.create_user(db=db , farmer=farmer)

@router.get("/check",tags=["APIs"])
def check_farmer(aadhar: str,db : Session = Depends(get_db)):
    db_user = crud.check_aadhar(db=db , aadhar=aadhar)
    if db_user:
        raise HTTPException(status_code=400 , detail="Farmer already registered")
    else:
        return { "status" : "Not Registed"}

@router.get("/data/", response_model=List[schemas.Farmer],tags=["APIs"])
def list_all_farmers(db : Session = Depends(get_db)):
    records = db.query(models.Farmer).all()
    return records

@router.get("/delete",tags=["APIs"])
def delete_all_farmers(db : Session = Depends(get_db)):
    db.query(models.Farmer).delete()
    db.commit()
    return { "status" : "databse Cleared"}

@router.get("/getallwebusers",tags=["APIs"], response_model=List[schemas.WebUser])
def get_all_webusers(db : Session = Depends(get_db)):
    return crud.get_all_webusers(db=db)

@router.post("/verifyuser",tags=["APIs"], response_model=schemas.WebUser)
def verifyuser(email :str,db : Session = Depends(get_db)):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 587 )
        server.ehlo()
        server.login("karthikraj.v17@siesgst.ac.in", "Kar123thik456")
        server.sendmail("karthikraj.v17@siesgst.ac.in", email, "YOUR ACCOUNT HAS BEEN VERIFIED")
        server.close()

        print ('Email sent!')
    except:
        print ('Something went wrong...')
    return crud.verify_user(db=db,email=email)

