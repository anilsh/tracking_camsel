from rdflib import Graph, RDF, RDFS, OWL

# Load the TTL file
g = Graph()
g.parse("your_file.ttl", format="ttl")  # Change filename as needed

# Extract classes
classes = set(g.subjects(RDF.type, RDFS.Class)) | set(g.subjects(RDF.type, OWL.Class))

# Extract properties
properties = (
    set(g.subjects(RDF.type, RDF.Property)) |
    set(g.subjects(RDF.type, OWL.ObjectProperty)) |
    set(g.subjects(RDF.type, OWL.DatatypeProperty))
)

# Build schema representation
schema = {
    "classes": [],
    "properties": []
}

# Add classes
for cls in classes:
    schema["classes"].append({
        "uri": str(cls),
        "label": str(g.label(cls) or ""),
        "subClassOf": [str(o) for o in g.objects(cls, RDFS.subClassOf)]
    })

# Add properties
for prop in properties:
    schema["properties"].append({
        "uri": str(prop),
        "label": str(g.label(prop) or ""),
        "domain": [str(o) for o in g.objects(prop, RDFS.domain)],
        "range": [str(o) for o in g.objects(prop, RDFS.range)],
        "subPropertyOf": [str(o) for o in g.objects(prop, RDFS.subPropertyOf)]
    })

# Pretty print the schema
import json
print(json.dumps(schema, indent=2))

