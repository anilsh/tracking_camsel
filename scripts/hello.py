import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD

# Define RDF namespace
ex = Namespace("http://example.com/")

# Initialize RDF graph
g = Graph()
g.bind("ex", ex)

# Sample DataFrames (Replace with actual data)
facesview_df = pd.DataFrame([
    {"image_id": "IMG_001", "media_id": "M001", "person_id": "P001", "name": "John Doe", "age": 30, "gender": "Male", "face_expression": "Happy"}
])

location_view_df = pd.DataFrame([
    {"media_id": "M001", "lat": 37.7749, "lon": -122.4194, "address": "San Francisco, CA"}
])

scene_view_df = pd.DataFrame([
    {"image_id": "IMG_001", "scene_name": "Beach Sunset", "datetaken": "2024-03-26T14:30:00"}
])

# Function to add Person entities
def add_persons(df):
    for _, row in df.iterrows():
        person_uri = URIRef(ex + f"Person_{row['person_id']}")
        media_uri = URIRef(ex + f"Media_{row['media_id']}")

        g.add((person_uri, RDF.type, ex.Person))
        g.add((person_uri, ex.hasName, Literal(row["name"], datatype=XSD.string)))
        g.add((person_uri, ex.hasAge, Literal(row["age"], datatype=XSD.integer)))
        g.add((person_uri, ex.hasGender, Literal(row["gender"], datatype=XSD.string)))
        g.add((person_uri, ex.appearsIn, media_uri))

# Function to add Media entities and locations
def add_media_locations(df):
    for _, row in df.iterrows():
        media_uri = URIRef(ex + f"Media_{row['media_id']}")
        location_uri = URIRef(ex + f"Location_{row['media_id']}")

        g.add((media_uri, RDF.type, ex.Media))
        g.add((media_uri, ex.takenAt, location_uri))

        g.add((location_uri, RDF.type, ex.Location))
        g.add((location_uri, ex.hasLatitude, Literal(row["lat"], datatype=XSD.float)))
        g.add((location_uri, ex.hasLongitude, Literal(row["lon"], datatype=XSD.float)))
        g.add((location_uri, ex.hasAddress, Literal(row["address"], datatype=XSD.string)))

# Function to add Scene entities
def add_scenes(df):
    for _, row in df.iterrows():
        media_uri = URIRef(ex + f"Media_{row['image_id']}")
        scene_uri = URIRef(ex + f"Scene_{row['image_id']}")

        g.add((media_uri, RDF.type, ex.Media))
        g.add((media_uri, ex.depictsScene, scene_uri))

        g.add((scene_uri, RDF.type, ex.Scene))
        g.add((scene_uri, ex.hasSceneName, Literal(row["scene_name"], datatype=XSD.string)))
        g.add((scene_uri, ex.hasTimestamp, Literal(row["datetaken"], datatype=XSD.dateTime)))

# Generate RDF triples
add_persons(facesview_df)
add_media_locations(location_view_df)
add_scenes(scene_view_df)

# Save to Turtle file
output_file = "personal_kg.ttl"
g.serialize(output_file, format="turtle")
print(f"Turtle file saved as {output_file}")
