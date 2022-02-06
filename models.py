from sqlalchemy import Column, Integer, String  
from database import Base  


class Image(Base):
    __tablename__ = "inbox" 
    code = Column(Integer, primary_key=True, index=True)     
    name = Column(String, unique=True, index=True)     
    data = Column(String, unique=True, index=True)      
