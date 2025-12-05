# Assumptions

## From Observational Data to Conditionally Randomized Experiments

Causal inference from observational data relies on the idea that, under the assumptions of the **Rubin Causal Model** (Rubin, 1978), an observational study can be regarded as a *conditionally randomized experiment*. 

Under the assumptions of ignorability (see below), the observed data represent the essential features of a randomized experiment, enabling the identification and consistent estimation of causal effects within the **potential outcomes framework**.

## Potential Outcomes Framework
- (Neyman, 1923; Rubin, 1974 and 1978): Rubin extended Neyman’s theory for randomized experiments to observational studies.
- Specifically, when treatment assignment is **strongly ignorable** given a set of observed covariates — that is, when the following two conditions hold:

$$
(Y(1), Y(0)) \perp T \mid X
$$

$$
0 < P(T = 1 \mid X) < 1,
$$

then conditioning on $X$ renders the treatment assignment mechanism analogous to that of a randomized controlled trial. More explanation in [assumptions guide](https://www.uniqcret.com/post/causal-inference-assumptions-guide.) and in [2020 Neal](https://www.bradyneal.com/Introduction_to_Causal_Inference-Aug27_2020-Neal.pdf)

### Assumptions
#### **(1) Consistency**: 

$$
Y(A) = Y(a) = Y \quad \text{when } A = a
$$

links the potential outcomes to the observed outcomes by requiring that the two are equal under the same treatment assignments. This ties the potential outcome $Y(a)$ to the factual outcome $Y$ when the treatment actually received is $A = a$. 

#### **(2) Stable Unit Treatment Value Assumption (SUTVA)**: 

SUTVA combines consistency and no interference. The **no interference** assumption states that:

$$
Y_i(a_i) \text{ depends only on } a_i \text{ (not on } a_j \text{ for } j \neq i)
$$

implies that there is no interference between treatment assignment and outcomes across patients. In the assumption of consistency, we are implicitly making the assumption of no interference; that is, whether one individual receives treatment (or not) has no effect on the potential outcomes of any other individual. This is encapsulated by the usual statistical ‘i.i.d.’ assumption, but it can easily be violated in a study of the effect of a vaccine or if a treatment is assigned at a group level.

#### **(3) Positivity**: 

$$
0 < P(T = 1 \mid X) < 1 \quad \text{with probability } 1
$$

or more strictly (strict positivity):

$$
\varepsilon < P(T = 1 \mid X) < 1 - \varepsilon \quad \text{with probability } 1, \text{ for some } \varepsilon > 0
$$

This states that, for any possible patient characteristic, treatment assignment is not deterministic. For all but a measure zero subset of the population, the probability of receiving treatment **and** of receiving control is non-zero.

#### **(4) Exchangeability (No unobserved confounding)**: 

$$
Y(a) \perp\!\!\!\perp A \mid X \quad \text{for all } a \in \mathcal{A}
$$

or equivalently:

$$
(Y(1), Y(0)) \perp\!\!\!\perp A \mid X
$$

This implies that conditioning on the patient characteristics (covariates $X$) is sufficient to remove confounding bias in estimated HTEs. This is also called *conditional exchangeability*, *conditional ignorability*, or *causal sufficiency*.

By exchangeability $(4)$ and consistency $(1)$, the estimation of the average (causal) treatment effect (causal inference) can be done based on observed data:

$$
\mathbb{E}[Y(a)|T=t] 
\overset{(4)}{=}\mathbb{E}[Y(a)|T=t, X=x]
\overset{(1)}{=}\mathbb{E}[Y|T=t, X=x]
$$


## Collider Bias

## Selection Bias
