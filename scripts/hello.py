Great — now we narrow this down to 5 strong, deployable pipelines (mobile-ready) similar to your image (clear flow, deterministic, robust).

I’ll give each in the same style:

Trigger logic

Steps

Why it works



---

✅ 1. Embedding Similarity → Template (Primary Path)

Flow

User Query
↓
Vector Similarity (SLM embedding)
↓
Top Template (Qi) + score
↓ (if score ≥ threshold)
Entity Extraction (NER)
↓
Fill SPARQL
↓
Execute KG

Why this works

Fast (single embedding + dot product)

Robust to paraphrases

Already in your design



---

✅ 2. Keyword + Rule-based Routing (Fallback)

Flow

User Query
↓
Keyword Detection (most, recent, location, interest, etc.)
↓
Rule Mapping → Template (Qi)
↓
Entity Extraction
↓
Fill SPARQL
↓
Execute KG

Why this works

Deterministic

Handles edge cases where embeddings fail

Very cheap on mobile



---

✅ 3. Hybrid: Similarity + Constraint Validation (Best Practical)

Flow

User Query
↓
Vector Similarity → Top-K templates
↓
Entity Extraction (NER)
↓
Constraint Check (time, person, category)
↓
Select best valid template
↓
Fill SPARQL
↓
Execute KG

Why this works

Avoids wrong template selection

Uses KG constraints (important for temporal queries)

High accuracy without heavy models



---

✅ 4. Lightweight Classification → Template

Flow

User Query
↓
Intent Classifier (Q01–Q15)
↓
Template Selection (Qi)
↓
Entity Extraction
↓
Fill SPARQL
↓
Execute KG

Why this works

Very fast (small classifier)

Stable mapping to predefined queries

Works well when query space is fixed



---

✅ 5. NER-first → Graph-aware Routing

Flow

User Query
↓
Entity Extraction (NER)
↓
Entity Linking (KG nodes)
↓
Infer possible relations from KG
↓
Template Selection (Qi)
↓
Fill SPARQL
↓
Execute KG

Why this works

Uses KG structure (not just text)

Good for ambiguous queries

Handles entity-heavy queries well



---

🚫 What we are NOT choosing (important)

Not suitable for mobile:

❌ Full LLM generation (KGT5 seq2seq)

❌ REBEL triple generation

❌ Complex reasoning models (GNN inference heavy)

❌ Free-form parsing



---

🔑 Final Combined Architecture (Recommended)

You can combine 1 + 2 + 3:

User Query
↓
Vector Similarity
↓ (if confident)
Template Selected
↓
NER → Fill SPARQL

ELSE
↓
Keyword + Rule Mapping
↓
Template

ELSE
↓
Top-K + Constraint Validation
↓
Template

↓
Execute KG


---

🧠 Key Insight (for your slide)

All robust mobile pipelines reduce to:
Template Selection + Slot Filling + KG Execution


---

📌 One-line summary

Use embedding similarity as primary routing, rules as fallback, and constraint validation to ensure correct template selection before SPARQL execution.


---

If you want, I can convert this into a clean diagram exactly like your slide (with YES/NO branches and thresholds) so it directly fits your presentation.