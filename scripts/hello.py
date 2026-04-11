Got it — you want something that reads like a tight AAAI 2-page extended abstract, not just a rewritten abstract. I’ll structure it with:

Introduction (positioning vs prior work)

Method (DCE-centric, lens minimized)

Experiments (selective, high-impact, mobile relevance)

Tone: important, forward-looking, mobile/edge AI framing


Below is a clean, submission-ready draft.


---

ContextGraph: Mobile-Centric Lifelog Intelligence via Contextual Subgraph Evolution

1. Introduction

Modern mobile devices continuously generate dense streams of lifelog data through sensors, applications, and user interactions. These signals encode rich contextual information about user behavior, social interactions, and environmental dynamics. However, existing approaches to mobile intelligence largely rely on either (i) stateless embeddings that ignore temporal evolution or (ii) retrieval-based systems that fail to capture higher-order structure in user context. This limits their ability to support personalized, adaptive, and privacy-preserving intelligence directly on-device.

Recent advances in temporal graph learning and knowledge graph embeddings provide a promising direction for modeling structured and evolving data. However, these methods are typically designed for large-scale server-side settings and do not directly address the constraints of mobile environments, such as limited compute, streaming data, and the need for compact representations. Furthermore, prior work does not explicitly model daily contextual coherence, which is a fundamental unit of human behavioral patterns.

We introduce ContextGraph, a lifelog intelligence framework that models mobile-generated data as a Temporal Knowledge Graph (TKG) and captures its evolution through compact, learnable representations. The key contribution is Day Context Embeddings (DCE), which encode temporally grounded, context-rich summaries of user activity. Unlike conventional embeddings that focus on static graph structure, DCE captures how context evolves over time, enabling downstream reasoning tasks such as behavioral prediction, routine discovery, and anomaly detection.

Our design explicitly targets mobile-first deployment, emphasizing computational efficiency, incremental updates, and compact representations. While we incorporate a subgraph extraction mechanism to localize contextual signals, the primary emphasis is on learning expressive yet efficient embeddings that can operate in resource-constrained environments.


---

2. Method: ContextGraph with Day Context Embeddings

2.1 Temporal Knowledge Graph Construction

We represent lifelog data as a Temporal Knowledge Graph (TKG) , where nodes correspond to entities (e.g., locations, activities, contacts) and edges represent temporally grounded interactions. Each event is modeled as a timestamped relational triple, enabling the graph to evolve continuously as new data arrives.

This representation unifies heterogeneous mobile signals into a structured format, enabling relational reasoning while preserving temporal dynamics.


---

2.2 Day Context Embeddings (DCE)

The core of our approach is Day Context Embeddings (DCE), which aggregate temporally proximal interactions into a compact representation for each day.

Formally, for a given day , we construct a contextual subgraph . The DCE vector  is learned to capture:

Entity co-occurrence patterns (what appears together)

Temporal distribution of interactions (when events occur)

Relational structure (how entities are connected)


DCE is computed through a combination of:

Temporal aggregation of node/edge features

Context-aware pooling over daily subgraphs

Embedding optimization using contrastive or predictive objectives


This results in a low-dimensional, expressive representation that summarizes a full day of activity.

Key properties for mobile use:

Compactness → efficient storage and transmission

Incrementality → can be updated as new events arrive

Generality → supports multiple downstream tasks



---

2.3 Contextual Subgraph Evolution (Lightweight Lens)

To capture fine-grained contextual dynamics, we include a lightweight mechanism for extracting contextual subgraphs from the TKG. These subgraphs allow the model to focus on relevant subsets of interactions when needed.

However, unlike prior formulations that rely heavily on subgraph reasoning, our approach uses this component sparingly, with DCE serving as the primary representation. This design choice ensures scalability and suitability for on-device deployment.


---

2.4 Mobile-Centric Design Considerations

ContextGraph is designed with mobile constraints in mind:

Streaming compatibility: embeddings can be updated incrementally

Low memory footprint: DCE compresses high-frequency lifelog data

On-device feasibility: avoids heavy graph computations at inference time

Privacy preservation: enables local processing without cloud dependency



---

3. Experiments

3.1 Tasks and Setup

We evaluate ContextGraph on tasks that reflect both graph reasoning and mobile intelligence use cases:

Node classification (predicting entity roles or categories)

Graph classification (classifying daily or contextual graphs)

Temporal prediction (forecasting future interactions or behaviors)


We compare against standard baselines from:

Static graph embeddings

Temporal graph models

Knowledge graph embedding methods



---

3.2 Main Results

Across tasks, DCE consistently outperforms baseline methods, demonstrating:

Improved accuracy in node and graph classification

Strong performance in temporal prediction tasks

Better generalization across datasets and domains


Importantly, these gains are achieved with significantly lower representational complexity, highlighting the efficiency of DCE.


---

3.3 Ablation and Analysis

We analyze the contribution of each component:

DCE vs static embeddings: DCE captures temporal coherence, leading to clear gains

With vs without subgraph extraction: marginal improvements, confirming DCE as the dominant factor

Dimensionality analysis: DCE maintains performance even at low embedding sizes


These results reinforce that contextual temporal aggregation is the key driver of performance.


---

3.4 Mobile Relevance

We further evaluate properties relevant to mobile deployment:

Embedding size vs performance trade-offs

Incremental updates over streaming data

Inference efficiency compared to temporal graph baselines


Results show that ContextGraph achieves a strong balance between accuracy and efficiency, making it suitable for on-device intelligence applications.


---

4. Conclusion

We presented ContextGraph, a mobile-centric framework for modeling and reasoning over lifelog data using Temporal Knowledge Graphs. By introducing Day Context Embeddings (DCE), we provide a compact and expressive representation that captures the evolution of user context over time.

Our results demonstrate that DCE enables efficient, scalable, and accurate reasoning, positioning ContextGraph as a foundation for next-generation mobile intelligence systems that are continuous, personalized, and privacy-aware.


---

✅ If you want to push this further

I can next:

Compress this to exact AAAI 2-page formatting (word count + figure placement)

Add related work citations positioning (very important for acceptance tone)

Suggest a single strong figure (DCE pipeline diagram)

Rewrite experiments to match specific tables from your paper


Just tell me 👍