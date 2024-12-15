from database import Base, engine
from models.task import Task
from models.user import User
from models.token import ActiveToken

print("Creating Tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")