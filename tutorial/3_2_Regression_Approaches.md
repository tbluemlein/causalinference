# Regression Approaches

## Double Machine Learning

```{prf:algorithm} Double Machine Learning
:label: alg-dml
:class: dropdown

**Inputs** Data $D = \{X, T, Y\}$, ML learners $\mathcal{L}_Y$ (for outcome), $\mathcal{L}_T$ (for treatment)

**Outputs** Estimated causal effect $\hat{\theta}$

1. Split data $D$ into two disjoint sets: $D_{train}$ and $D_{eval}$ *(Cross-fitting/Honesty)*

2. **Outcome Residualization**
	1. Train model $\hat{\mu}(X) = \mathcal{L}_Y(Y \sim X)$ on $D_{train}$ *(Predict $Y$ using covariates only)*
	2. Compute residuals $\tilde{Y} = Y - \hat{\mu}(X)$ on $D_{eval}$

3. **Treatment Residualization**
	1. Train model $\hat{m}(X) = \mathcal{L}_T(T \sim X)$ on $D_{train}$ *(Estimate propensity score)*
	2. Compute residuals $\tilde{T} = T - \hat{m}(X)$ on $D_{eval}$

4. **Causal Estimation**
	1. Regress outcome residuals on treatment residuals: $\tilde{Y} = \tau \tilde{T} + \epsilon$
	2. *Note:* This identifies the effect using only the "exogenous" variation in $T$

5. Return estimated treatment effect $\hat{\tau}$
```

## Instrumental Variable Approach
{cite:t}`Shalizi2025ADA`

When unobserved confounding exists, an instrument $I$ can identify the causal effect if:

1. *Relevance*: $I$ affects $T$
2. *Exogenous noise*: $I \perp U$ — the instrumental variable is independent of the unobserved confounder
3. *Exclusion restriction*: $I$ affects $Y$ only through $T$

The instrumental variable $I$ is a source of exogenous variation in $T$ that is uncorrelated with the common ancestors of $T$ and $Y$. By seeing how both $T$ and $Y$ respond to these perturbations, and using the fact that $I$ only influences $Y$ through $T$, we can deduce the causal effect of $T$ on $Y$.

```{figure} figs/4_IV.pdf
:width: 50%
:name: fig-IV

Instrumental variable $I$
```

## Two Stage Least Squares Regression

```{prf:algorithm} Two Stage Least Squares
:label: alg-2sls
:class: dropdown

**Inputs** Observed instrument $I$, treatment variable $T$, outcome $Y$

**Outputs** Estimated causal effect $\hat{\beta}$ of $T$ on $Y$

1. **Stage 1: Regress $T$ on instrument $I$** *(Isolate exogenous variation)*
	1. Estimate $\hat{\alpha}$ from $T = \alpha I + \epsilon_1$
	2. Compute predicted values $\hat{T} = \hat{\alpha} I$ *($\hat{T}$ is now independent of $U$)*

2. **Stage 2: Regress $Y$ on predicted $\hat{T}$** *(Identify causal mechanism)*
	1. Estimate $\hat{\beta}$ from $Y = \beta \hat{T} + \epsilon_2$

3. Return estimated causal effect $\hat{\beta}$
```
