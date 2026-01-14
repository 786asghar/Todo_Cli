from sqlmodel import create_engine, Session
from typing import Generator
import os
from contextlib import contextmanager
try:
    # Try relative import first
    from .models.task import Task
    from .models.skill import Skill
    from .models.user import User
except ImportError:
    # Fall back to absolute import
    from models.task import Task
    from models.skill import Skill
    from models.user import User
from sqlmodel import SQLModel

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, that's fine

# Get database URL from environment, with a default for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_test.db")

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)


# Create tables function
def create_db_and_tables():
    SQLModel.metadata.create_all(engine, checkfirst=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session