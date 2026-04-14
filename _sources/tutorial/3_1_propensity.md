# Propensity Score Methods

## Propensity Score Definition

## Propensity Score Matching
Matching focuses on creating "apples-to-apples" comparisons by pairing treated units with similar control units. This algorithm typically estimates the Average Treatment Effect on the Treated (ATT).

```{prf:algorithm} Propensity Score Matching
:label: alg-psm
:class: dropdown

**Inputs** Data $D$ with covariates $X$, treatment $T$, and outcome $Y$; Caliper $\delta$

**Outputs** Estimated ATT $\hat{\tau}_{ATT}$

1. **Estimate Propensity Scores**
	1. Train model $P(T=1|X)$ (e.g., Logistic Regression) on $D$
	2. Compute $\hat{e}(x_i)$ for all individuals $i$ *(Probability of treatment)*

2. **Match Units**
	1. Split $D$ into Treated group $\mathcal{T}$ and Control group $\mathcal{C}$
	2. Initialize empty matched set $\mathcal{M} = \emptyset$
	3. For each unit $i \in \mathcal{T}$:

		1. Find unit $j \in \mathcal{C}$ that minimizes $|\hat{e}(x_i) - \hat{e}(x_j)|$
		2. If $|\hat{e}(x_i) - \hat{e}(x_j)| \leq \delta$: *(Apply caliper distance)*

			1. Add pair $(i, j)$ to $\mathcal{M}$
			2. *Optional:* Remove $j$ from $\mathcal{C}$ *(Matching without replacement)*

3. **Estimate Effect**
	1. $\hat{\tau}_{ATT} = \frac{1}{|\mathcal{M}|} \sum_{(i,j) \in \mathcal{M}} (Y_i - Y_j)$
	2. Return $\hat{\tau}_{ATT}$
```


## Inverse Propensity Score Weighing
Weighting uses Inverse Probability Weighting (IPW) to create a "pseudo-population" where the treatment is independent of measured covariates. This approach is often used to estimate the Average Treatment Effect (ATE) for the entire population. {cite:t}`austin2011`

```{prf:algorithm} Propensity Score Weighting
:label: alg-psw
:class: dropdown

**Inputs** Data $D$ with covariates $X$, treatment $T$, and outcome $Y$

**Outputs** Estimated ATE $\hat{\tau}_{ATE}$

1. **Estimate Propensity Scores**
	1. Train model $P(T=1|X)$ to obtain $\hat{e}(x_i)$
	2. *Optional:* Clip scores (e.g., $[0.05, 0.95]$) to avoid extreme weights

2. **Calculate IPW Weights**
	1. For each unit $i$ in $D$:

		1. If $T_i = 1$: $w_i = \frac{1}{\hat{e}(x_i)}$ *(Weight for Treated)*
		2. Else: $w_i = \frac{1}{1 - \hat{e}(x_i)}$ *(Weight for Control)*

3. **Estimate Effect**
	1. $\hat{Y}_1 = \frac{\sum T_i Y_i w_i}{\sum T_i w_i}$ *(Weighted mean for Treated)*
	2. $\hat{Y}_0 = \frac{\sum (1-T_i) Y_i w_i}{\sum (1-T_i) w_i}$ *(Weighted mean for Control)*
	3. $\hat{\tau}_{ATE} = \hat{Y}_1 - \hat{Y}_0$
	4. Return $\hat{\tau}_{ATE}$
```
