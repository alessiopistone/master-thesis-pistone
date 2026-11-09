# Thesis Research Architecture: DFG Transformations and Petri-Net Discovery

## 1. Research objective

Investigate how graph-theoretical transformations of a Directly-Follows
Graph (DFG) affect the structure and quality of Petri nets discovered
from an event log.

The proposed study compares:

1.  A reference process model discovered directly from the cleaned event
    log using the Inductive Miner. (Branch A)
2.  A baseline Petri net discovered from the unmodified DFG using DFG
    Miner. (Branch B)
3.  Three Petri nets discovered after applying different
    graph-theoretical transformations to the same original DFG (Branch C):
    -   Edmonds' minimum spanning arborescence algorithm.
    -   Dijkstra's shortest-path algorithm.
    -   Ford--Fulkerson maximum-flow algorithm, with minimum-cut
        analysis for bottleneck investigation.

**Important framing:** These are not three interchangeable DFG
optimization algorithms. They solve different graph problems. The thesis
should describe them as three graph-theoretical DFG transformation or
analysis approaches, and define precisely how each output is converted
into a valid DFG before Petri-net discovery.

## 2. Overall experimental architecture

All branches start from the same cleaned event log.

``` text
Original Event Log
        |
        v
Cleaning and preprocessing
        |
        v
Cleaned Event Log
        |
        +------------------------------------+
        |                  |                 |
        v                  v                 v
     Branch A           Branch B          Branch C
        |                  |                 |
        v                  v                 v
Inductive Miner       Generate DFG       Generate DFG
        |                  |                 |
        v                  v                 +-------------------------+
   Petri Net A              |                 |            |            |
                           v                 v            v            v
                       DFG Miner         Edmonds       Dijkstra   Ford–Fulkerson
                           |                 |            |            |
                           v                 v            v            v
                      Petri Net B       Transform     Transform    Flow/cut
                                           DFG           DFG        analysis
                                             |            |            |
                                             v            v            v
                                         DFG C1        DFG C2        DFG C3
                                             |            |            |
                                             +------------+------------+
                                                          |
                                        Same DFG-to-Petri-net conversion
                                                          |
                                         +----------------+----------------+
                                         |                |                |
                                         v                v                v
                                     Petri Net C1    Petri Net C2    Petri Net C3
                                      (Edmonds)        (Dijkstra)     (Ford–Fulkerson)
```

### Models produced

  --------------------------------------------------------------------------------
  Model                   Input and method        Role
  ----------------------- ----------------------- --------------------------------
  Petri Net A             Cleaned event log →     Event-log-based reference model
                          standard Inductive      
                          Miner                   

  Petri Net B             Original DFG → DFG      Unmodified DFG baseline
                          Miner                   

  Petri Net C1            DFG → Edmonds           Arborescence-based model
                          transformation →        
                          DFG-to-Petri-net        
                          conversion              

  Petri Net C2            DFG → Dijkstra-based    Shortest-path-based model
                          transformation →        
                          DFG-to-Petri-net        
                          conversion              

  Petri Net C3            DFG → flow/cut-based    Maximum-flow/minimum-cut-based
                          transformation →        model
                          DFG-to-Petri-net        
                          conversion              
  --------------------------------------------------------------------------------

For a fair comparison between B and C1--C3, use the **same
DFG-to-Petri-net conversion method** for all four DFG-derived models.
DFG Miner is the proposed baseline converter. Confirm the precise PM4Py
API and variant in the installed version.

## 3. Why retain both an event-log reference and a DFG baseline?

A DFG is a lossy abstraction of an event log.

An event log can retain complete case traces, event order, timestamps,
case attributes, resources and other contextual information. A DFG
aggregates traces into activities, directly-follows edges, frequencies,
and start/end information.

Consequently, different event logs can produce the same DFG. The DFG may
not retain enough information to reconstruct the original case-level
behavior uniquely.

This motivates two baselines:

-   **Petri Net A (Inductive Miner):** uses the cleaned event log and
    its trace information.
-   **Petri Net B (DFG Miner):** uses the unmodified DFG and provides
    the baseline for the graph-transformation experiments.

Do not assume that A and B will have equivalent process languages or
identical behavior. They are based on different input representations
and discovery semantics.

## 4. Branch A --- Inductive Miner reference model

**Input:** Cleaned event log.

**Method:** Standard Inductive Miner applied directly to the cleaned
event log (not the IMd DFG variant).

**Output:** Petri Net A.

Purpose:

-   Provide an event-log-based reference model.
-   Retain trace-level information available in the cleaned log.
-   Provide a point of comparison for DFG-based discovery.

The Inductive Miner family discovers process structure recursively,
using constructs such as sequence, exclusive choice, parallelism and
loops. Its process-tree-based construction provides structured models
and soundness guarantees under the algorithm's assumptions.

Do not describe standard Inductive Miner and IMd as the same variant.
Standard Inductive Miner consumes an event log; IMd is a DFG-based
variant.

## 5. Branch B --- DFG Miner baseline

**Input:** DFG generated from the cleaned event log.

**Method:** DFG Miner, using the appropriate PM4Py DFG-to-Petri-net
implementation and variant.

**Output:** Petri Net B.

Purpose:

-   Establish a baseline for Petri nets discovered from an unmodified
    DFG.
-   Enable a controlled comparison with C1, C2 and C3.
-   Isolate the effect of graph transformations from the effect of
    changing the Petri-net conversion method.

Record how the DFG is constructed, including edge frequencies, start
activities and end activities.

## 6. Branch C --- Graph-theoretical transformations

Generate one original DFG from the cleaned event log. Create three
independent copies of it. Apply one method to each copy.

Do not apply the algorithms sequentially to one another's outputs. Each
C branch should start from the same original DFG so that the experiments
are comparable.

### 6.1 C1 --- Edmonds' minimum spanning arborescence

**Graph problem:** Find a minimum-weight directed spanning arborescence
rooted at a specified node, subject to the graph and algorithm's
feasibility requirements.

**Potential process-mining interpretation:**

-   Identify a directed backbone connecting activities from a selected
    root.
-   Reduce the graph to a spanning structure.
-   Investigate the trade-off between structural simplicity and loss of
    directly-follows behavior.

**Important design decisions:**

1.  Specify the root. A natural candidate is a designated start node,
    but multiple start activities may require a super-source node.
2.  Define edge costs. DFG frequencies are typically counts or
    strengths, whereas Edmonds minimizes cost. A possible transformation
    is: \[ c(u,v) = `\frac{1}{f(u,v)}`{=tex} \] where (f(u,v)) is the
    edge frequency. This makes frequent edges cheaper, but the choice
    must be justified and tested.
3.  Decide how to handle multiple start/end activities, unreachable
    nodes, disconnected components and self-loops.
4.  State explicitly that an arborescence is a tree-like structure and
    generally cannot preserve all DFG cycles, alternative paths or
    concurrency-related relations.

**Output:** Transformed DFG C1, followed by the common DFG-to-Petri-net
conversion, producing Petri Net C1.

### 6.2 C2 --- Dijkstra's shortest-path algorithm

**Graph problem:** Find a minimum-cost path from a source to a
destination in a graph with non-negative edge costs.

**Potential process-mining interpretation:**

-   Identify low-cost routes through the process graph.
-   Study important source-to-destination paths.
-   Build a subgraph from selected paths and investigate the resulting
    process model.

**Important design decisions:**

1.  Specify source and destination nodes. Consider a super-source and
    super-sink if the process has multiple start or end activities.
2.  Define non-negative edge costs. One possible frequency-based
    transformation is: \[ c(u,v) = `\frac{1}{f(u,v)}`{=tex} \] This
    favors high-frequency edges when minimizing path cost.
3.  Dijkstra returns a path, not a complete process model. Decide
    whether to use one path, paths for multiple source-destination
    pairs, or the union of selected shortest paths.
4.  Define how ties are handled and how disconnected nodes or
    unreachable destinations are treated.
5.  Recognize that retaining only selected shortest paths can remove
    valid alternative executions and loops.

**Output:** Transformed DFG C2, followed by the common DFG-to-Petri-net
conversion, producing Petri Net C2.

### 6.3 C3 --- Ford--Fulkerson maximum flow and minimum-cut analysis

**Graph problem:** Compute maximum flow between a source and destination
subject to edge capacities. The associated minimum cut identifies a
minimum-capacity set of edges separating source and destination.

**Potential process-mining interpretation:**

-   Use DFG edge frequencies as possible capacity values.
-   Investigate high-capacity routes and flow distribution.
-   Use minimum-cut analysis to identify edges forming a bottleneck
    between the chosen source and destination.

**Important distinction:** Ford--Fulkerson computes maximum flow; it
does not itself directly output a process bottleneck. Bottleneck
analysis should explicitly use the resulting flow information and, where
appropriate, minimum-cut analysis.

**Important design decisions:**

1.  Specify source and destination, including how multiple starts and
    ends are represented.
2.  Define edge capacities. DFG frequencies may be used as capacities,
    but this is a modelling assumption: observed directly-follows counts
    are not automatically physical or operational capacities.
3.  Decide how flow values are used to transform or filter the DFG.
    Maximum-flow output alone is not a transformed DFG.
4.  Define whether the transformation retains edges carrying positive
    flow, edges in a minimum cut, or another explicitly justified
    selection.
5.  Explain how cycles, alternative routes, and edges not selected by
    the flow analysis are handled.
6.  Avoid claiming that a minimum cut necessarily identifies a
    real-world operational bottleneck. It identifies a graph-theoretical
    bottleneck under the chosen source, sink and capacity model.

**Output:** Flow/cut-based transformed DFG C3, followed by the common
DFG-to-Petri-net conversion, producing Petri Net C3.

## 7. Essential methodological control

For the comparison of Petri Nets B, C1, C2 and C3:

-   Start from the exact same original DFG.
-   Keep the DFG representation and activity labels consistent.
-   Document the treatment of start and end activities.
-   Use the same DFG-to-Petri-net conversion algorithm and settings.
-   Record every edge removed, retained, added or reweighted.
-   Check whether each transformed graph remains connected in the
    required sense and whether every relevant activity remains
    reachable.
-   Check whether the resulting Petri nets are sound; do not assume
    soundness merely because a graph algorithm completed successfully.

Petri Net A is a separate event-log-based reference and should not be
presented as if it were produced by the same DFG conversion pipeline.

## 8. Evaluation plan

Evaluate both the transformed DFGs and the resulting Petri nets.

### 8.1 DFG-level evaluation

Possible measurements:

-   Number of nodes and edges before and after transformation.
-   Edge reduction percentage.
-   Retained edge-frequency mass.
-   Start-to-end reachability.
-   Number of connected components or unreachable activities.
-   Preservation of observed directly-follows relations.
-   Runtime and memory usage.
-   For flow analysis: maximum-flow value, minimum-cut capacity and cut
    edges.
-   For path analysis: path cost, path length and coverage of activities
    or observed edges.

Be careful: fewer edges do not automatically mean a better DFG.
Simplification can remove legitimate behavior.

### 8.2 Petri-net-level evaluation

  -----------------------------------------------------------------------
  Dimension               Possible metric or      Purpose
                          analysis                
  ----------------------- ----------------------- -----------------------
  Fitness                 Token-based replay      How well the model can
                          fitness or              replay observed traces
                          alignment-based fitness 

  Precision               An appropriate          Whether the model
                          precision measure,      permits excessive
                          e.g. alignment-based    behavior
                          precision               

  Generalization          A suitable              Whether the model
                          generalization measure  captures plausible
                          or held-out evaluation  unseen behavior

  Simplicity              Places, transitions,    Structural complexity
                          arcs and a justified    
                          complexity measure      

  Soundness               Workflow-net soundness  Whether the net can
                          checks                  complete correctly
                                                  under the chosen formal
                                                  definition

  Runtime                 Discovery and           Computational
                          transformation time     efficiency
  -----------------------------------------------------------------------

Use metrics whose assumptions are appropriate for the discovered model
type. State the exact PM4Py implementation, parameters and version.

### 8.3 Recommended comparisons

**Comparison 1 --- A versus B**

Compare event-log-based Inductive Miner discovery with DFG-based DFG
Miner discovery.

Research question: What differences arise when process discovery uses
the complete cleaned event log versus its DFG abstraction?

**Comparison 2 --- B versus C1, C2 and C3**

Compare the unmodified DFG baseline with each graph-transformed DFG
model.

Research question: How do the graph-theoretical transformations affect
DFG structure and the quality of the resulting Petri nets?

**Comparison 3 --- C1 versus C2 versus C3**

Compare the three graph-theoretical approaches.

Research question: Which approach provides the most useful trade-off
between simplification, retained behavior, model quality and
computational cost?

## 9. Train/test evaluation

If the research question includes generalization to unseen cases,
consider splitting the cleaned event log into training and test sets.

A possible procedure:

1.  Split cases, not individual events, to avoid putting events from the
    same case in both sets.
2.  Generate the discovery DFG from the training log.
3.  Apply the DFG transformations to the training DFG.
4.  Discover Petri nets from the resulting DFGs.
5.  Evaluate the models on held-out test traces, as well as on training
    traces.
6.  Apply a consistent procedure to the Inductive Miner reference model.

Document the split strategy, random seed, and any temporal
considerations. If the event log is time-dependent, a chronological
split may be more appropriate than a random split.

Do not use test data to select transformation parameters if the test set
is intended to provide an unbiased final evaluation.

## 10. Edge-weight design

Edge weights are central to all three graph algorithms, but each
algorithm interprets them differently.

Let (f(u,v)) be the directly-follows frequency from activity (u) to
activity (v).

  -------------------------------------------------------------------------
  Algorithm         Required edge     Possible choice     Interpretation
                    quantity                              
  ----------------- ----------------- ------------------- -----------------
  Edmonds           Cost/weight to    (c(u,v)=1/f(u,v))   Frequent edges
                    minimize                              have lower cost

  Dijkstra          Non-negative path (c(u,v)=1/f(u,v))   Frequent edges
                    cost to minimize                      are cheaper to
                                                          traverse

  Ford--Fulkerson   Capacity to       (cap(u,v)=f(u,v))   Frequent edges
                    maximize flow                         have greater
                                                          capacity
  -------------------------------------------------------------------------

These are possible modelling choices, not universally correct
conversions. Justify them theoretically and test sensitivity to
alternatives where feasible.

For example, frequency-based costs may be affected by event-log size and
skewed activity frequencies. Consider normalization or sensitivity
analysis if comparing different datasets.

## 11. Proposed research question and hypotheses

### Main research question

> To what extent can graph-theoretical algorithms, specifically minimum
> spanning arborescence, shortest-path and maximum-flow approaches,
> improve the structural characteristics and quality of process models
> discovered from Directly-Follows Graphs?

### Possible hypotheses

-   **H1:** DFG-based process discovery produces different process
    models compared with event-log-based Inductive Miner discovery.
-   **H2:** Graph-theoretical transformations can reduce DFG complexity
    while maintaining an acceptable level of process-model fitness and
    precision.
-   **H3:** The three graph-theoretical approaches produce different
    trade-offs between model simplicity, retained behavior and
    behavioral quality.

Treat these as hypotheses to test, not expected findings. Define
measurable operational criteria for terms such as "improve,"
"acceptable," and "complexity" before running the experiments.

## 12. Implementation checklist

### Data and preprocessing

-   [ ] Define event-log cleaning rules.
-   [ ] Record the number of cases, events and activities before and
    after cleaning.
-   [ ] Define handling of incomplete traces, duplicate events, missing
    timestamps and lifecycle events where relevant.
-   [ ] Ensure all branches use the same cleaned event log.

### Baselines

-   [ ] Discover Petri Net A using standard Inductive Miner on the
    cleaned event log.
-   [ ] Generate the original DFG from the cleaned event log.
-   [ ] Discover Petri Net B using DFG Miner on the original DFG.
-   [ ] Record software and PM4Py versions, variants and parameters.

### Edmonds

-   [ ] Define root and any super-source construction.
-   [ ] Define and justify edge-cost transformation.
-   [ ] Define handling of loops, multiple starts/ends and unreachable
    nodes.
-   [ ] Generate transformed DFG C1.
-   [ ] Validate graph properties and discover Petri Net C1.

### Dijkstra

-   [ ] Define source and destination or multiple source-destination
    pairs.
-   [ ] Define non-negative edge costs.
-   [ ] Define whether one path or a union of paths is retained.
-   [ ] Define tie and unreachable-node handling.
-   [ ] Generate transformed DFG C2.
-   [ ] Validate graph properties and discover Petri Net C2.

### Ford--Fulkerson

-   [ ] Define source, destination and any super-source/super-sink.
-   [ ] Define and justify edge capacities.
-   [ ] Define how maximum-flow results affect the DFG.
-   [ ] Specify minimum-cut/bottleneck analysis.
-   [ ] Generate transformed DFG C3.
-   [ ] Validate graph properties and discover Petri Net C3.

### Evaluation and reproducibility

-   [ ] Use the same DFG-to-Petri-net converter for B, C1, C2 and C3.
-   [ ] Evaluate DFG structure and Petri-net quality separately.
-   [ ] Check soundness rather than assuming it.
-   [ ] Evaluate fitness, precision, generalization and simplicity.
-   [ ] Consider held-out test cases.
-   [ ] Record runtimes and parameter settings.
-   [ ] Save the original DFG, each transformed DFG, all Petri nets and
    evaluation outputs.
-   [ ] Ensure results can be reproduced from scripts and recorded
    configuration.

## 13. Important terminology and caveats

Use precise terminology in the thesis:

-   **Standard Inductive Miner:** event-log-based discovery.
-   **IMd:** DFG-based Inductive Miner variant. It is not the same as
    standard Inductive Miner.
-   **DFG Miner:** DFG-to-Petri-net discovery method.
-   **Edmonds' algorithm:** minimum spanning arborescence, not an
    undirected minimum spanning tree.
-   **Dijkstra:** shortest-path algorithm, not a complete graph
    optimizer by itself.
-   **Ford--Fulkerson:** maximum-flow algorithm; minimum-cut analysis is
    used to identify a graph cut that may be interpreted as a bottleneck
    under the chosen capacity model.

Do not claim that any transformation necessarily improves process
quality. The transformations may simplify the graph while removing valid
behavior. The experiments should quantify that trade-off.

Also distinguish: - Structural simplification from behavioral
improvement. - Observed edge frequency from actual process capacity. -
Graph connectivity from Petri-net soundness. - A model's ability to
replay observed traces from its ability to generalize to unseen
behavior.

## 14. Concise thesis methodology summary

The cleaned event log is used to discover an event-log-based reference
Petri net with the standard Inductive Miner. The same cleaned event log
is also converted into a Directly-Follows Graph. The unmodified DFG is
used to discover a baseline Petri net with DFG Miner. Three independent
copies of the DFG are then processed using Edmonds' minimum spanning
arborescence, Dijkstra's shortest-path algorithm, and Ford--Fulkerson
maximum-flow analysis with minimum-cut investigation. Each transformed
graph is reconstructed as a DFG and converted into a Petri net using the
same DFG-to-Petri-net method as the baseline. The five resulting Petri
nets and their underlying DFGs are evaluated for behavioral quality,
structural complexity, graph properties, soundness and computational
performance.

------------------------------------------------------------------------

## Working principle for an agentic research workflow

When continuing this project, an agent should:

1.  Preserve the five-model architecture unless the researcher
    explicitly changes it.
2.  Never treat Edmonds, Dijkstra and Ford--Fulkerson as equivalent
    algorithms.
3.  Ask for or document the root/source/sink, edge-cost and capacity
    definitions before implementing each method.
4.  Start every C experiment from the same original DFG.
5.  Use the same DFG-to-Petri-net conversion method for B, C1, C2 and
    C3.
6.  Validate transformed DFGs and resulting Petri nets.
7.  Never infer that fewer edges means better process discovery.
8.  Keep implementation details, parameters, software versions and
    results reproducible.
9.  Separate established facts, design assumptions and empirical
    findings.
10. Do not fabricate experimental results or claim improvements before
    evaluation.
