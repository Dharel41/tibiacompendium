from sqlalchemy import Integer, String, Column
from tibiacompendium.db import Base

class HuntingPlace(Base):
    __tablename__ = 'huntingplace'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    exp_on_hour = Column(Integer, nullable=False)
    gold_on_hour = Column(Integer, nullable=True)
    hunt_type = Column(String(10), nullable=True, default='solo')
    description = Column(String, nullable=True, default='')
    rune = Column(String(50), nullable=True, default='')
    character_levels = Column(String(50), nullable=True, default='')
    equipment_with_resistance = Column(String(50), nullable=True, default='')

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return f'{self.name}'