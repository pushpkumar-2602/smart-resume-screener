from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    raw_text = Column(Text, nullable=False)
    skills = Column(Text)
    education = Column(Text)
    content_hash = Column(String, unique=True, nullable=False)

engine = create_engine("sqlite:///data/screener.db")
Session = sessionmaker(bind=engine)

def init_db():
    """Creates the resumes table if it doesn't already exist."""
    Base.metadata.create_all(engine)
