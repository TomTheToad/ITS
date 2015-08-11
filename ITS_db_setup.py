from sqlalchemy import Column, ForeignKey, Integer, String, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine('sqlite:///ITS.db')

Base.metadata.create_all(engine)


# A table which stores the agent users of this app.
class Agents(Base):
    __tablename__ = 'agents'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


# A collection of various species to choose from
# when creating clients
class Species(Base):
    __tablename__ = 'species'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    description = Column(String(200))
    special_messages = Column(String(200))

    @property
    def serialize(self):
        """Return object data in serializable format"""
        return {
            'special_messages': self.special_messages,
            'description': self.description,
            'name': self.name,
            'id': self.id,
        }


# Passenger information. Not the test clients.
class Passengers(Base):
    __tablename__ = 'passengers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    species_id = Column(Integer, ForeignKey('species.id'), nullable=False)
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    notes = Column(String(400))
    image = Column(String(100))

    species = relationship(Species)
    agents = relationship(Agents)


# Test passenger details
class TestPassengers(Base):
    __tablename__ = 'test_passengers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(80))
    last_name = Column(String(80))
    species_id = Column(Integer, ForeignKey('species.id'))
    notes = Column(String(250))
    image = Column(String(250))

    species = relationship(Species)


# Travel Destinations
class Destinations(Base):
    __tablename__ = 'destinations'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    description = Column(String(200))

    @property
    def serialize(self):
        """Return object data in serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


# Methods of travel
class TravelMethod(Base):
    __tablename__ = 'travel_method'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    description = Column(String(200))

    @property
    def serialize(self):
        """Return object data in serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


# The food options
class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    description = Column(String(200))

    @property
    def serialize(self):
        """Return object data in serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


# Storage for test parameters for agent testing game
class Tests(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True)
    test_name = Column(String(60))
    passenger_id = Column(Integer, ForeignKey('test_passengers.id'))
    destination_id = Column(Integer, ForeignKey('destinations.id'))
    travel_method_id = Column(Integer, ForeignKey('travel_method.id'))
    menu_id = Column(Integer, ForeignKey('menu.id'))

    test_passengers = relationship(TestPassengers)
    destinations = relationship(Destinations)
    travel_method = relationship(TravelMethod)
    menu = relationship(Menu)


# Stores the agents game attempts
class TestingStatus(Base):
    __tablename__ = 'testing_status'

    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agents.id'))
    test_id = Column(Integer, ForeignKey('tests.id'))
    test_complete = Column(BOOLEAN)

    agents = relationship(Agents)
    tests = relationship(Tests)


# A currently unused place to store a
# collection of outcomes. This will
# be used in the next version.
class TestResults(Base):
    __tablename__ = 'test_results'

    id = Column(Integer, primary_key=True)
    test_id = Column(Integer, ForeignKey('tests.id'))
    win_message = Column(String(400))
    lose_message = Column(String(400))

    test = relationship(Tests)


engine = create_engine('sqlite:///ITS.db')

Base.metadata.create_all(engine)
