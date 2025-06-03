from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from database import Base
from datetime import datetime

class Redacao(Base):
    __tablename__ = "redacoes"

    id = Column(Integer, primary_key=True, index=True)
    hash_imagem = Column(String, unique=True, index=True, nullable=False)
    nota_final = Column(Integer, nullable=False)
    competencias = Column(JSONB, nullable=False)  
    comentarios = Column(JSONB, nullable=False)   
    feedback_geral = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
