
from typing import List
import pandas as pd
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi import Depends, FastAPI, HTTPException ,Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from fastapi.templating import Jinja2Templates

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

villages = pd.read_csv("cleaned_villages.csv")
block = pd.read_csv("blocks.csv",sep=";")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/delete")
def delete(db: Session = Depends(get_db)):
    db.query(models.Farmer).delete()
    db.commit()
    return { "status" : "databse Cleared"}

@app.get("/",response_class=HTMLResponse)
def read_root(request: Request,db: Session = Depends(get_db)):
    records = db.query(models.Farmer).all()
    return templates.TemplateResponse("index.html", {"request": request, "data": records})

@app.get("/data/", response_model=List[schemas.Farmer])
def show_farmer(db: Session = Depends(get_db)):
    records = db.query(models.Farmer).all()
    return records

@app.post("/add/" , response_model = schemas.Farmer)
def add_farmer(farmer: schemas.Farmer,db: Session = Depends(get_db)):
    db_user = crud.check_aadhar(db=db , aadhar=farmer.Identity_Proof_No)
    if db_user:
        raise HTTPException(status_code=400 , detail="Farmer already registered")
    return crud.create_user(db=db , farmer=farmer)

@app.get("/check")
def check_farmer(aadhar: str ,db : Session = Depends(get_db)):
    db_user = crud.check_aadhar(db=db , aadhar=aadhar)
    if db_user:
        raise HTTPException(status_code=400 , detail="Farmer already registered")
    else:
        return { "status" : "Not Registed"}

@app.get("/districts")
def get_districts():
    village_code = sorted(list(set(villages["District Code"])))
    village_name = sorted(list(set(villages["District Name (In English)"])))
    response = list()
    for i in range(len(village_code)):
        temp = dict()
        temp['code'] = village_code[i]
        temp['name'] = village_name[i]
        response.append(temp)
    return response

@app.get("/subdistrict/{dis_code}")
def get_subdistricts(dis_code):
    temp_village = villages.loc[villages["District Code"] == int(dis_code)]

    village_code = sorted(list(set(temp_village["Sub-District Code"])))
    village_name = sorted(list(set(temp_village["Sub-District Name (In English)"])))
    response = list()
    for i in range(len(village_code)):
        temp = dict()
        temp['code'] = village_code[i]
        temp['name'] = village_name[i]
        response.append(temp)
    return response

@app.get("/village/{dis_code}")
def get_villages(dis_code):
    temp_village = villages.loc[villages["Sub-District Code"] == int(dis_code)]
    village_code = sorted(list(set(temp_village["Village Code"])))
    village_name = sorted(list(set(temp_village["Village Name (In Englsih)"])))
    response = list()
    for i in range(len(village_code)):
        temp = dict()
        temp['code'] = village_code[i]
        temp['name'] = village_name[i]
        response.append(temp)
    return response

@app.get("/block/{dis_code}")
def get_blocks(dis_code):
    temp_village = block.loc[block["District Code"] == int(dis_code)]
    village_code = sorted(list(set(temp_village["Block Code"])))
    village_name = sorted(list(set(temp_village["Block Name                      (In English)"])))
    response = list()
    for i in range(len(village_code)):
        temp = dict()
        temp['code'] = village_code[i]
        temp['name'] = village_name[i]
        response.append(temp)
    return response

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0')