from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from database import Base
import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="user")  # user/admin

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    date = Column(Date)
    location = Column(String)
    description = Column(String)
    capacity = Column(Integer)

# class Booking(Base):
#     __tablename__ = "bookings"
#     id = Column(Integer, primary_key=True, index=True)
#     booking_id = Column(String, unique=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     event_id = Column(Integer, ForeignKey("events.id"))
#     timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # Add relationship
    event = relationship("Event")  