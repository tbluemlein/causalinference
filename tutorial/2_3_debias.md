# Possible Biases and Mitigation Strategies

When the causal assumptions from {prf:ref}`consistency`, {prf:ref}`sutva`, {prf:ref}`positivity`, or {prf:ref}`exchangeability` are violated, the resulting treatment effect estimates are **biased**. This chapter catalogues the major biases that arise in observational causal inference and the strategies to mitigate them.

## Confounding Bias

```{prf:definition} Confounding Bias
:label: confounding-bias

**Confounding bias** occurs when a variable $C$ causally influences both the treatment $T$ and the outcome $Y$, and the analysis fails to adjust for $C$. The observed association between $T$ and $Y$ then conflates the causal effect with the spurious association through $C$.
```

```{mermaid}
graph TD
    C["C (Confounder)"] --> T
    C --> Y
    T --> Y
    style C fill:#e74c3c,color:#fff
```

Confounding violates {prf:ref}`exchangeability`. The bias takes the form:

$$
\mathbb{E}[Y \mid T=1] - \mathbb{E}[Y \mid T=0] = \underbrace{\mathbb{E}[Y(1) - Y(0)]}_{\text{ATE}} + \underbrace{\mathbb{E}[Y(0) \mid T=1] - \mathbb{E}[Y(0) \mid T=0]}_{\text{confounding bias (baseline difference)}}
$$

**Mitigation strategies:**
- **Regression adjustment:** Include confounders $C$ as covariates in the outcome model ([Wooldridge, 2012](https://doi.org/10.1016/C2011-0-05506-1)).
- **Propensity score methods:** Matching, stratification, or inverse-probability weighting on the propensity score $\pi(x) = P(T=1 \mid X=x)$ ([Rosenbaum & Rubin, 1983](https://doi.org/10.1093/biomet/70.1.41); [Austin, 2011](https://doi.org/10.1080/00273171.2011.568786)).
- **Doubly robust estimation:** Combines outcome modelling and propensity weighting; consistent if *either* model is correctly specified.
- **Instrumental variables:** When unmeasured confounders exist, an instrument $Z$ that affects $T$ but not $Y$ directly can identify the causal effect ([Angrist & Pischke, 2015](https://doi.org/10.2307/j.ctt5vhbqm)).

## Selection Bias

```{prf:definition} Selection Bias
:label: selection-bias

**Selection bias** arises when the sample analysed is not representative of the target population, because the selection into the sample depends on variables related to both $T$ and $Y$.
```

Selection bias can occur at study entry (differential enrolment), during follow-up (differential attrition/censoring), or through post-treatment conditioning. It violates {prf:ref}`exchangeability` at the population level even if within-sample adjustment is performed.

**Mitigation strategies:**
- **Inverse-probability-of-censoring weighting (IPCW):** Re-weight observed individuals to represent the target population.
- **Sensitivity analysis:** Bound the impact of selection on the estimated effect.
- **Careful study design:** Define inclusion/exclusion criteria that do not condition on post-treatment variables.

## Collider Bias

```{prf:definition} Collider Bias
:label: collider-bias-def

**Collider bias** (Berkson's paradox) occurs when the analysis conditions on a **collider** — a variable $S$ that is a common effect of $T$ and $Y$ (or their descendants). Conditioning on $S$ opens a non-causal path between $T$ and $Y$, inducing a spurious association.
```

```{mermaid}
graph TD
    T --> S["S (Collider)"]
    Y --> S
    T --> Y
    style S fill:#9b59b6,color:#fff
```

Collider bias does not violate the standard causal assumptions *per se*, but results from **incorrect adjustment** — conditioning on a variable that should not be conditioned on. In insurance, this can arise when analysing claims conditional on whether a claim was filed (since filing depends on both the treatment and the outcome severity).

**Mitigation strategies:**
- **Do not condition on post-treatment variables** or descendants of colliders.
- **Use DAGs** to identify colliders before selecting the adjustment set (see {prf:ref}`backdoor-criterion`).
- **Sensitivity analysis** for potential collider bias when the adjustment set is uncertain.

## Positivity Violations and Extreme Weights

When {prf:ref}`positivity` is violated, propensity score weights $w = 1/\hat{\pi}(x)$ or $w = 1/(1 - \hat{\pi}(x))$ become extreme, leading to **high-variance, unstable estimates**.

**Mitigation strategies:**
- **Trimming:** Remove units with propensity scores below $\varepsilon$ or above $1 - \varepsilon$ (e.g. $\varepsilon = 0.05$). This changes the estimand to a *trimmed* population ATE.
- **Weight truncation/stabilisation:** Cap weights at a percentile (e.g. 99th) or use stabilised weights $w^s = P(T=t) / P(T=t \mid X)$ ([Austin, 2011](https://doi.org/10.1080/00273171.2011.568786)).
- **Overlap weighting:** Use weights proportional to $\pi(x)(1-\pi(x))$, which naturally down-weight units in regions of poor overlap.
- **Redefine the target population:** Restrict to the overlap population where both treatments are plausible.

## Interference and Spillover

When {prf:ref}`sutva` is violated because one unit's treatment affects another's outcome, standard estimators are biased.

**Mitigation strategies:**
- **Cluster-level treatment assignment:** Assign treatment at the group level and analyse at the cluster level.
- **Partial interference models:** Assume interference occurs only within known clusters (e.g. households, employer groups).
- **Spatial/network models:** Explicitly model the dependence structure if interference follows a known network.

## Summary: Bias–Assumption–Mitigation Map

| Bias | Violated Assumption | Primary Mitigation |
|------|--------------------|--------------------|
| Confounding | Exchangeability | Regression, propensity scores, IV |
| Selection bias | Exchangeability (population level) | IPCW, study design |
| Collider bias | Incorrect adjustment | DAG-guided variable selection |
| Extreme weights | Positivity | Trimming, overlap weighting |
| Spillover/interference | SUTVA | Cluster randomisation, network models |
| Treatment ambiguity | Consistency | Precise treatment definition |
