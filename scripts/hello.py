# Required libraries
from rdflib import Graph, URIRef, Namespace, Literal
from rdflib.namespace import XSD
from datetime import datetime, timedelta
from collections import defaultdict
import networkx as nx
from node2vec import Node2Vec
from karateclub import Graph2Vec
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Namespaces
general = Namespace("http://example.org/personal/general/")
health1 = Namespace("http://example.org/personal/health/")
person1 = Namespace("http://example.org/personal/person/")
travell = Namespace("http://example.org/personal/travel/")
time = Namespace("http://example.org/personal/time/")

# Load Graph
g = Graph()
g.parse("simulated_health_travel_drift_daily.ttl", format="ttl")

# --- 1. Snapshot Extraction (Weekly Buckets) ---
def extract_weekly_snapshot(graph, start_date, target_week):
    grouped = defaultdict(list)
    for o, p, t in graph.triples((None, time.timestamp, None)):
        if isinstance(t, Literal):
            dt = datetime.fromisoformat(str(t))
            week_num = (dt - start_date).days // 7
            grouped[week_num].append(str(o))

    snapshot_triples = []
    for s, p, o in graph:
        if str(o) in grouped[target_week] or str(s) in grouped[target_week]:
            snapshot_triples.append((s, p, o))
    return snapshot_triples

# --- 2. Extract Subgraphs by Context ---
def extract_subgraphs_by_context(triples, context_prefix):
    G = nx.DiGraph()
    for s, p, o in triples:
        if context_prefix in str(p) or context_prefix in str(o):
            G.add_edge(str(s), str(o), label=str(p).split("/")[-1])

    subgraphs = []
    for component in nx.weakly_connected_components(G):
        sg = G.subgraph(component).copy()
        if sg.number_of_edges() > 0:
            subgraphs.append(sg)
    return subgraphs

# --- 3. Compute Embeddings ---
def get_graph_embeddings(subgraphs):
    g2v = Graph2Vec(dimensions=64, wl_iterations=2, epochs=10)
    g2v.fit(subgraphs)
    graph_embeds = g2v.get_embedding()
    return graph_embeds

def get_node_embeddings(subgraph):
    if subgraph.number_of_nodes() < 2:
        return None
    n2v = Node2Vec(subgraph, dimensions=64, walk_length=5, num_walks=10, workers=1)
    model = n2v.fit(window=3, min_count=1, batch_words=4)
    emb = np.mean([model.wv[n] for n in subgraph.nodes if n in model.wv], axis=0)
    return emb

# --- 5. Compute Evolution Signature ---
def compute_evolution_signature(ref_subgraphs, fut_subgraphs):
    Sg = cosine_similarity(get_graph_embeddings(ref_subgraphs), get_graph_embeddings(fut_subgraphs))
    Sn = []
    for gi in ref_subgraphs:
        row = []
        vi = get_node_embeddings(gi)
        for gj in fut_subgraphs:
            vj = get_node_embeddings(gj)
            if vi is None or vj is None:
                row.append(0.0)
            else:
                row.append(cosine_similarity([vi], [vj])[0][0])
        Sn.append(row)
    Sn = np.array(Sn)

    # Decision
    evolution_sig = []
    for i in range(Sg.shape[0]):
        for j in range(Sg.shape[1]):
            sg_sim = Sg[i, j]
            sn_sim = Sn[i, j]
            if sg_sim > 0.7 and sn_sim > 0.7:
                label = "static"
            elif sg_sim > 0.7 and sn_sim < 0.5:
                label = "growing"
            elif sg_sim < 0.5 and sn_sim > 0.7:
                label = "possible drift"
            else:
                label = "drifted"
            evolution_sig.append((i, j, label))
    return evolution_sig, Sg, Sn

# --- 6. Run Full Pipeline ---
start_date = datetime(2023, 1, 1)
t1 = 0  # week 0
t2 = 20  # week 20

triples_t1 = extract_weekly_snapshot(g, start_date, t1)
triples_t2 = extract_weekly_snapshot(g, start_date, t2)

subgraphs_t1 = extract_subgraphs_by_context(triples_t1, "health")
subgraphs_t2 = extract_subgraphs_by_context(triples_t2, "health")

evol_sig, sg_mat, sn_mat = compute_evolution_signature(subgraphs_t1, subgraphs_t2)

print("Evolution Signatures between t1 and t2:")
for (i, j, label) in evol_sig:
    print(f"Subgraph {i} → {j}: {label}")

# Check if any drift
drift_detected = any(label == "drifted" or label == "possible drift" for (_, _, label) in evol_sig)
print("\nDrift Detected:" if drift_detected else "\nNo Drift Detected")
