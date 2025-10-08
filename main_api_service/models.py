from pydantic import BaseModel

class UserLocationModel(BaseModel):
    lat: float
    long: float
    email: str