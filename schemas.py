from pydantic import BaseModel
from datetime import date
from pydantic import BaseModel
from datetime import datetime
# Users
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Events
class EventCreate(BaseModel):
    title: str
    date: date
    location: str
    description: str
    capacity: int

class EventResponse(BaseModel):
    id: int
    title: str
    date: date
    location: str
    description: str
    capacity: int

    class Config:
        orm_mode = True

# Bookings
class BookingCreate(BaseModel):
    event_id: int

from schemas import EventResponse

class BookingResponse(BaseModel):
    id: int
    booking_id: str
    user_id: int
    event_id: int
    timestamp: datetime
    event: EventResponse  # nested event details

    class Config:
        orm_mode = True
