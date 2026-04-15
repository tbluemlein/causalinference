# Graphical Causal Models

This chapter introduces **Directed Acyclic Graphs (DAGs)** as the language for encoding causal assumptions. The presentation follows [Shalizi (2025, Chs. 21–22)](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf), with additional references to [Pearl (2009)](https://doi.org/10.1017/CBO9780511803161). See also the [Python Causality Handbook (Ch. 4)](https://matheusfacure.github.io/python-causality-handbook/04-Graphical-Models.html) for an applied introduction.

## Causal Diagrams

A causal diagram is a graph where **nodes** represent random variables and **directed edges** ($\rightarrow$) represent direct causal effects. The absence of an edge encodes the assumption that there is *no* direct causal effect between two variables.

```{prf:definition} Directed Acyclic Graph (DAG)
:label: dag

A **directed acyclic graph** $\mathcal{G} = (V, E)$ consists of:
- a finite set of **vertices** (nodes) $V = \{V_1, V_2, \dots, V_p\}$, each representing a random variable,
- a set of **directed edges** $E \subseteq V \times V$, where $(V_i, V_j) \in E$ is drawn as $V_i \rightarrow V_j$,

subject to the constraint that there are **no directed cycles**: there is no sequence $V_{i_1} \rightarrow V_{i_2} \rightarrow \cdots \rightarrow V_{i_k} \rightarrow V_{i_1}$.
```

The acyclicity constraint reflects the assumption that causes precede their effects — no variable can be its own cause through any chain of intermediate variables ([Shalizi, 2025, §21.1](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf)).

### Graph Terminology

```{prf:definition} Parents, Children, Ancestors, Descendants
:label: graph-family

Given a DAG $\mathcal{G} = (V, E)$ and a node $X \in V$:

- **Parents** of $X$: $\text{Pa}(X) = \{Z \in V : Z \rightarrow X \in E\}$
- **Children** of $X$: $\text{Ch}(X) = \{Z \in V : X \rightarrow Z \in E\}$
- **Ancestors** of $X$: all nodes $Z$ such that there exists a directed path $Z \rightarrow \cdots \rightarrow X$
- **Descendants** of $X$: all nodes $Z$ such that there exists a directed path $X \rightarrow \cdots \rightarrow Z$
```

```{mermaid}
graph LR
    Z["Z (Parent)"] --> X
    X --> W["W (Child)"]
    W --> Y["Y (Descendant of X)"]
    style X fill:#4a90d9,color:#fff
```

A **path** between two nodes is any sequence of edges connecting them, regardless of direction. A **directed path** follows the arrow directions. A **causal path** from $T$ to $Y$ is a directed path $T \rightarrow \cdots \rightarrow Y$.

## Three Fundamental Path Structures

Every path through three variables takes one of exactly three forms. Understanding these structures is the key to reasoning about confounding and adjustment ([Shalizi, 2025, §21.2](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf)).

### Chains (Mediation)

```{prf:definition} Chain (Mediator)
:label: chain

A **chain** is a path of the form $X \rightarrow M \rightarrow Y$. The variable $M$ is called a **mediator** — it transmits the causal effect of $X$ on $Y$.
```

```{mermaid}
graph LR
    X["X (Cause)"] --> M["M (Mediator)"] --> Y["Y (Effect)"]
    style M fill:#f5a623,color:#fff
```

In a chain, $X$ and $Y$ are **marginally dependent** (information flows through $M$), but **conditionally independent given $M$**: once we know $M$, learning $X$ provides no additional information about $Y$.

$$
X \perp\!\!\!\perp Y \mid M \quad \text{(in a chain)}
$$

### Forks (Common Cause / Confounding)

```{prf:definition} Fork (Common Cause)
:label: fork

A **fork** is a path of the form $X \leftarrow F \rightarrow Y$. The variable $F$ is a **common cause** (confounder) of $X$ and $Y$.
```

```{mermaid}
graph TD
    F["F (Common Cause)"] --> X
    F --> Y
    style F fill:#e74c3c,color:#fff
```

In a fork, $X$ and $Y$ are marginally dependent (the common cause $F$ induces a spurious association), but conditionally independent given $F$:

$$
X \perp\!\!\!\perp Y \mid F \quad \text{(in a fork)}
$$

This is the structure that generates **confounding bias**: if $F$ is not adjusted for, the association between $X$ and $Y$ conflates the causal effect with the spurious path through $F$.

### Colliders (Common Effect)

```{prf:definition} Collider
:label: collider

A **collider** on a path is a node $C$ where two arrowheads meet: $X \rightarrow C \leftarrow Y$. The variable $C$ is a **common effect** of $X$ and $Y$.
```

```{mermaid}
graph TD
    X --> C["C (Collider)"]
    Y --> C
    style C fill:#9b59b6,color:#fff
```

Colliders behave **opposite** to chains and forks. In a collider structure, $X$ and $Y$ are **marginally independent** — there is no open path connecting them. However, **conditioning on the collider $C$ (or any descendant of $C$) opens the path** and induces a spurious association:

$$
X \perp\!\!\!\perp Y \quad \text{but} \quad X \not\!\perp\!\!\!\perp Y \mid C \quad \text{(collider)}
$$

This is the source of **collider bias** (also called **selection bias** or **Berkson's paradox**). Adjusting for a collider — or for a descendant of a collider — creates a spurious association where none existed ([Shalizi, 2025, §21.2](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf)).

### Summary of Path Structures

| Structure | Path | Marginal | Conditional on middle node |
|-----------|------|----------|---------------------------|
| **Chain** (Mediator) | $X \rightarrow M \rightarrow Y$ | Dependent | Independent |
| **Fork** (Common Cause) | $X \leftarrow F \rightarrow Y$ | Dependent | Independent |
| **Collider** (Common Effect) | $X \rightarrow C \leftarrow Y$ | Independent | Dependent |

## $d$-Separation

The three path structures above give rise to a general graphical criterion for reading off conditional independencies from a DAG.

```{prf:definition} Blocked Path
:label: blocked-path

A path $p$ between nodes $X$ and $Y$ in a DAG is **blocked** by a set of nodes $Z$ if and only if $p$ contains a node $W$ such that either:

1. $W$ is a **non-collider** on $p$ (i.e. $W$ is in a chain or fork) **and** $W \in Z$ (we condition on it), or
2. $W$ is a **collider** on $p$ **and** neither $W$ nor any descendant of $W$ is in $Z$.
```

```{prf:definition} $d$-Separation
:label: d-separation

Two nodes $X$ and $Y$ are **$d$-separated** by a set $Z$ in a DAG $\mathcal{G}$, written $X \perp_{\mathcal{G}} Y \mid Z$, if **every** path between $X$ and $Y$ is blocked by $Z$.

If $X$ and $Y$ are not $d$-separated by $Z$, they are **$d$-connected** given $Z$.
```

$d$-separation is the graphical analogue of conditional independence. It provides a purely mechanical procedure: to check whether $X \perp\!\!\!\perp Y \mid Z$, enumerate all paths between $X$ and $Y$ and verify that each one is blocked ([Shalizi, 2025, §21.2](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf)).

### Conditional Independence

The connection between the graphical criterion ($d$-separation) and the probabilistic property (conditional independence) is formalised by two properties.

```{prf:property} Causal Markov Condition
:label: causal-markov

If a DAG $\mathcal{G}$ is a causal model for a distribution $P$, then every variable $X$ is conditionally independent of its non-descendants given its parents:

$$
X \perp\!\!\!\perp \text{NonDesc}(X) \mid \text{Pa}(X)
$$

Equivalently: if $X \perp_{\mathcal{G}} Y \mid Z$ ($d$-separation), then $X \perp\!\!\!\perp Y \mid Z$ (conditional independence in $P$).
```

The Causal Markov Condition ensures that $d$-separation implies conditional independence. The converse — that every conditional independence in the data corresponds to a $d$-separation in the graph — requires an additional assumption.

```{prf:assumption} Faithfulness
:label: faithfulness

A distribution $P$ is **faithful** to a DAG $\mathcal{G}$ if the *only* conditional independencies in $P$ are those entailed by $d$-separation in $\mathcal{G}$.

Equivalently: if $X \perp\!\!\!\perp Y \mid Z$ in $P$, then $X \perp_{\mathcal{G}} Y \mid Z$.
```

Together, the Causal Markov Condition and faithfulness give a one-to-one correspondence between $d$-separation statements and conditional independence relations ([Shalizi, 2025, §22.3](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf)).

### Example: $d$-Separation in Practice

Consider the following DAG:

```{mermaid}
graph LR
    F["F (Confounder)"] --> T
    F --> Y
    T --> M --> Y
    T --> C["C (Collider)"]
    Y --> C
    style F fill:#e74c3c,color:#fff
    style C fill:#9b59b6,color:#fff
    style M fill:#f5a623,color:#fff
```

- **$T$ and $Y$ given $\emptyset$**: The path $T \leftarrow F \rightarrow Y$ is open (fork, $F$ not conditioned on). $T$ and $Y$ are $d$-connected — **not** independent.
- **$T$ and $Y$ given $F$**: The backdoor path $T \leftarrow F \rightarrow Y$ is now blocked. The directed path $T \rightarrow M \rightarrow Y$ remains open (chain, $M$ not conditioned on). $T$ and $Y$ are $d$-connected given $F$ — but now the remaining open paths are *causal*.
- **$T$ and $Y$ given $\{F, C\}$**: Conditioning on the collider $C$ **opens** the path $T \rightarrow C \leftarrow Y$, creating collider bias. This is an **incorrect** adjustment set.


## Methods to Identify the Correct Adjustment Set

The central question in observational causal inference is: *which variables should we condition on to identify the causal effect of $T$ on $Y$?* The following criteria provide graphical answers ([Shalizi, 2025, §21.3–21.4](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf)).

### Backdoor Criterion

```{prf:criterion} Backdoor Criterion
:label: backdoor-criterion

A set of variables $Z$ satisfies the **backdoor criterion** relative to the ordered pair $(T, Y)$ in a DAG $\mathcal{G}$ if:

1. No node in $Z$ is a **descendant** of $T$, and
2. $Z$ **blocks every path** between $T$ and $Y$ that contains an arrow *into* $T$ (i.e. every "backdoor path").

If $Z$ satisfies the backdoor criterion, then the causal effect of $T$ on $Y$ is identifiable and given by the **adjustment formula**:

$$
P(Y \mid \text{do}(T=t)) = \sum_{z} P(Y \mid T=t, Z=z) \, P(Z=z)
$$
```

The adjustment formula converts the interventional distribution $P(Y \mid \text{do}(T=t))$ into a quantity computable from observational data. This is precisely the bridge between causal and statistical estimands discussed in {prf:ref}`exchangeability` ([Rosenbaum & Rubin, 1983](https://doi.org/10.1093/biomet/70.1.41)).

```{prf:algorithm} Backdoor Criterion Check
:label: backdoor-algorithm

**Input:** DAG $\mathcal{G}$, treatment $T$, outcome $Y$, candidate adjustment set $Z$

**Output:** `True` if $Z$ satisfies the backdoor criterion, `False` otherwise

1. **Check descendant condition:** For each $z_i \in Z$:
	1. If $z_i \in \text{Descendants}(T)$ in $\mathcal{G}$, return `False`
2. **Enumerate backdoor paths:** Find all paths between $T$ and $Y$ that have an arrow into $T$ (i.e. paths of the form $T \leftarrow \cdots\, Y$ or $T \leftarrow \cdots \rightarrow Y$)
3. **Check blocking:** For each backdoor path $p$:
	1. If $p$ is not blocked by $Z$ (applying the $d$-separation rules from {prf:ref}`blocked-path`), return `False`
4. Return `True`
```

```{prf:example} Applying the Backdoor Criterion
:label: backdoor-example

Consider the DAG:

$F \rightarrow T, \quad F \rightarrow Y, \quad T \rightarrow Y$

- **Candidate $Z = \{F\}$**: $F$ is not a descendant of $T$ ✓. The only backdoor path is $T \leftarrow F \rightarrow Y$, which is blocked by conditioning on $F$ ✓. The backdoor criterion is satisfied.
- **Candidate $Z = \emptyset$**: The backdoor path $T \leftarrow F \rightarrow Y$ is not blocked ✗. The criterion fails.
```

### Frontdoor Criterion

When all backdoor paths are blocked by **unobserved** confounders, the backdoor criterion cannot be applied. The frontdoor criterion provides an alternative identification strategy through an observed mediator ([Shalizi, 2025, §21.4](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf)).

```{prf:criterion} Frontdoor Criterion
:label: frontdoor-criterion

A set of variables $M$ satisfies the **frontdoor criterion** relative to $(T, Y)$ in a DAG $\mathcal{G}$ if:

1. $M$ **intercepts all directed paths** from $T$ to $Y$ (i.e. every causal path from $T$ to $Y$ passes through some $m \in M$),
2. There is **no unblocked backdoor path** from $T$ to $M$, and
3. All backdoor paths from $M$ to $Y$ are **blocked by $T$**.

If $M$ satisfies the frontdoor criterion, the causal effect is identified by:

$$
P(Y \mid \text{do}(T=t)) = \sum_{m} P(M=m \mid T=t) \sum_{t'} P(Y \mid T=t', M=m) \, P(T=t')
$$
```

```{prf:algorithm} Frontdoor Criterion Check
:label: frontdoor-algorithm

**Input:** DAG $\mathcal{G}$, treatment $T$, outcome $Y$, candidate mediator set $M$

**Output:** `True` if $M$ satisfies the frontdoor criterion, `False` otherwise

1. **Check path interception:** For each directed path $p$ from $T$ to $Y$:
	1. If $p$ does not pass through any $m_i \in M$, return `False`
2. **Check no backdoor $T \to M$:** For each $m_i \in M$:
	1. If there exists an unblocked backdoor path from $T$ to $m_i$ (not through $Y$), return `False`
3. **Check backdoor $M \to Y$ blocked by $T$:** For each $m_i \in M$:
	1. If there exists a backdoor path from $m_i$ to $Y$ that is not blocked by $\{T\}$, return `False`
4. Return `True`
```

```{prf:example} Frontdoor Criterion with Unobserved Confounding
:label: frontdoor-example

Consider the DAG where $U$ is unobserved:

$U \rightarrow T, \quad U \rightarrow Y, \quad T \rightarrow M, \quad M \rightarrow Y$

- The backdoor criterion **fails** because we cannot condition on $U$.
- **Candidate $M = \{M\}$**: All causal paths from $T$ to $Y$ go through $M$ ✓. No backdoor path from $T$ to $M$ (since $U \rightarrow T$ and $U \rightarrow Y$, but no path $T \leftarrow \cdots M$ bypassing the direct edge) ✓. The backdoor path from $M$ to $Y$ through $U$ is $M \leftarrow T \leftarrow U \rightarrow Y$, which is blocked by $T$ ✓. The frontdoor criterion is satisfied.
```

```{mermaid}
graph LR
    U["U (Unobserved)"] -.-> T
    U -.-> Y
    T --> M --> Y
    style U fill:#999,color:#fff,stroke-dasharray: 5 5
    style M fill:#f5a623,color:#fff
```

### Comparison of Criteria

| | Backdoor Criterion | Frontdoor Criterion |
|---|---|---|
| **Requires** | Observed confounders | Observed mediator |
| **Blocks** | Non-causal (backdoor) paths | Uses causal path through mediator |
| **Fails when** | Confounders are unobserved | No suitable mediator exists |
| **Adjusts for** | Common causes $F$ | Mediator $M$ via two-step identification |


## Causal Discovery

Given observational data, can we *learn* the DAG rather than assuming it? **Causal discovery** algorithms attempt to infer causal structure from conditional independence relations in the data ([Shalizi, 2025, Ch. 22](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf)).

### Markov Equivalence

```{prf:definition} Markov Equivalence Class
:label: markov-equivalence

Two DAGs are **Markov equivalent** if they encode exactly the same set of $d$-separation (conditional independence) statements. DAGs in the same equivalence class share the same **skeleton** (undirected edges) and the same set of **v-structures** (collider patterns $X \rightarrow C \leftarrow Y$ where $X$ and $Y$ are not adjacent).
```

Observational data alone can only identify the DAG up to its Markov equivalence class. Orienting all edges requires either interventional data or additional assumptions ([Shalizi, 2025, §22.3](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf)).

### The SGS Algorithm

The **SGS algorithm** (Spirtes, Glymour & Scheines, 1993) is a constraint-based procedure that recovers the Markov equivalence class from conditional independence tests. The following pseudo-code is adapted from [Shalizi (2025, §22.7)](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf).

```{prf:algorithm} SGS Algorithm
:label: sgs-algorithm

**Input:** Set of variables $V$, conditional independence oracle (or statistical test)

**Output:** Partially directed graph (CPDAG) representing the Markov equivalence class

**Phase I — Skeleton Recovery:**

1. Start with the **complete undirected graph** on $V$
2. For each pair of nodes $(X, Y)$ with $X \neq Y$:
	1. For each subset $S \subseteq V \setminus \{X, Y\}$ (in order of increasing size):
		1. Test whether $X \perp\!\!\!\perp Y \mid S$
		2. If independent: **remove** the edge $X - Y$ and record $S$ as the **separating set** $\text{Sep}(X,Y) \leftarrow S$
		3. Break (move to next pair)

**Phase II — Orient V-Structures:**

3. For each **unshielded triple** $(X, Z, Y)$ — where $X - Z$ and $Z - Y$ but $X$ and $Y$ are **not** adjacent:
	1. If $Z \notin \text{Sep}(X, Y)$: orient as $X \rightarrow Z \leftarrow Y$ (v-structure / collider)

**Phase III — Orient Remaining Edges:**

4. Repeatedly apply the following **orientation rules** until no more edges can be oriented:
	1. **Acyclicity:** If $X \rightarrow Z - Y$ and $X$ and $Y$ are not adjacent, orient as $Z \rightarrow Y$
	2. **No new v-structures:** If there is a directed path $X \rightarrow \cdots \rightarrow Y$ and an undirected edge $X - Y$, orient as $X \rightarrow Y$
```

The SGS algorithm is correct under the assumptions of the Causal Markov Condition ({prf:ref}`causal-markov`) and faithfulness ({prf:ref}`faithfulness`). In practice, the **PC algorithm** (a computationally efficient variant) is more commonly used: it restricts the conditioning sets in Phase I to neighbours of $X$ or $Y$ in the current skeleton, greatly reducing the number of tests ([Shalizi, 2025, §22.4](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf)).

```{prf:remark}
:label: discovery-limitations

Causal discovery from observational data has fundamental limitations:
- It can only recover the **Markov equivalence class**, not the unique DAG.
- It requires **faithfulness**, which can be violated when causal effects cancel.
- It assumes **no latent confounders** (for the basic SGS/PC algorithms; extensions like FCI handle latent variables).
- Statistical tests for conditional independence have limited power in finite samples, especially with many conditioning variables.
```
