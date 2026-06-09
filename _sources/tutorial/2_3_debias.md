# Biases, De-biasing, and Fairness

In {doc}`2_1_assumptions` we established the four assumptions — {prf:ref}`consistency`, {prf:ref}`sutva`, {prf:ref}`positivity`, and {prf:ref}`exchangeability` — that allow causal effects to be identified from observational data. In {doc}`2_2_graphical_models` we introduced DAGs as the language for encoding and reasoning about these assumptions. In practice, **assumptions are rarely perfectly satisfied**. This chapter is a practical guide for the actuary: how to diagnose what went wrong, how to fix it, and how to ensure the resulting model is fair.

## What went wrong? — From Assumption Violations to Biases

When a causal assumption is violated, a specific bias enters the treatment effect estimate. The table below maps each assumption to the bias it produces and the diagnostic pattern visible in data.

| Violated Assumption | Bias | Diagnostic Pattern |
|---|---|---|
| {prf:ref}`exchangeability` | Confounding | Effect estimate changes when adjusting for additional covariates |
| {prf:ref}`exchangeability` (population) | Selection bias | Sample composition differs systematically from target population |
| Incorrect adjustment | Collider bias | Conditioning on a post-treatment variable *creates* an association |
| {prf:ref}`positivity` | Extreme weights | Propensity scores cluster near 0 or 1; IPW estimates are unstable |
| {prf:ref}`sutva` | Interference | Control outcomes correlate with treatment intensity in neighbouring units |
| {prf:ref}`consistency` | Treatment ambiguity | Effect estimates vary when stratifying by treatment sub-type |

The remainder of this section defines each bias precisely.

### Confounding Bias

```{prf:definition} Confounding Bias
:label: confounding-bias

**Confounding bias** occurs when a fork variable $F$ causally influences both the treatment $T$ and the outcome $Y$, and the analysis fails to adjust for $F$.
```

```{mermaid}
graph TD
    F["F (Confounder)"] --> T
    F --> Y
    T --> Y
    style F fill:#e74c3c,color:#fff
```

Confounding violates {prf:ref}`exchangeability`. The naive comparison conflates the causal effect with a baseline difference between groups:

$$
\mathbb{E}[Y \mid T{=}1] - \mathbb{E}[Y \mid T{=}0] = \underbrace{\mathbb{E}[Y(1) - Y(0)]}_{\text{ATE}} + \underbrace{\mathbb{E}[Y(0) \mid T{=}1] - \mathbb{E}[Y(0) \mid T{=}0]}_{\text{confounding bias}}
$$

In insurance, confounding arises when healthier policyholders self-select into wellness programmes, making the programme *appear* more effective than it is.

### Selection Bias

```{prf:definition} Selection Bias
:label: selection-bias

**Selection bias** arises when the sample analysed is not representative of the target population, because selection into the sample depends on variables related to both $T$ and $Y$.
```

Selection bias can occur at study entry (differential enrolment), during follow-up (differential attrition), or through post-treatment conditioning. It violates {prf:ref}`exchangeability` at the population level. In insurance, survivorship bias in long-term policy data is a common example: only policies that were not cancelled are observed.

### Collider Bias

```{prf:definition} Collider Bias
:label: collider-bias-def

**Collider bias** (Berkson's paradox) occurs when the analysis conditions on a **collider** $C$ — a common effect of $T$ and $Y$. Conditioning on $C$ opens a non-causal path between $T$ and $Y$.
```

```{mermaid}
graph TD
    T --> C["C (Collider)"]
    Y --> C
    T --> Y
    style C fill:#9b59b6,color:#fff
```

Collider bias results from **incorrect adjustment**, not from a violated assumption per se. In insurance, analysing claims conditional on whether a claim was *filed* can introduce collider bias, since filing depends on both the treatment and the outcome severity. DAG-guided variable selection ({prf:ref}`backdoor-criterion`) is the primary safeguard.

### Positivity Violations

When {prf:ref}`positivity` is violated, propensity score weights $w = 1/\hat{\pi}(x)$ become extreme, leading to high-variance, unstable estimates. In insurance, positivity fails when certain policyholder profiles are *always* or *never* eligible for a programme — e.g. a discount that is automatically applied above a certain age.

### Interference

When {prf:ref}`sutva` is violated because one unit's treatment affects another's outcome, the standard individual-level estimators are biased. In insurance, this arises when offering a group discount changes behaviour across all members of a household or employer group.

## How to fix it — The De-biasing Toolkit

The biases above are not merely theoretical concerns — they are practical obstacles that the actuary must address. The following table organises the available de-biasing strategies by *what you do*, maps each to the bias it addresses, and links to the estimation methods covered in later chapters.

| Strategy | Addresses | Covered in |
|---|---|---|
| **Adjust** (regression, propensity scores, doubly robust) | Confounding, selection | {doc}`3_1_propensity`, {doc}`3_2_Regression_Approaches` |
| **Reweight** (IPW, IPCW, overlap weighting) | Confounding, selection, positivity | {doc}`3_1_propensity` |
| **Restrict** (trimming, redefine target population) | Positivity violations | {doc}`3_1_propensity` |
| **Model the causal structure** (DAG-guided variable selection) | Collider bias, confounding | {doc}`2_2_graphical_models` |
| **Cluster or network models** | Interference / spillover | — |
| **Sensitivity analysis** | Unobserved confounding | {doc}`4_sensitivity` |

### Adjust

Include confounders $F$ as covariates in the outcome model ([Wooldridge, 2012](https://doi.org/10.1016/C2011-0-05506-1)), or use propensity score methods — matching, stratification, or inverse-probability weighting on $\pi(x) = P(T{=}1 \mid X{=}x)$ ([Rosenbaum & Rubin, 1983](https://doi.org/10.1093/biomet/70.1.41); [Austin, 2011](https://doi.org/10.1080/00273171.2011.568786)). **Doubly robust** estimators combine both approaches and are consistent if *either* the outcome model or the propensity model is correctly specified. When unmeasured confounders exist, **instrumental variables** can identify the causal effect using exogenous variation ([Angrist & Pischke, 2015](https://doi.org/10.2307/j.ctt5vhbqm)).

### Reweight

Inverse-probability weighting (IPW) creates a pseudo-population in which treatment is independent of confounders. **Inverse-probability-of-censoring weighting** (IPCW) extends this idea to correct for selection bias due to attrition or censoring. **Stabilised weights** $w^{s} = P(T{=}t) / P(T{=}t \mid X)$ reduce variance ([Austin, 2011](https://doi.org/10.1080/00273171.2011.568786)). **Overlap weighting** — with weights proportional to $\pi(x)(1-\pi(x))$ — naturally down-weights units in regions of poor overlap and is particularly useful when positivity is borderline.

### Restrict

When certain covariate strata have near-deterministic treatment assignment, the estimand itself may need to change. **Trimming** removes units with $\hat{\pi}(x) < \varepsilon$ or $\hat{\pi}(x) > 1 - \varepsilon$ (e.g. $\varepsilon = 0.05$), targeting a *trimmed* population ATE. Alternatively, **redefine the target population** to the overlap population where both treatment and control are plausible.

### Model the causal structure

Use a DAG to distinguish confounders (adjust for them) from colliders (do not condition on them) and mediators (condition only if interested in direct effects). The {prf:ref}`backdoor-criterion` and {prf:ref}`frontdoor-criterion` from {doc}`2_2_graphical_models` provide algorithmic tools for selecting the correct adjustment set.

### Cluster or network models

When interference is present, assign treatment at the group level and analyse at the cluster level. **Partial interference models** assume spillover occurs only within known clusters (e.g. households, employer groups). **Spatial or network models** explicitly model the dependence structure.

### Sensitivity analysis

{prf:ref}`exchangeability` cannot be verified from data alone. **Sensitivity analysis** quantifies how strong an unmeasured confounder would need to be to explain away the estimated effect. Methods include E-values, Rosenbaum bounds, and partial $R^2$ sensitivity — covered in detail in {doc}`4_sensitivity`.

## Is my model fair? — Discrimination and Fairness in Insurance

Beyond causal bias, actuaries face a distinct but related challenge: ensuring that pricing models do not discriminate against protected groups. EU regulation prohibits the use of protected characteristics (e.g. gender, ethnicity) for insurance pricing, but simply dropping the sensitive attribute $S$ does not solve the problem.

### Proxy Discrimination

```{prf:definition} Proxy Discrimination
:label: proxy-discrimination

**Proxy discrimination** (indirect discrimination) occurs when non-protected covariates $X$ that are correlated with the sensitive attribute $S$ allow the model to implicitly reconstruct $S$, even though $S$ is not used as an input.
```

The mechanism is the tower property of conditional expectation: $\mu(X) = \int \mu(X, s) \, \mathrm{d}P(S{=}s \mid X)$. If $X$ and $S$ are dependent, the unawareness price channels information about $S$ through $X$ ([Lindholm et al., 2022](https://arxiv.org/abs/2209.00858)).

### Three Fairness Definitions

```{prf:definition} Fairness through Unawareness
:label: fairness-unawareness

A model satisfies **fairness through unawareness** if it does not use the sensitive attribute $S$ as input: $\hat{\mu}(X) = f(X)$.
```

Unawareness is necessary but not sufficient — it does not prevent proxy discrimination.

```{prf:definition} Discrimination-Free Pricing
:label: discrimination-free-pricing

An insurance price is **discrimination-free** ([Lindholm et al., 2022](https://arxiv.org/abs/2209.00858)) if

$$
P(Y \leq y \mid X, S) = P(Y \leq y \mid X) \quad \text{for all } y
$$

i.e., the sensitive attribute $S$ carries no additional information about $Y$ beyond the non-protected covariates $X$.
```

```{prf:definition} Counterfactual Fairness
:label: counterfactual-fairness

A predictor $\hat{\mu}$ is **counterfactually fair** ([Kusner et al., 2017](https://arxiv.org/abs/1703.06856)) if, for all $s, s'$:

$$
P\bigl(\hat{\mu}_{S \leftarrow s}(X) = y \mid X{=}x, S{=}s\bigr) = P\bigl(\hat{\mu}_{S \leftarrow s'}(X) = y \mid X{=}x, S{=}s\bigr)
$$

i.e., the prediction would not change had the individual belonged to a different demographic group, all else being equal.
```

### Group Fairness Criteria as Diagnostic Checks

```{prf:remark} Group Fairness Criteria
:label: group-fairness-criteria

The machine learning literature proposes three group fairness criteria as evaluation constraints on a predictor $\hat{\mu}(X)$ ([Barocas et al., 2019](https://fairmlbook.org/)):

- **Statistical parity** (demographic parity): $\hat{\mu}(X) \perp\!\!\!\perp S$ — the price distribution is the same across groups.
- **Equalized odds**: $\hat{\mu}(X) \perp\!\!\!\perp S \mid Y$ — prediction errors are equal across groups.
- **Predictive parity**: $Y \perp\!\!\!\perp S \mid \hat{\mu}(X)$ — the model is calibrated across groups.

These criteria are useful **diagnostic checks** but cannot replace causal reasoning. [Lindholm et al. (2022)](https://arxiv.org/abs/2209.00858) show that even a genuinely discrimination-free model violates all three criteria whenever $X$ and $S$ are statistically dependent. Moreover, except in trivial cases, the three criteria are mutually incompatible ([Chouldechova, 2017](https://doi.org/10.1089/big.2016.0047)).
```

### Why Causal Inference Resolves the Fairness Problem

```{mermaid}
graph TD
    S["S (Sensitive)"] -->|proxy path| X1["X₁ (Proxy)"]
    S -->|legitimate path| X2["X₂ (Legitimate risk factor)"]
    X1 --> Y["Y (Claim)"]
    X2 --> Y
    F["F (Confounder)"] --> S
    F --> Y
    style S fill:#e74c3c,color:#fff
    style X1 fill:#f39c12,color:#fff
    style X2 fill:#27ae60,color:#fff
```

Whether a covariate is a discriminatory proxy or a legitimate risk factor depends on the **causal structure**, not the correlation matrix. A causal model allows the actuary to:

- **Include** $X_2$ — a genuine risk mechanism, even if correlated with $S$.
- **Exclude or adjust** $X_1$ — a proxy that merely transmits discriminatory information from $S$.
- **Account for** $F$ — a confounder creating spurious associations between $S$ and $Y$.

Without a DAG, removing the influence of $S$ either does too little (unawareness) or too much (statistical parity). Counterfactual fairness is inherently a causal question: *"would this price change if the individual had belonged to a different group?"* — and it can only be answered within the potential outcomes framework ([Kusner et al., 2017](https://arxiv.org/abs/1703.06856)).

## Putting It All Together — The Actuary's Workflow

The following workflow connects the identification theory from this chapter with the estimation methods in {doc}`3_inference` and the validation tools in {doc}`4_sensitivity`.

```{mermaid}
graph LR
    W1["1. Draw the DAG"] --> W2["2. Check assumptions"]
    W2 --> W3["3. Diagnose biases"]
    W3 --> W4["4. Select de-biasing strategy"]
    W4 --> W5["5. Estimate causal effect"]
    W5 --> W6["6. Check fairness"]
    W6 --> W7["7. Sensitivity analysis"]
    style W1 fill:#4a90d9,color:#fff
    style W2 fill:#4a90d9,color:#fff
    style W3 fill:#e74c3c,color:#fff
    style W4 fill:#e74c3c,color:#fff
    style W5 fill:#f5a623,color:#fff
    style W6 fill:#27ae60,color:#fff
    style W7 fill:#27ae60,color:#fff
```

| Step | Action | Chapter |
|---|---|---|
| 1. **Draw the DAG** | Encode domain knowledge as a directed acyclic graph | {doc}`2_2_graphical_models` |
| 2. **Check assumptions** | Verify consistency, SUTVA, positivity, exchangeability | {doc}`2_1_assumptions` |
| 3. **Diagnose biases** | Use the diagnostic table above to identify which biases may be present | This chapter |
| 4. **Select de-biasing strategy** | Choose from adjust, reweight, restrict, or restructure based on the DAG | This chapter |
| 5. **Estimate causal effect** | Apply propensity scores, DML, causal forests, or Bayesian methods | {doc}`3_inference` |
| 6. **Check fairness** | Evaluate proxy discrimination and group fairness diagnostics | This chapter |
| 7. **Sensitivity analysis** | Quantify robustness to unmeasured confounding and untestable assumptions | {doc}`4_sensitivity` |
