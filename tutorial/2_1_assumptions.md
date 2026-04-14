# Assumptions

## From Observational Data to Conditionally Randomized Experiments

Causal inference from observational data relies on the idea that, under the assumptions of the **Rubin Causal Model** ([Rosenbaum & Rubin, 1983](https://doi.org/10.1093/biomet/70.1.41)), an observational study can be regarded as a *conditionally randomized experiment*. 

Under the assumptions of ignorability (see below), the observed data represent the essential features of a randomized experiment, enabling the identification and consistent estimation of causal effects within the **potential outcomes framework**.

## Potential Outcomes Framework
- [Rubin (1974)](papers/1974%20Rubin.pdf) extended Neyman's (1923) theory for randomized experiments to observational studies.
- Specifically, when treatment assignment is **strongly ignorable** given a set of observed covariates — that is, when the following two conditions hold ([Rosenbaum & Rubin, 1983](https://doi.org/10.1093/biomet/70.1.41)):

$$
(Y(1), Y(0)) \perp T \mid X
$$

$$
0 < P(T = 1 \mid X) < 1,
$$

then conditioning on $X$ renders the treatment assignment mechanism analogous to that of a randomized controlled trial. More explanation in the [Assumptions Guide](https://www.uniqcret.com/post/causal-inference-assumptions-guide) and in [Neal (2020)](https://www.bradyneal.com/Introduction_to_Causal_Inference-Aug27_2020-Neal.pdf). See also [Oxford: Causal Assumptions](https://www.stats.ox.ac.uk/~evans/APTS/causassmp.html) for a formal treatment.

### Assumptions

```{prf:assumption} Consistency
:label: consistency

$$
Y(A) = Y(a) = Y \quad \text{when } A = a
$$
```

Links the potential outcomes to the observed outcomes by requiring that the two are equal under the same treatment assignments. This ties the potential outcome $Y(a)$ to the factual outcome $Y$ when the treatment actually received is $A = a$ ([Rubin, 1974](papers/1974%20Rubin.pdf)).

```{prf:assumption} Stable Unit Treatment Value Assumption (SUTVA)
:label: sutva

$$
Y_i(a_i) \text{ depends only on } a_i \text{ (not on } a_j \text{ for } j \neq i)
$$
```

SUTVA combines consistency and no interference. The **no interference** assumption states that there is no interference between treatment assignment and outcomes across patients. In the assumption of consistency, we are implicitly making the assumption of no interference; that is, whether one individual receives treatment (or not) has no effect on the potential outcomes of any other individual. This is encapsulated by the usual statistical 'i.i.d.' assumption, but it can easily be violated in a study of the effect of a vaccine or if a treatment is assigned at a group level ([Angrist & Pischke, 2015](papers/Joshua%20D.%20Angrist%2C%20J%C3%B6rn-Steffen%20Pischke%20-%20Mastering%20%27Metrics_%20The%20Path%20from%20Cause%20to%20Effect-Princeton%20University%20Press%20(2015).pdf)).

```{prf:assumption} Positivity
:label: positivity

$$
0 < P(T = 1 \mid X) < 1 \quad \text{with probability } 1
$$

or more strictly (strict positivity):

$$
\varepsilon < P(T = 1 \mid X) < 1 - \varepsilon \quad \text{with probability } 1, \text{ for some } \varepsilon > 0
$$
```

This states that, for any possible patient characteristic, treatment assignment is not deterministic. For all but a measure zero subset of the population, the probability of receiving treatment **and** of receiving control is non-zero. Violations of positivity lead to extreme propensity score weights and unstable estimates ([Austin, 2011](https://doi.org/10.1080/00273171.2011.568786); [Rosenbaum & Rubin, 1983](https://doi.org/10.1093/biomet/70.1.41)).

```{prf:assumption} Exchangeability (No unobserved confounding)
:label: exchangeability

$$
Y(a) \perp\!\!\!\perp A \mid X \quad \text{for all } a \in \mathcal{A}
$$

or equivalently:

$$
(Y(1), Y(0)) \perp\!\!\!\perp A \mid X
$$
```

This implies that conditioning on the patient characteristics (covariates $X$) is sufficient to remove confounding bias in estimated HTEs. This is also called *conditional exchangeability*, *conditional ignorability*, or *causal sufficiency* ([Rosenbaum & Rubin, 1983](https://doi.org/10.1093/biomet/70.1.41); [Wooldridge, 2012](papers/2012%20Wooldridge%20-%20Introductory%20Econometrics.pdf)). This is the strongest and least verifiable of the four assumptions — see the [Assumptions Guide](https://www.uniqcret.com/post/causal-inference-assumptions-guide) for discussion.

By exchangeability ({prf:ref}`exchangeability`) and consistency ({prf:ref}`consistency`), the estimation of the average (causal) treatment effect (causal inference) can be done based on observed data:

$$
\mathbb{E}[Y(a)|T=t] 
\overset{(4)}{=}\mathbb{E}[Y(a)|T=t, X=x]
\overset{(1)}{=}\mathbb{E}[Y|T=t, X=x]
$$


## Biases and Mitigation Strategies

### Collider Bias

### Selection Bias

### Mitigation Strategies 