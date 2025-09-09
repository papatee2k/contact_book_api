import email
from pydantic import BaseModel, EmailStr
from typing import List, Optional

# creating the contactBase class
class contactBase(BaseModel):
    first_name: str
    last_name: str
    phone_numbers: List[str]
    emails: Optional[List[EmailStr]] = []
    address: Optional[str] = None
    birthday: Optional[str] = None
    notes: Optional[str] = None
    favorite: Optional[bool] = False

# contact create
class contactCreate(contactBase):
    pass

# ContactUpdate is basically ContactBase, but first_name and last_name
# are optional (set to None) so they can be skipped when updating.
class contactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_numbers: Optional[List[str]] = None
    emails: Optional[List[EmailStr]] = None
    address: Optional[str] = None
    birthday: Optional[str] = None
    notes: Optional[str] = None
    favorite: Optional[bool] = None

# contactout 

class contactOut(contactBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
