from enum import Enum
import datetime
from sqlalchemy import Column, Boolean, Integer, Table, String, ForeignKey, DateTime, func, Enum as SQLEnum
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.db.database import Base  # Используем единую точку входа для Base
class UserRole(str, Enum):
    TEENAGER = "teenager"
    PARENT = "parent"
    PARTNER = "partner"



class UserPosition(Base):
    __tablename__ = "user_positions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    geom = Column(Geometry('POINT', srid=4326), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="position")

class SOSHistory(Base):
    __tablename__ = "sos_history"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    geom = Column(Geometry('POINT', srid=4326), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="sos_history")


class SafetyPoint(Base):
    __tablename__ = "safety_points"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Название (например, "Аптека")
    address = Column(String)
    # Поле для координат (широта и долгота)
    location = Column(Geometry(geometry_type='POINT', srid=4326))

if "circle_members" not in Base.metadata.tables:
    circle_members = Table(
        "circle_members",
        Base.metadata,
        Column("circle_id", Integer, ForeignKey("circles.id"), primary_key=True),
        Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
        extend_existing=True,
    )
else:
    circle_members = Base.metadata.tables["circle_members"]

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    fcm_token = Column(String, nullable=True)
    
    # Связи (ORM)
    owned_circles = relationship("Circle", back_populates="owner")
    member_of_circles = relationship("Circle", secondary=circle_members, back_populates="members")
    position = relationship("UserPosition", back_populates="user")
    sos_history = relationship("SOSHistory", back_populates="user")
class Circle(Base):
    __tablename__ = "circles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Связи (ORM)
    owner = relationship("User", back_populates="owned_circles")
    members = relationship(
        "User", 
        secondary=circle_members, 
        back_populates="member_of_circles", 
        lazy="selectin"  # <--- ВОТ ЭТО ИСПРАВИТ ОШИБКУ
    )
class SOSSession(Base):
    __tablename__ = "sos_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id")) # Кто в беде
    status = Column(String, default="active") # active, completed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class SOSResponse(Base):
    __tablename__ = "sos_responses"
    id = Column(Integer, primary_key=True)
    sos_id = Column(Integer, ForeignKey("sos_sessions.id"))
    responder_id = Column(Integer, ForeignKey("users.id")) # Кто принял
    status = Column(String, default="accepted") # accepted, arrived