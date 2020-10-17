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

    def getdict(self):
        return {"Identity_Proof_No" : self.Identity_Proof_No,
        "State_Ref_Number": self.State_Ref_Number,
        "StateCode": self.StateCode,
        "DistrictCode":self.DistrictCode,
        "Sub_District_Code":self.Sub_District_Code,
        "BlockCode":self.BlockCode,
        "VillageCode":self.VillageCode,
        "Farmer_Name":self.Farmer_Name,
        "Gender":self.Gender,
        "Farmer_Category":self.Farmer_Category,
        "Identity_Proof_Type":self.Identity_Proof_Type,
        "IFSC_Code":self.IFSC_Code,
        "Bank_Account_Number":self.Bank_Account_Number,
        "MobileNo":self.MobileNo,
        "DOB":self.DOB,
        "Father_Mother_Husband_Name":self.Father_Mother_Husband_Name,
        "HomeAddress":self.HomeAddress,
        "Ownership_Single_Joint":self.Ownership_Single_Joint,
        "Sr_No":self.Sr_No,
        "Survey_Khata_No":self.Survey_Khata_No,
        "Khasra_Drag_No":self.Khasra_Drag_No,
        "Area":self.Area,
        "FarmerType":self.FarmerType,
        "IMEI" :self.IMEI}

class WebUser(Base):
    __tablename__ = "WebUser"
    WebUser_Email =  Column(String, unique=True, primary_key=True)
    WebUser_Name =  Column(String)
    WebUser_Contact =  Column(String)
    WebUser_Password =  Column(String)
    WebUser_District =  Column(String)
    WebUser_SubDistrict =  Column(String)
    WebUser_Verified = Column(String)
    WebUser_Role = Column(String)
