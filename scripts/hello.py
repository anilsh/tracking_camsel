from rdflib import Graph, RDF, RDFS, OWL
from collections import defaultdict
import json

g = Graph()
g.parse("your_file.ttl", format="ttl")  # <- change this to your file

classes = set(g.subjects(RDF.type, RDFS.Class)) | set(g.subjects(RDF.type, OWL.Class))
properties = (
    set(g.subjects(RDF.type, RDF.Property)) |
    set(g.subjects(RDF.type, OWL.ObjectProperty)) |
    set(g.subjects(RDF.type, OWL.DatatypeProperty))
)

schema = {
    "classes": [],
    "properties": [],
    "instances": defaultdict(list)
}

def get_label(thing):
    return next(g.objects(thing, RDFS.label), None)

for cls in classes:
    schema["classes"].append({
        "uri": str(cls),
        "label": str(get_label(cls) or ""),
        "subClassOf": [str(o) for o in g.objects(cls, RDFS.subClassOf)]
    })

for prop in properties:
    schema["properties"].append({
        "uri": str(prop),
        "label": str(get_label(prop) or ""),
        "domain": [str(o) for o in g.objects(prop, RDFS.domain)],
        "range": [str(o) for o in g.objects(prop, RDFS.range)],
        "subPropertyOf": [str(o) for o in g.objects(prop, RDFS.subPropertyOf)]
    })

for s, p, o in g.triples((None, RDF.type, None)):
    if o in classes:
        schema["instances"][str(o)].append(str(s))

usage_patterns = defaultdict(lambda: defaultdict(int))
for s, p, o in g:
    types = list(g.objects(s, RDF.type))
    for t in types:
        usage_patterns[str(t)][str(p)] += 1

schema["usage_patterns"] = usage_patterns

print(json.dumps(schema, indent=2))
