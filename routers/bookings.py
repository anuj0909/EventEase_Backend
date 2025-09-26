from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, relationship
from database import SessionLocal
from models import Booking, Event, User
from schemas import BookingCreate, BookingResponse, EventResponse
from auth import get_current_user
import random, string, datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_booking_id():
    rnd = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return f"BKG-{datetime.datetime.now().strftime('%b%Y')}-{rnd}"

@router.post("/", response_model=BookingResponse)
def create_booking(
    booking: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Debug info
    print("=== Booking Attempt ===")
    print("Current user:", current_user.id, current_user.name)
    print("Booking event ID:", booking.event_id)

    # Fetch event
    event = db.query(Event).filter(Event.id == booking.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    print("Event fetched:", event.id, event.title, "Capacity:", event.capacity)

    # Check total bookings for the event
    total_booked = db.query(Booking).filter(Booking.event_id == event.id).count()
    print("Total booked for this event:", total_booked)
    if total_booked >= event.capacity:
        raise HTTPException(status_code=400, detail="Event full")

    # Check if current user already booked
    user_booking = (
        db.query(Booking)
        .filter(Booking.event_id == event.id, Booking.user_id == current_user.id)
        .first()
    )
    if user_booking:
        print("User already booked:", user_booking.booking_id)
        raise HTTPException(status_code=400, detail="Already booked")

    # Create new booking
    new_booking = Booking(
        booking_id=generate_booking_id(),
        user_id=current_user.id,
        event_id=event.id
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    # Assign the event object for response
    new_booking.event = event

    print("Booking created successfully:", new_booking.booking_id)
    return new_booking

# List all bookings of the current user
@router.get("/", response_model=list[BookingResponse])
def list_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bookings = db.query(Booking).filter(Booking.user_id == current_user.id).all()
    return bookings
