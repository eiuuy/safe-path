from sqlalchemy import Column, Integer, ForeignKey, String, Enum
from sqlalchemy.orm import relationship
from app.db.database import Base

class CircleMember(Base):
    __tablename__ = "circle_members"
    
    id = Column(Integer, primary_key=True, index=True)
    # Тот, кто под защитой (обычно teenager)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Родитель или партнер
    guardian_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Статус связи для подтверждения
    status = Column(String, default="pending") # pending, accepted, rejected

    # Отношения для удобного доступа
    user = relationship("User", foreign_keys=[user_id])
    guardian = relationship("User", foreign_keys=[guardian_id])