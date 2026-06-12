
## Why Causal Inference Resolves the Fairness Problem

Beyond causal bias, actuaries face a distinct but related challenge: ensuring that models do not discriminate against protected groups. EU regulation prohibits the use of protected characteristics (e.g. gender, ethnicity) for insurance pricing, but simply dropping the sensitive attribute $S$ does not solve the problem.

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

### How Causal Inference Resolves the Fairness Problem

```{figure} figs/fairness_dag.svg
:width: 85%
:name: fig-fairness-dag

The fairness DAG: the sensitive attribute $S$ reaches the claim $Y$ via a discriminatory proxy path through $X_1$ and a legitimate path through the risk factor $X_2$, while the confounder $F$ creates a spurious $S$–$Y$ association.
```

> TODO: How ? Wasserstein distance ? 