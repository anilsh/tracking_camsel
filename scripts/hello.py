
import random
from datetime import datetime, timedelta
from rdflib import Graph, Literal, RDF, URIRef, Namespace, XSD

# Namespaces
EX = Namespace("http://example.org/")
TIME = Namespace("http://www.w3.org/2006/time#")
XSD_NS = Namespace("http://www.w3.org/2001/XMLSchema#")

# Initialize Graph
g = Graph()
g.bind("ex", EX)
g.bind("time", TIME)

# Simulation params
start_date = datetime(2025, 2, 1)
user = URIRef(EX.User)

def city_for_day(day):
    return "Delhi" if day < datetime(2025, 3, 15) else "Bangalore"

def add_event(subject, predicate, obj, timestamp):
    g.add((subject, predicate, obj))
    stmt = URIRef(f"{subject}_{predicate}_{obj}_{timestamp}")
    g.add((stmt, TIME.hasTime, Literal(timestamp.strftime("%Y-%m-%d"), datatype=XSD.date)))

# Activity schedule logic
def simulate_day(day):
    city = city_for_day(day)
    weekday = day.weekday()  # 0=Mon, ..., 6=Sun
    date_str = day.strftime("%Y-%m-%d")
    
    # Base daily events
    add_event(user, EX.lives_at, URIRef(EX[f"Home_{city}"]), day)
    if weekday < 5:
        add_event(user, EX.works_at, URIRef(EX[f"Office_{city}"]), day)

    # Gym on Mon/Wed/Fri
    if weekday in [0, 2, 4]:
        add_event(user, EX.visits, URIRef(EX[f"Gym_{city}"]), day)
    
    # Park on Tue/Sun
    if weekday in [1, 6]:
        add_event(user, EX.visits, URIRef(EX[f"Park_{city}"]), day)
    
    # Cafe 1–2x per week
    if random.random() < 0.2:
        add_event(user, EX.visits, URIRef(EX[f"Cafe_{city}"]), day)

    # Meets friend on Sat or Sun
    if weekday in [5, 6]:
        add_event(user, EX.meets, URIRef(EX[f"Friend_{city}"]), day)
    
    # Shops every 2 weeks on weekends
    if day.day % 14 == 0 and weekday in [5, 6]:
        add_event(user, EX.shops_at, URIRef(EX[f"Mall_{city}"]), day)

# Generate data for 10 weeks
for i in range(70):
    current_day = start_date + timedelta(days=i)
    simulate_day(current_day)

# Save TKG
g.serialize("lifelog_10weeks_tkg.ttl", format="turtle")
