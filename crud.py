from sqlalchemy.orm import Session
import models ,  schemas
from json2xml import json2xml
from json2xml.utils import readfromurl, readfromstring, readfromjson
import json
import xml.etree.ElementTree as ET

def create_user(db: Session ,  farmer: schemas.Farmer):
    db_user = models.Farmer(
        Identity_Proof_No = farmer.Identity_Proof_No,
        State_Ref_Number= farmer.State_Ref_Number , 
        StateCode= farmer.StateCode , 
        DistrictCode= farmer.DistrictCode , 
        Sub_District_Code= farmer.Sub_District_Code , 
        BlockCode= farmer.BlockCode , 
        VillageCode= farmer.VillageCode , 
        Farmer_Name= farmer.Farmer_Name , 
        Gender= farmer.Gender , 
        Farmer_Category= farmer.Farmer_Category , 
        Identity_Proof_Type= farmer.Identity_Proof_Type , 
        IFSC_Code= farmer.IFSC_Code , 
        Bank_Account_Number= farmer.Bank_Account_Number , 
        MobileNo= farmer.MobileNo , 
        DOB= farmer.DOB , 
        Father_Mother_Husband_Name= farmer.Father_Mother_Husband_Name , 
        HomeAddress= farmer.HomeAddress , 
        Ownership_Single_Joint= farmer.Ownership_Single_Joint , 
        Sr_No= farmer.Sr_No , 
        Survey_Khata_No= farmer.Survey_Khata_No , 
        Khasra_Drag_No= farmer.Khasra_Drag_No , 
        Area= farmer.Area , 
        FarmerType= farmer.FarmerType , 
        IMEI = farmer.IMEI , 
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_WebUser(db:Session, webuser:schemas.WebUser):
    db_user = models.WebUser(
        WebUser_Email =  webuser.WebUser_Email,
        WebUser_Name =  webuser.WebUser_Name,
        WebUser_Contact =  webuser.WebUser_Contact,
        WebUser_Password =  webuser.WebUser_Password,
        WebUser_District =  webuser.WebUser_District,
        WebUser_SubDistrict =  webuser.WebUser_SubDistrict,
        WebUser_Verified = "0" , 
        WebUser_Role = webuser.WebUser_Role
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_webusers(db:Session):
    return db.query(models.WebUser).all()


def get_all(db:Session):
    return db.query(models.Farmer).all()

def check_aadhar(db: Session, aadhar: str):
    return db.query(models.Farmer).filter(models.Farmer.Identity_Proof_No == aadhar).first()

def check_webuser_login(db:Session,email:str,password:str):
    print(password)
    return db.query(models.WebUser).filter((models.WebUser.WebUser_Email == email ) & (models.WebUser.WebUser_Password == password ) ).first()

def get_unverfied_webusers(db:Session):
    return db.query(models.WebUser).filter(models.WebUser.WebUser_Verified == "0").all()

def get_unverfied_tehsildar(db:Session,district:str):
    return db.query(models.WebUser).filter((models.WebUser.WebUser_Verified == "0" )& (models.WebUser.WebUser_District == district ) & ( models.WebUser.WebUser_Role == "Tehsildar")).all()

def get_tehsildar_farmers(db:Session,district:str,subdistrict:str):
    return db.query(models.Farmer).filter((models.Farmer.DistrictCode== district) & ( models.Farmer.Sub_District_Code== subdistrict)).all()

def get_collector_farmers(db:Session,district:str):
    return db.query(models.Farmer).filter(models.Farmer.DistrictCode== district).all()

def getfarmerbyid(db:Session,id_no:str):
    farmer = db.query(models.Farmer).filter(models.Farmer.Identity_Proof_No == id_no).first()
    print(type(json.dumps(farmer.getdict())))
    data =  readfromstring(json.dumps(farmer.getdict()) )
    xmlstring =  json2xml.Json2xml(data,wrapper="Farmer", pretty=True).to_xml()
    return xmlstring


def verify_user(db:Session,email:str):
    db.query(models.WebUser).filter(models.WebUser.WebUser_Email == email).update({models.WebUser.WebUser_Verified:"1"}, synchronize_session = False)
    db.commit()
    db.refresh(db.query(models.WebUser).filter(models.WebUser.WebUser_Email == email).first())
    return db.query(models.WebUser).filter(models.WebUser.WebUser_Email == email).first()

def delete_webuser(db:Session,email:str):
    try:
        user = db.query(models.WebUser).filter(models.WebUser.WebUser_Email == email ).first()
        db.delete(user)
        db.commit()
        return True 
    except:
        return False
