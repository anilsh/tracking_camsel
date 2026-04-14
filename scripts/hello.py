Here is the refined methodology section, formatted for an academic venue (e.g., AAAI), incorporating the parameter-efficient training of the Small Language Model (SLM) and formally defining the Relation Chain Generation (RCG) process.
### **3. Methodology**
We propose a neuro-symbolic Knowledge Graph Question Answering (KGQA) framework that synthesizes the generative flexibility of Small Language Models (SLMs) with the deterministic accuracy of semantic reasoning engines. The methodology is divided into two primary phases: (1) the parameter-efficient adaptation of the SLM for relation extraction, and (2) the multi-stage inference pipeline comprising Entity Linking, Relation Chain Generation (RCG), and logical execution via RDFox.
#### **3.1 Parameter-Efficient Fine-Tuning of the SLM**
To enable the SLM to accurately map natural language queries to complex relation chains without the computational overhead of full fine-tuning, we employ Low-Rank Adaptation (LoRA). Instead of updating the pre-trained weight matrix W_0 \in \mathbb{R}^{d \times k}, LoRA injects trainable rank decomposition matrices into the transformer layers.
For a given weight matrix, the forward pass is modified as:


where B \in \mathbb{R}^{d \times r} and A \in \mathbb{R}^{r \times k} are the low-rank matrices, and the rank r \ll \min(d, k).
During the training phase, the model is provided with a natural language query Q, the grounded entities E_Q, and the ground-truth relation chain R^* = \langle r_1, \dots, r_n \rangle. We optimize the parameters \Theta_{LoRA} = \{A, B\} by minimizing the standard autoregressive cross-entropy loss:


This phase effectively conditions the SLM to act as a highly specialized relation-chain generator over the target Knowledge Graph schema.
#### **3.2 Neuro-Symbolic Inference Pipeline**
During inference, the framework processes an unseen query Q through a sequential pipeline designed to ground the query, deduce the logical trajectory, and execute the symbolic search.
**3.2.1 Entity Resolution (NER and EL)**
Given the input query Q, a Named Entity Recognition (NER) module extracts a set of entity mentions M = \{m_1, m_2, \dots, m_k\}. Subsequently, the Entity Linking (EL) module grounds these mentions to specific nodes within the Knowledge Graph \mathcal{G} = (\mathcal{E}, \mathcal{R}, \mathcal{F}). For each mention m_i, the optimal entity e_i \in \mathcal{E} is selected by maximizing a disambiguation scoring function s:


This stage yields the grounded entity set E_Q, which serves as the starting node(s) for graph traversal.
**3.2.2 Relation Chain Generation (RCG)**
The core of the reasoning process relies on the fine-tuned SLM to perform Relation Chain Generation (RCG). By analyzing the query Q and the linked entities E_Q, the SLM autoregressively generates the logical sequence of relations required to answer the query.
The RCG module is designed to dynamically handle queries of varying complexity, specifically generating:
 * 1\text{-hop} chains for direct facts.
 * 2\text{-hop} chains for intermediate reasoning.
 * n\text{-hop} chains for complex, multi-step queries.
The generated relation chain R_c = \langle r_1, r_2, \dots, r_n \rangle where r_j \in \mathcal{R}, is decoded by maximizing the conditional probability modeled during the LoRA fine-tuning phase:

**3.2.3 Path Parsing and Template Instantiation**
The generated relation chain R_c^* outlines the structural traversal path but requires syntactic transformation to be machine-executable. A deterministic path parser maps R_c^* and the source entities E_Q into a formal logical query template T (e.g., a parameterized SPARQL query or Datalog rule).
Let \Phi denote the mapping function that aligns the entities with the relation sequence. The fully instantiated, executable query is defined as:

**3.2.4 Symbolic Execution via RDFox**
In the final step, T_{exec} is submitted to **RDFox**, a high-performance, in-memory semantic reasoning engine. RDFox evaluates the logical query against the facts \mathcal{F} of the Knowledge Graph \mathcal{G}. Utilizing highly optimized Datalog materialization, it traverses the exact topological path prescribed by T_{exec}.
The system returns the final answer set A, comprising all entities that satisfy the logical conditions of the generated relation chain originating from the linked entities:

