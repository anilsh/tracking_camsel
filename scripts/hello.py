AriGraph:

The paper introduces AriGraph, a knowledge graph-based memory system for LLM agents to improve reasoning and planning in dynamic environments. Existing memory architectures (e.g., RAG, summarization) struggle with structured knowledge retention. AriGraph integrates semantic (factual) and episodic (experience-based) memories, enabling LLM agents to learn world models, retrieve relevant information, and explore environments more effectively.

Handling unstructured LLM memory – Converts raw experiences into structured knowledge graphs.
Efficient long-term knowledge retention – Integrates semantic and episodic memory for improved recall.
Effective reasoning & decision-making – Enables agents to plan and act based on structured world models.
Scalability in dynamic environments – Allows incremental updates and efficient retrieval from memory.

Approach:
Observation Processing – The LLM agent receives observations from the environment and extracts semantic triplets (object, relation, object).
Then a Knowledge Graph is constructed – Semantic memory stores general factual knowledge, while episodic memory stores past experiences as interconnected nodes (by linking observations with semantic triples).
The system then removes outdated knowledge and updates the graph dynamically as the agent interacts with the environment.
Retrieval for Decision-Making – Uses semantic search (triplet-based) and episodic search (event-based) to retrieve relevant information for planning. A planning module generates sub-goals, and the decision-making module (ReAct framework) chooses the best action based on retrieved knowledge.
Execution & Learning Loop – The agent performs the action, receives feedback, and updates its memory, continuously refining its world model.


Zep: 
Zep employs episodic memory within a temporally-aware knowledge graph (KG), constructed and updated through its Graphiti engine. The memory system is designed to ingest, structure, and retrieve time-sensitive knowledge while preserving historical context.

Zep organizes memory into three hierarchical graph substructures:
1. Episodic Subgraph: Stores raw input data (messages, JSON, structured text) as episodic nodes
2. Semantic Entity Subgraph: Extracts entities and relationships from episodes, resolving them against existing graph entities.
3. Community Subgraph: Forms higher-level clusters of related entities, summarizing their interactions.

Temporal Knowledge Graph Updates: The system tracks four timestamps for each fact and relationship. Zep automatically invalidates outdated facts when newer, contradicting facts appear, ensuring the KG remains temporally consistent.

Memory-Driven Agent Context Construction: 
Retrieved entities, facts, and relationships are structured into formatted context strings for LLMs.
The system provides time-bounded, validated context, enabling agents to reason over evolving knowledge states.
                                                                                                                                                           
                                                                                                                                                           
                                                                                                                                                           
A*Net

The paper introduces A*Net, a scalable path-based reasoning model for knowledge graphs (KGs) that improves efficiency in multi-hop reasoning by using a neural priority function inspired by the A shortest path algorithm* to prune unnecessary paths, reducing search space.


Given a head entity (u) and query relation (q), A*Net aims to find the target entity (v) by searching important paths.
Define Priority Function

Uses a learned priority function to score entities based on their importance to the query.
The priority function is defined as:
s(x)=d(u,x)⊗g(x,v)
where d(u, x) is the shortest path distance from u to x, and g(x, v) estimates the remaining cost.

Instead of exploring all possible paths, A*Net selects the top-K most promising nodes and top-L edges per iteration based on the priority function.

This ensures that only the most relevant paths contribute to reasoning. The algorithm expands the graph until a valid answer is reached. Returns the most probable target entity (v) based on path scores.

expansion refers to the process of selecting and exploring new nodes and edges in the knowledge graph (KG) during multi-hop reasoning. Instead of searching the entire graph, A*Net expands only the most promising paths based on a learned priority function, making reasoning more efficient.
Expansion is to reduce the search path as compared to the addition of new entities/knowledge to the KG. 


The paper introduces MStar, an inductive knowledge graph (KG) reasoning framework that enhances message propagation efficiency for distant entities. Implements a shortcut mechanism inspired by ResNet to allow faster propagation of conditional messages, reducing computational overhead.

Starting Entities Selection (SES)
A Pre-Embedded GNN encodes entities and selects multiple query-specific starting entities instead of a single source node.
Selected entities broaden the reasoning scope, improving coverage for distant entities.

Highway Layer for Message Propagation
Constructs shortcut edges between the head entity and selected starting entities, inspired by skip connections in deep networks.
Enables faster message passing across long distances in the KG.

A graph neural network (GNN) propagates relational information from the starting entities. A decoder (MLP-based) ranks candidate entities based on their updated embeddings.

The model predicts missing triplets by selecting the most relevant tail entity.

Short-Term Memory (Short Term Personal Memory Component 1052)
Stores recent user interactions, including dialog history, UI selections, and recent requests.
Maintains context-aware session data for interpreting follow-up commands (e.g., recognizing "in New York" as a reference to a previous weather query)​
.
Cached locally on client devices or server-side session storage for fast recall.
Long-Term Memory (Long Term Personal Memory Component 1054)
Persistently stores user-specific information, such as preferences, identities, contact lists, saved locations, shopping lists, entertainment history, and transaction records​
.
Supports contextual personalization by recalling previous selections and refining recommendations based on past interactions.
Stored across databases, cloud storage, or external services for long-term retrieval.
                                                                                                                                                           
