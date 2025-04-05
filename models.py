from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    phone = Column(String)
    age = Column(Integer)
    is_active = Column(Boolean, default=True)

    # Optionally, a relationship with teams, if needed
    teams = relationship("Team", back_populates="user")


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))  # <-- Corrected line

    # Relationship with the user (one-to-many)
    user = relationship("User", back_populates="teams")

    # Optional relationship with tournaments (many-to-many, depending on structure)
    tournaments = relationship("Tournament", secondary="team_tournaments", back_populates="teams")


class Tournament(Base):
    __tablename__ = 'tournaments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    reward = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    close_reg = Column(DateTime)

    # Relationship with teams (many-to-many)
    teams = relationship("Team", secondary="team_tournaments", back_populates="tournaments")


# Association table for the many-to-many relationship between Team and Tournament
class TeamTournament(Base):
    __tablename__ = 'team_tournaments'

    team_id = Column(Integer, ForeignKey('teams.id'), primary_key=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'), primary_key=True)


class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))
    team_id = Column(Integer, ForeignKey('teams.id'))
    mvp = Column(String, nullable=True)
    score = Column(String)

    # Relationship to team and tournament
    team = relationship("Team")
    tournament = relationship("Tournament")
