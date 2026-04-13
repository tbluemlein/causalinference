# Concepts of Causal Inference

## Randomized Controlled Trials
The **"gold standard"** for causal inference is the Randomized Controlled Trial (RCT). Randomization in treatment assignment ensures that treatment and control groups are as similar as possible, eliminating confounding and ensuring the treatment is independent of potential outcomes.

## Fundamental Problem of Causal Inference
Every unit has two potential outcomes but only one can be observed. Because we cannot "re-run" time to see what would have happened to the same person under a different treatment, we cannot directly calculate individual treatment effects.

## Potential Outcome Framework 
The potential outcomes framework (Neyman, 1923; Rubin, 1974 and 1978) posits that for every unit, there are multiple outcomes that could happen, but we only ever observe the one corresponding to the treatment.

### Observational Data
Causal inference from observational data relies on the idea that, under the assumptions of the **Rubin Causal Model** (Rubin, 1978), an observational study can be regarded as a *conditionally randomized experiment*. Under the assumptions of ignorability, the observed data represent the essential features of a randomized experiment, enabling the identification and consistent estimation of causal effects. 

### Identifiability
Essentially, an effect is identifiable from observational data if, with a set of structural assumptions, you can de-bias confounders to reveal the true causal effect.


### Treatment Effect Estimation
* **Average Treatment Effect (ATE):** The population-level causal effect:
    $$\tau = \mathbb{E}[Y(1) - Y(0)]$$
* **Conditional Average Treatment Effect (CATE):** The effect for a specific subpopulation defined by characteristics $X$:
    $$\tau(x) = \mathbb{E}[Y(1) - Y(0) \mid X=x]$$
* **Average Treatment Effect on the Treated (ATT):** The effect specifically for those who received the intervention:
    $$\text{ATT} = \mathbb{E}[Y(1) - Y(0) \mid T=1]$$

### Propensity Score
The probability of receiving treatment given a set of observed covariates $X$, defined as:
$$\pi = \mathbb{P}(T=1|X=x)$$





---

**Resources:**
* [Assumptions Guide](https://www.uniqcret.com/post/causal-inference-assumptions-guide)
* [Introduction to Causal Inference (Brady Neal, 2020)](https://www.bradyneal.com/Introduction_to_Causal_Inference-Aug27_2020-Neal.pdf)