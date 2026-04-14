# Sensitivity Analysis

The identification of causal effects from observational data rests on untestable assumptions — most critically, {prf:ref}`exchangeability` (no unmeasured confounding). **Sensitivity analysis** asks: *how robust are our conclusions to violations of these assumptions?* This chapter surveys the main approaches, following [Rosenbaum (2002)](https://doi.org/10.1007/978-1-4757-3692-2), [Cinelli & Hazlett (2020)](https://doi.org/10.1111/rssb.12348), and [Shalizi (2025)](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf).

## Why Sensitivity Analysis?

Even with careful adjustment for observed confounders, the possibility of **unmeasured confounding** can never be ruled out in observational data. Sensitivity analysis complements point estimation by answering:

1. **How strong** would an unmeasured confounder $U$ need to be to explain away the observed effect?
2. **How much** would the estimated treatment effect change under plausible confounding scenarios?
3. **What are the bounds** on the true effect under worst-case confounding?

Without sensitivity analysis, causal conclusions from observational data remain fundamentally incomplete.

## Balance Diagnostics

Before performing sensitivity analysis for unmeasured confounding, it is essential to verify that **measured confounders are adequately balanced** after adjustment. Balance diagnostics assess whether the adjustment method (matching, weighting, regression) has successfully eliminated observed confounding ([Austin, 2011](https://doi.org/10.1080/00273171.2011.568786)).

```{prf:definition} Standardised Mean Difference (SMD)
:label: smd

The **standardised mean difference** for a covariate $X_j$ between treated and control groups is:

$$
\text{SMD}_j = \frac{\bar{X}_{j,1} - \bar{X}_{j,0}}{\sqrt{(s_{j,1}^2 + s_{j,0}^2) / 2}}
$$

where $\bar{X}_{j,t}$ and $s_{j,t}^2$ are the (weighted) mean and variance of $X_j$ in treatment group $t$.
```

A common threshold is $|\text{SMD}| < 0.1$ for adequate balance. For propensity-score-based methods, compare SMDs before and after weighting/matching across all covariates. Poor balance signals residual confounding that undermines the analysis.

Additional diagnostics include:
- **Propensity score overlap plots:** Histograms or density plots of $\hat{\pi}(x)$ by treatment group.
- **Variance ratios:** The ratio of covariate variances between groups (target: close to 1).
- **Love plots:** Visual display of SMDs for all covariates, before and after adjustment.

## Placebo and Falsification Tests

```{prf:definition} Placebo Test
:label: placebo-test

A **placebo test** (falsification test) applies the causal estimator to a setting where the true effect is known to be zero. If the estimator reports a non-zero effect, this signals bias (likely from unmeasured confounding or model misspecification).
```

Common designs:
- **Negative control outcome:** Estimate the effect of $T$ on an outcome $\tilde{Y}$ that $T$ cannot plausibly affect. A non-zero estimate implies residual confounding ([Lipsitch, Tchetgen & Cohen, 2010](https://doi.org/10.1097/EDE.0b013e3181d8d195)).
- **Negative control treatment:** Estimate the effect of a "treatment" $\tilde{T}$ that cannot plausibly affect $Y$. A non-zero estimate again signals confounding.
- **Pre-treatment outcome test:** If pre-treatment outcome data exists, test whether the "treatment" predicts the outcome *before* it was administered. A significant effect indicates confounding.

In insurance applications, a placebo test might assess whether a health intervention $T$ "affects" a car insurance claim outcome — an effect here would indicate systematic differences between groups unrelated to the intervention.

## Rosenbaum Bounds

[Rosenbaum (2002)](https://doi.org/10.1007/978-1-4757-3692-2) developed a framework for bounding the effect of unmeasured confounding in matched observational studies.

```{prf:definition} Rosenbaum's Sensitivity Parameter $\Gamma$
:label: rosenbaum-gamma

In a matched pair $(i, j)$ with similar observed covariates, the sensitivity parameter $\Gamma \geq 1$ bounds the ratio of treatment assignment odds:

$$
\frac{1}{\Gamma} \leq \frac{P(T_i = 1 \mid X_i) / P(T_i = 0 \mid X_i)}{P(T_j = 1 \mid X_j) / P(T_j = 0 \mid X_j)} \leq \Gamma
$$

When $\Gamma = 1$, treatment assignment is random within matched pairs (no unmeasured confounding). As $\Gamma$ increases, more confounding is allowed.
```

For each value of $\Gamma$, Rosenbaum's method computes **worst-case p-values** and confidence intervals. The analysis reports the **critical $\Gamma$** at which the effect would no longer be statistically significant — a larger critical $\Gamma$ indicates a more robust finding.

## E-Values

The **E-value** ([VanderWeele & Ding, 2017](https://doi.org/10.7326/M16-2607)) provides a simple, model-free summary of sensitivity to unmeasured confounding.

```{prf:definition} E-Value
:label: e-value

The **E-value** for an observed risk ratio $\text{RR}_{\text{obs}}$ is:

$$
E = \text{RR}_{\text{obs}} + \sqrt{\text{RR}_{\text{obs}} \times (\text{RR}_{\text{obs}} - 1)}
$$

The E-value represents the **minimum strength of association** (on the risk ratio scale) that an unmeasured confounder $U$ would need to have with *both* the treatment $T$ and the outcome $Y$, conditional on measured covariates, to fully explain away the observed effect.
```

A large E-value means the observed association is robust: only a very strong unmeasured confounder could explain it away. A small E-value indicates vulnerability to even moderate unmeasured confounding.

For treatment effects on continuous outcomes, analogous E-values can be computed by first converting the effect to an approximate risk ratio scale.

## Partial $R^2$ and Omitted Variable Bias

[Cinelli & Hazlett (2020)](https://doi.org/10.1111/rssb.12348) provide a regression-based sensitivity analysis framework using the **partial $R^2$** — the proportion of residual variance explained by an omitted confounder.

```{prf:definition} Partial $R^2$ Sensitivity
:label: partial-r2

Let $R^2_{Y \sim U \mid T, X}$ denote the partial $R^2$ of the omitted confounder $U$ with the outcome $Y$ (after adjusting for $T$ and $X$), and $R^2_{T \sim U \mid X}$ the partial $R^2$ with the treatment $T$. The bias in the treatment effect estimate due to omitting $U$ is bounded by:

$$
|\text{bias}| \leq \sqrt{R^2_{Y \sim U \mid T, X} \cdot R^2_{T \sim U \mid X}} \cdot \frac{\text{SD}(Y_{\text{res}})}{\text{SD}(T_{\text{res}})}
$$

where $Y_{\text{res}}$ and $T_{\text{res}}$ are residuals from regressions on $X$.
```

This framework is particularly intuitive because the required confounding strengths can be **benchmarked against observed covariates**: "the unmeasured confounder would need to be as strong as [observed covariate $X_j$] to reduce the effect to zero."

The `sensemakr` R package implements this approach and produces **contour plots** showing how the estimated effect changes across a grid of $(R^2_{Y \sim U \mid T, X}, R^2_{T \sim U \mid X})$ values.

## Bounds on Treatment Effects

When parametric assumptions are undesirable, **partial identification** provides worst-case bounds on treatment effects under minimal assumptions.

```{prf:definition} Manski Bounds
:label: manski-bounds

Under no assumptions beyond bounded outcomes ($Y \in [y_{\min}, y_{\max}]$), the ATE is bounded by:

$$
\mathbb{E}[Y \mid T=1] - y_{\max} \cdot P(T=0) - \mathbb{E}[Y \mid T=0] \cdot P(T=0) \;\leq\; \tau \;\leq\; \mathbb{E}[Y \mid T=1] + y_{\max} \cdot P(T=0) - \mathbb{E}[Y \mid T=0]
$$

These bounds are **sharp** (cannot be tightened without additional assumptions) but often wide. Adding monotonicity or instrumental variable assumptions narrows them considerably.
```

## Recommended Sensitivity Analysis Workflow

1. **Balance diagnostics:** Verify covariate balance (SMDs, overlap plots) after adjustment.
2. **Placebo/falsification tests:** Check negative controls for residual bias.
3. **E-values:** Compute for the main estimate and the confidence interval bound closest to the null.
4. **Partial $R^2$ analysis:** Benchmark against observed covariates using `sensemakr`.
5. **Rosenbaum bounds** (if using matching): Report the critical $\Gamma$.
6. **Report transparently:** Present the main estimate alongside sensitivity results. State explicitly how strong unmeasured confounding would need to be to alter conclusions.
