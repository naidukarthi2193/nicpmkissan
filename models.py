from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from database import Base



class Farmer(Base):
    __tablename__ = "Farmers"
    Identity_Proof_No = Column(String, unique=True, primary_key=True)
    State_Ref_Number= Column(String)
    StateCode= Column(String)
    DistrictCode= Column(String)
    Sub_District_Code= Column(String)
    BlockCode= Column(String)
    VillageCode= Column(String)
    Farmer_Name= Column(String)
    Gender= Column(String)
    Farmer_Category= Column(String)
    Identity_Proof_Type= Column(String)
    IFSC_Code= Column(String)
    Bank_Account_Number= Column(String)
    MobileNo= Column(String)
    DOB= Column(String)
    Father_Mother_Husband_Name= Column(String)
    HomeAddress= Column(String)
    Ownership_Single_Joint= Column(String)
    Sr_No= Column(String)
    Survey_Khata_No= Column(String)
    Khasra_Drag_No= Column(String)
    Area= Column(String)
    FarmerType= Column(String)
    IMEI = Column(String)
