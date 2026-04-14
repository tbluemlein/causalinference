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

1. *Relevance*: $I$ affects $X$
2. *Exogenous noise*: $I \perp U$ The instrumental variable is independent from the unobserved confounder
3. *Exclusion restriction*: $I$ affects $Y$ only through $X$ (there is a string correlation between the instrument and the covariates)

The instrumental variable $I$ is source of variation in $X$ that's uncorrelated with the common ancestors of $X$ and $Y$. By seeing how both $X$ and $Y$ respond
to these perturbations, and using the fact that $I$ only influences $Y$ through $X$, we can deduce something about how X influences Y, i.e., the treatment effect.

```{figure} figs/4_IV.pdf
:width: 50%
:name: fig-IV

Instrumental variable $I$
```

## Two Stage Least Squares Regression

```{prf:algorithm} Two Stage Least Squares
:label: alg-2sls
:class: dropdown

**Inputs** Observed instrument $I$, treatment variable $X$, outcome $Y$

**Outputs** Estimated causal effect $\hat{\beta}$ of $X$ on $Y$

1. **Stage 1: Regress $X$ on instrument $I$** *(Isolate exogenous variation)*
	1. Estimate $\hat{\alpha}$ from $X = \alpha I + \epsilon_1$
	2. Compute predicted values $\hat{X} = \hat{\alpha} I$ *($\hat{X}$ is now independent of $U$)*

2. **Stage 2: Regress $Y$ on predicted $\hat{X}$** *(Identify causal mechanism)*
	1. Estimate $\hat{\beta}$ from $Y = \beta \hat{X} + \epsilon_2$

3. Return estimated causal effect $\hat{\beta}$
```
