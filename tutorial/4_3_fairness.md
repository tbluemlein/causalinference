
## Why Causal Inference Resolves the Fairness Problem

Beyond causal bias, actuaries face a distinct but related challenge: ensuring that models do not discriminate against protected groups. EU regulation prohibits the use of protected characteristics (e.g. gender, ethnicity) for insurance pricing, but simply dropping the sensitive attribute $S$ does not solve the problem.

### Proxy Discrimination

```{prf:definition} Proxy Discrimination
:label: proxy-discrimination

**Proxy discrimination** (indirect discrimination) occurs when non-protected covariates $X$ that are correlated with the sensitive attribute $S$ allow the model to implicitly reconstruct $S$, even though $S$ is not used as an input.
```

The mechanism is the tower property of conditional expectation: $\mu(X) = \int \mu(X, s) \, \mathrm{d}P(S{=}s \mid X)$. If $X$ and $S$ are dependent, the unawareness price channels information about $S$ through $X$ ([Lindholm et al., 2022](https://arxiv.org/abs/2209.00858)).

### From Unawareness to Counterfactual Fairness

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

The machine learning literature evaluates a predictor against several **group fairness criteria** ([Barocas et al., 2019](https://fairmlbook.org/)). To make them concrete, recast pricing as a binary flagging decision $\hat{Y} \in \{0,1\}$ (e.g. "refer the costliest risks for review") compared against the truth $Y$. The interactive explainer in {doc}`../application/pricing` — adapted from the [Google PAIR *Measuring Fairness* explorable (Pearce, 2020)](https://pair.withgoogle.com/explorables/measuring-fairness/) — compares the four most common criteria:

- **Group unawareness**: $S$ is not an input to the model. This is {prf:ref}`fairness-unawareness` — the weakest criterion, and the one that proxy discrimination defeats.
- **Demographic (statistical) parity**: $\hat{Y} \perp\!\!\!\perp S$ — the selection rate $P(\hat{Y}{=}1 \mid S)$ is equal across groups ([Dwork et al., 2012](https://arxiv.org/abs/1104.3913)).
- **Equal opportunity**: $\hat{Y} \perp\!\!\!\perp S \mid Y{=}1$ — the true-positive rate is equal across groups, so the model misses high-cost risks at the same rate in each group ([Hardt et al., 2016](https://arxiv.org/abs/1610.02413)). Requiring equality of *both* the true- and false-positive rates is the stronger **equalised odds** criterion.
- **Equal accuracy** (overall accuracy equality): $P(\hat{Y}{=}Y \mid S)$ is equal across groups — the model is right equally often for each group ([Berk et al., 2021](https://doi.org/10.1177/0049124118782533)).

A closely related criterion is **predictive parity / calibration**: $Y \perp\!\!\!\perp S \mid \hat{\mu}(X)$ — a given score means the same thing in each group ([Chouldechova, 2017](https://doi.org/10.1089/big.2016.0047)).

These criteria are useful **diagnostic checks** but cannot replace causal reasoning. [Lindholm et al. (2022)](https://arxiv.org/abs/2209.00858) show that even a genuinely discrimination-free model violates them whenever $X$ and $S$ are statistically dependent. Moreover, except in trivial cases, the criteria are mutually incompatible at unequal base rates ([Kleinberg et al., 2017](https://arxiv.org/abs/1609.05807); [Chouldechova, 2017](https://doi.org/10.1089/big.2016.0047)).
```

### How Causal Inference Resolves the Fairness Problem

```{figure} figs/fairness_dag.svg
:width: 85%
:name: fig-fairness-dag

The fairness DAG: the sensitive attribute $S$ reaches the claim $Y$ via a discriminatory proxy path through $X_1$ and a legitimate path through the risk factor $X_2$, while the confounder $F$ creates a spurious $S$–$Y$ association.
```

The DAG makes precise why purely statistical constraints fail: not every $S \to Y$ path is illegitimate. The strength of causal inference is that it lets us reason about *which* paths are admissible instead of imposing a blanket independence requirement. Three steps follow directly from the graph:

- **Block the spurious path.** The association $S \leftarrow F \rightarrow Y$ is confounding, not discrimination. Conditioning on (or adjusting for) $F$ closes this back-door path, so that any remaining $S$–$Y$ dependence reflects genuine causal channels rather than artefacts.
- **Separate proxy from legitimate channels.** The proxy path $S \to X_1 \to Y$ is the discriminatory mechanism, whereas $S \to X_2 \to Y$ runs through a bona fide risk factor and may be defensible. **Path-specific (counterfactual) effects** let us neutralise only the unfair path while preserving the predictive signal carried by the legitimate one ([Chiappa, 2019](https://arxiv.org/abs/1802.08139); [Kusner et al., 2017](https://arxiv.org/abs/1703.06856)).
- **Construct the discrimination-free price.** Operationally, {prf:ref}`discrimination-free-pricing` is obtained by integrating the price over the *marginal* $P(S)$ rather than the conditional $P(S \mid X)$, which severs the $X$–$S$ dependence that the tower property would otherwise exploit ([Lindholm et al., 2022](https://arxiv.org/abs/2209.00858)).

**Where the Wasserstein distance fits in.** When the dependence between $X$ and $S$ cannot be fully removed — or when statistical parity is required as a hard constraint — fairness can be enforced *geometrically* via optimal transport. The idea is to map each group-conditional price distribution $P(\hat{\mu} \mid S{=}s)$ onto a common target: the **Wasserstein barycenter**, i.e. the distribution that minimises the total squared Wasserstein-2 distance to all the group distributions,

$$
\bar{P} = \arg\min_{P} \sum_{s} P(S{=}s)\, W_2^2\bigl(P,\; P(\hat{\mu} \mid S{=}s)\bigr).
$$

Projecting onto this barycenter yields (approximate) demographic parity while distorting the original prices as little as possible, since $W_2$ measures the minimal "cost" of reshaping one distribution into another ([Chzhen et al., 2020](https://arxiv.org/abs/2006.07286); [Plečko & Meinshausen, 2020](https://arxiv.org/abs/1911.06685)). Beyond repair, the Wasserstein distance also serves as a continuous **fairness metric**: $W_2\bigl(P(\hat{\mu}\mid S{=}s),\, P(\hat{\mu}\mid S{=}s')\bigr)$ quantifies how far apart the price distributions of two groups remain, complementing the binary independence tests of the group-fairness criteria above.