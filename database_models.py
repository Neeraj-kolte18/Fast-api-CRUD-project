from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer,Column,String,Float

Base =declarative_base()

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer,primary_key = True,index = True)
    name = Column(String)
    price = Column(Float)
    quantity = Column(Float)
    description = Column(String)
