from fastapi import FastAPI
from database import Base, engine
from routers import users, events, bookings

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EventEase Backend")

# Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])

@app.get("/")
def home():
    return {"message": "Welcome to EventEase API"}
