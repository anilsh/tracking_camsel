Based on the hand-drawn architecture diagram you provided, the workflow represents a Knowledge Graph Question Answering (KGQA) pipeline that combines neural and symbolic approaches.
Here is a technical description of the proposed methodology, formatted in the style of an academic conference paper (e.g., AAAI) with formal mathematical definitions.
### **Methodology**
We propose a neuro-symbolic pipeline for answering multi-hop queries over Knowledge Graphs (KGs). The architecture leverages the reasoning capabilities of Language Models for logical path generation alongside the deterministic execution of a semantic reasoning engine. The pipeline processes an input Natural Language (NL) query through sequential stages of entity resolution, path generation, template instantiation, and logical evaluation.
**1. Entity Extraction and Linking**
Given an input natural language query Q, the system first identifies entity mentions using a Named Entity Recognition (NER) module. Let the set of extracted mentions be M = \{m_1, m_2, \dots, m_k\}.
To ground these mentions to the underlying Knowledge Graph \mathcal{G} = (\mathcal{E}, \mathcal{R}, \mathcal{F})—where \mathcal{E} is the set of entities, \mathcal{R} is the set of relations, and \mathcal{F} represents the facts—we apply an Entity Linking (EL) function. For each mention m_i, the EL module identifies the optimal corresponding entity e_i \in \mathcal{E} by maximizing a disambiguation scoring function s:


This step outputs the set of linked entities E_Q.
**2. Multi-Hop Path Generation via SLM**
Once the entities are linked, the system must deduce the logical reasoning steps required to reach the answer. This is handled by the core generation module, which utilizes a Language Model (denoted as SLM). The SLM takes both the original query Q and the linked entities E_Q to generate a sequence of relations that form a reasoning path P.
The model is capable of generating paths of variable lengths, specifically 1\text{-hop}, 2\text{-hop}, or n\text{-hop} paths. Let P = \langle r_1, r_2, \dots, r_n \rangle where r_j \in \mathcal{R}. The path is generated autoregressively by maximizing the following conditional probability:


where \theta represents the learned parameters of the SLM.
**3. Template Instantiation**
The generated path P^* provides the structural sequence of relations but is not inherently executable. To bridge the gap between generative output and symbolic execution, the "parsed paths" are fed into a **Template** module.
This module applies a deterministic mapping function \Phi that injects the linked entities E_Q into a predefined logical query template T structured by the generated path P^*. The resulting executable query (e.g., a SPARQL query or Datalog rule) is defined as:

**4. Symbolic Execution via RDFox**
In the final stage, the instantiated template T_{exec} is passed to **RDFox**, a high-performance, in-memory semantic reasoning engine. RDFox evaluates the logical query against the Knowledge Graph \mathcal{G}, leveraging its optimized Datalog reasoning capabilities to traverse the graph and retrieve the target nodes. The final answer set A is yielded by evaluating the true conditions of the template over the graph:

By combining the semantic flexibility of the SLM for path inference with the formal guarantees of RDFox for path execution, the architecture ensures both robust multi-hop reasoning and factual accuracy in the final answer A.
