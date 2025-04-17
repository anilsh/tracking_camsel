from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import TIME
from datetime import datetime, timedelta
from collections import defaultdict

# Namespace
EX = Namespace("http://example.org/")

# Assuming 'g' is your full rdflib.Graph object from earlier
# STEP 1: Get all dates from the graph
dates = set()
for stmt, _, date in g.triples((None, TIME.hasTime, None)):
    dates.add(datetime.strptime(str(date), "%Y-%m-%d"))

sorted_dates = sorted(dates)
start_date = sorted_dates[0]
end_date = sorted_dates[-1]

# STEP 2: Split into weeks
week_ranges = []
current_start = start_date

while current_start <= end_date:
    current_end = current_start + timedelta(days=6)
    week_ranges.append((current_start, current_end))
    current_start = current_end + timedelta(days=1)

# STEP 3: Extract weekly subgraphs for Delhi behavior
def get_weekly_subgraph(g, week_start, week_end, location_tag="Delhi"):
    subgraph = set()
    for stmt, _, date in g.triples((None, TIME.hasTime, None)):
        date_dt = datetime.strptime(str(date), "%Y-%m-%d")
        if week_start <= date_dt <= week_end:
            stmt_str = stmt.split('/')[-1]  # e.g. User_visits_Cafe_Delhi_2025-02-01
            parts = stmt_str.split('_')
            if len(parts) < 4:
                continue
            p = URIRef(EX[parts[1]])
            o = URIRef(EX["_".join(parts[2:-1])])
            if location_tag in str(o):
                subgraph.add((p, o))
    return subgraph

# STEP 4: Compare each week to Week 1 (Delhi) and compute decay
reference_graph = get_weekly_subgraph(g, *week_ranges[0], location_tag="Delhi")

print("Behavioral Drift (Decay from Week 1 - Delhi):")
for i, (ws, we) in enumerate(week_ranges):
    week_graph = get_weekly_subgraph(g, ws, we, location_tag="Delhi")
    if not reference_graph:
        decay = 1.0
    else:
        overlap = len(reference_graph.intersection(week_graph))
        decay = 1 - (overlap / len(reference_graph))
    print(f"Week {i+1} ({ws.date()} to {we.date()}): Decay = {decay:.2f}")
