from sqlalchemy.orm import Session
import models ,  schemas

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

def get_all(db:Session):
    return db.query(models.Farmer).all()

def check_aadhar(db: Session, aadhar: str):
    return db.query(models.Farmer).filter(models.Farmer.Identity_Proof_No == aadhar).first()