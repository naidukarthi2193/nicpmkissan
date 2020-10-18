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
    final = [dict(t) for t in {tuple(d.items()) for d in districtslist}]
    return sorted(final, key = lambda final: final['name'])

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
    return sorted(subdistrictslist, key = lambda subdistrictslist: subdistrictslist['name'])

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
    final = [dict(t) for t in {tuple(d.items()) for d in villageslist}]
    return sorted(final, key = lambda final: final['name'])

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
    return sorted(blocklist, key = lambda blocklist: blocklist['name'])

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
        s = smtplib.SMTP(os.getenv("SMTP_DOMAIN"), int(os.getenv("SMTP_PORT"))) 
        s.starttls() 
        s.login(os.getenv("SMTP_SENDER_EMAIL"), os.getenv("SMTP_SENDER_PASSWORD"))  
        message = """\
        Subject: PM KISSAN USER ADDED

        Your Request for User Regeisteration has been Accepted 
        Please Visit the Website for Logging In
        """
        s.sendmail(os.getenv("SMTP_SENDER_EMAIL"), email, message)  
        s.quit() 
        print ('Email sent!')
    except:
        print ('Something went wrong...')
    return crud.verify_user(db=db,email=email)

@router.post("/deleteuser",tags=["APIs"])
def deleteuser(email:str,db:Session = Depends(get_db)):
    if (crud.delete_webuser(db=db,email=email)):
        try:
            s = smtplib.SMTP(os.getenv("SMTP_DOMAIN"), int(os.getenv("SMTP_PORT"))) 
            s.starttls() 
            s.login(os.getenv("SMTP_SENDER_EMAIL"), os.getenv("SMTP_SENDER_PASSWORD"))  
            message = """\
            Subject: PM KISSAN USER DELETED

            Your Registeration has be DELETED by the Admin
            Please Re-Register or Contact Admin For Clarity at {}
            """.format(os.getenv("ADMIN_EMAIL"))
            s.sendmail(os.getenv("SMTP_SENDER_EMAIL"), email, message)  
            s.quit() 
            print ('Email sent!')
            return {"status": "User Deleted"}
        except:
            return {"status" : "Some Error"}
        
    else:
        return {"status" : "Some Error"}