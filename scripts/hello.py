from collections import defaultdict
from rdflib import URIRef

def get_weekly_subgraph(g, week_start, week_end):
    week_graph = set()
    for s, p, o in g:
        if isinstance(o, URIRef) and "Delhi" in str(o):
            stmt_str = f"{s.split('/')[-1]}_{p.split('/')[-1]}_{o.split('/')[-1]}"
            for stmt, _, date in g.triples((URIRef(f"http://example.org/{stmt_str}_{week_start.strftime('%Y-%m-%d')}"), TIME.hasTime, None)):
                week_graph.add((p, o))
    return week_graph

# For simplicity: assume we extract 6 weeks in Delhi
reference_graph = get_weekly_subgraph(g, week1_start, week1_end)
for w in range(2, 7):
    week_graph = get_weekly_subgraph(g, week_start[w], week_end[w])
    overlap = len(reference_graph.intersection(week_graph))
    decay = 1 - (overlap / len(reference_graph))
    print(f"Week {w}: Decay = {decay:.2f}")
