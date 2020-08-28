
from typing import List

import uvicorn
from fastapi.responses import HTMLResponse

from fastapi import Depends, FastAPI, HTTPException ,Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
# from starlette.responses import RedirectResponse

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

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0')