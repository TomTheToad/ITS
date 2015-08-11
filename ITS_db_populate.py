from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ITS_db_setup import Base, Agents, Passengers, Species, TestPassengers, Destinations, TravelMethod, Menu, \
    TestingStatus, Tests, TestResults


engine = create_engine('sqlite:///ITS.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Default primary user
newUser = Agents(name="Bo Jo", email="vasselta@gmail.com", picture="../static/images/eyes.jpg")
session.add(newUser)
session.commit()

# Default Species
species1 = Species(name="aquaticus", description="A water born species.",
                   special_messages="Sometimes allergic to Humans. Fears all fleshlings.")
species2 = Species(name="mechanicus", description="Autonomous, self procreating and sometimes intelligent robots",
                   special_messages="Sometimes homicidal. No real way of telling beyond the obvious. Fears fleshlings.")
species3 = Species(name="fleshling",
                   description="Generally referring to human yet category has grown significantly.",
                   special_messages="The most feared species in the universe. Use extreme caution")

session.add(species1)
session.add(species2)
session.add(species3)
session.commit()

# Default Primary Passenger
newPassenger1 = Passengers(first_name="Lewis", last_name="Gates", species_id=3, agent_id=1, notes="Write something.")
newPassenger2 = Passengers(first_name="Frank", last_name="Lloyd", species_id=3, agent_id=1, notes="Write something.")
newPassenger3 = Passengers(first_name="Robot", last_name="Jones", species_id=2, agent_id=1, notes="Write something.")

session.add(newPassenger1)
session.add(newPassenger2)
session.add(newPassenger3)
session.commit()

# Default Test Passengers
testpass1 = TestPassengers(first_name='Burney', last_name='Snapattakids', species_id=1,
                           notes="Mr Snapattakids is the host of a very popular children's show. It is imperative"
                                 "that Mr. Snapattakids does not see children on his vacation.",
                           image="../static/images/octo.gif")
testpass2 = TestPassengers(first_name='Eatya', last_name='Sausagemaker', species_id=2,
                           notes="Ms Sausagemaker led a stirling career as the head of all recycling on her home"
                                 "planet of Vyger when another one of our clients, not to be mentioned (see Mr"
                                 "Kerplowski) came for a visit. Her beloved recycling works was destroyed and "
                                 "many unfortunate events have ensued since. ", image="../static/images/robo2.gif")
testpass3 = TestPassengers(first_name='Leroy', last_name='Jenkins', species_id=3,
                           notes="Mr Kerplowsky is the most influential, successful, and wealthy door to door .net"
                                 "salesman in all the known universe. He is our best and, unfortunately, clumsiest "
                                 "clients. He is to be handled with extreme caution!",
                           image="../static/images/weirdo.jpg")

session.add(testpass1)
session.add(testpass2)
session.add(testpass3)
session.commit()

# Default Destinations
destination1 = Destinations(name='Deep Space9', description="Need something here.")
destination2 = Destinations(name='Zentari Moons', description="Need something here.")
destination3 = Destinations(name='Plava Laguna', description="Need something here.")

session.add(destination1)
session.add(destination2)
session.add(destination3)
session.commit()

# Default Travel Methods
travel_method1 = TravelMethod(name="RocketLiner", description="Although a bit cramped. The fastest way to reach your "
                                                              "destination of choice.")
travel_method2 = TravelMethod(name="Enterpoop", description="A casual, luxurious transport befitting of royalty")
travel_method3 = TravelMethod(name="Shipping Container", description="A cost effective way to safely transport any "
                                                                     "item of concern.")

session.add(travel_method1)
session.add(travel_method2)
session.add(travel_method3)
session.commit()

# Default Menu options
menu_item1 = Menu(name="sushi dinner", description="A lovely arrangement of sushi inspired delicacies. May not contain "
                                                   "actual sushi.")
menu_item2 = Menu(name="chicken dinner", description="A delectable chicken like dinner. Does not always contain "
                                                     "chicken but, nobody every seems to notice.")
menu_item3 = Menu(name="gelatinous goo", description="The one and only, authentic affluent from everybody's favorite "
                                                     "creamery. A fan favorite for sure.")
menu_item4 = Menu(name="third class", description="For the discerning, frugal palate. Only available in international "
                                                  "space regions.")

session.add(menu_item1)
session.add(menu_item2)
session.add(menu_item3)
session.add(menu_item4)
session.commit()

# Default Test requirements for success
test1 = Tests(test_name="It's Burney Time Kids!", passenger_id=1, destination_id=2,
              travel_method_id=3, menu_id=3)
test2 = Tests(test_name="Robot Rendezvous", passenger_id=2, destination_id=1,
              travel_method_id=2, menu_id=4)
test3 = Tests(test_name="Careful Planning", passenger_id=3, destination_id=3,
              travel_method_id=3, menu_id=1)

session.add(test1)
session.add(test2)
session.add(test3)
session.commit()


# Default Results for Agent Testing
results1 = TestResults(test_id=1, win_message="You Win", lose_message="Loser")
results2 = TestResults(test_id=2, win_message="You Win", lose_message="Loser")
results3 = TestResults(test_id=3, win_message="You Win", lose_message="Loser")

session.add(results1)
session.add(results2)
session.add(results3)
session.commit()

