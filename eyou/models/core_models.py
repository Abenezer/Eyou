


from sqlalchemy import (
    Column,
    Index,
    Integer,
    Float,
    Text,
    Boolean,
    ForeignKey

)

from sqlalchemy.orm import relationship
from .meta import Base


class Place(Base):
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    description = Column(Text)
    lat = Column(Integer)
    lon = Column(Integer)
    type_id = Column(Integer, ForeignKey('type.id'))
    area_id = Column(Integer, ForeignKey('area.id'))
    type = relationship("Type")
    area = relationship("Area")




#Index('place_name_index', Place.name, unique=True, mysql_length=255)

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    description = Column(Text)
    popularity = Column(Integer)
    types = relationship("Type", back_populates="category")


class Type(Base):
    __tablename__ = 'type'
    id= Column(Integer,primary_key=True)
    name = Column(Text)
    description = Column(Text)
    popularity = Column(Integer)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", back_populates="types")

#Index('type_name_index', Type.name, unique=True, mysql_length=255)

class Area(Base):
    __tablename__ = 'area'
    id = Column(Integer, primary_key=True)
    lon = Column(Float)
    lat = Column(Float)
    country = Column(Text)
    city = Column(Text)
    localName = Column(Text)
    displayName = Column(Text)
    description = Column(Text)
    boundingBox = Column(Text)
    OSM_id = Column(Integer)
    nom_place_id = Column(Integer)
