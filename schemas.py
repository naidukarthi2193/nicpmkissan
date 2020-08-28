from pydantic import BaseModel

class Farmer(BaseModel):
    Identity_Proof_No: str
    State_Ref_Number: str
    StateCode: str
    DistrictCode: str
    Sub_District_Code: str
    BlockCode: str
    VillageCode: str
    Farmer_Name: str
    Gender: str
    Farmer_Category: str
    Identity_Proof_Type: str
    IFSC_Code: str
    Bank_Account_Number: str
    MobileNo: str
    DOB: str
    Father_Mother_Husband_Name: str
    HomeAddress: str
    Ownership_Single_Joint: str
    Sr_No: str
    Survey_Khata_No: str
    Khasra_Drag_No: str
    Area: str
    FarmerType: str
    IMEI : str

    class Config:
        orm_mode = True
