# Concepts of Causal Inference

## Treatments

A **treatment** (or intervention) is the variable whose causal effect we want to study. We denote it $T$ (equivalently $A$ in some literature).

In the simplest **binary** setting, $T \in \{0, 1\}$, where $T=1$ indicates that the unit received the active treatment and $T=0$ indicates control (no treatment, placebo, or standard of care). The framework generalises to **multi-valued** ($T \in \{0,1,\dots,K\}$) and **continuous** treatments ($T \in \mathbb{R}$), though most of this tutorial focuses on the binary case.

A treatment must be a **well-defined intervention**: something that could, at least in principle, be manipulated or assigned to a unit. This is sometimes called the *"no causation without manipulation"* principle ([Rubin, 1974](papers/1974%20Rubin.pdf); [Angrist & Pischke, 2015](papers/Joshua%20D.%20Angrist%2C%20J%C3%B6rn-Steffen%20Pischke%20-%20Mastering%20%27Metrics_%20The%20Path%20from%20Cause%20to%20Effect-Princeton%20University%20Press%20(2015).pdf)). Vague or immutable attributes (e.g. "being older" or "being male") are problematic because it is unclear what it would mean to intervene on them, making the potential outcomes ill-defined.

## Randomized Controlled Trials
The **"gold standard"** for causal inference is the Randomized Controlled Trial (RCT). Randomization in treatment assignment ensures that treatment and control groups are as similar as possible, eliminating confounding and ensuring the treatment is independent of potential outcomes ([Rubin, 1974](papers/1974%20Rubin.pdf); [Angrist & Pischke, 2015](papers/Joshua%20D.%20Angrist%2C%20J%C3%B6rn-Steffen%20Pischke%20-%20Mastering%20%27Metrics_%20The%20Path%20from%20Cause%20to%20Effect-Princeton%20University%20Press%20(2015).pdf)).

## Fundamental Problem of Causal Inference
Using binary treatments, every unit $i$ has two **potential outcomes** — $Y_i(1)$ under treatment and $Y_i(0)$ under control — but only one can ever be observed. The observed outcome is the **factual**; the outcome under the alternative treatment is the **counterfactual**. Since we cannot reset time to see what would have happened to the same unit under a different treatment, it is impossible to directly calculate individual treatment effects $\tau_i = Y_i(1) - Y_i(0)$. This fundamental identification problem was formalised by [Rubin (1974)](papers/1974%20Rubin.pdf) and is discussed in detail in [Angrist & Pischke (2015, Ch. 1)](papers/Joshua%20D.%20Angrist%2C%20J%C3%B6rn-Steffen%20Pischke%20-%20Mastering%20%27Metrics_%20The%20Path%20from%20Cause%20to%20Effect-Princeton%20University%20Press%20(2015).pdf).

## Potential Outcome Framework 
The potential outcomes framework ([Rubin, 1974](papers/1974%20Rubin.pdf)) posits that for every unit, there are multiple outcomes that could happen, but we only ever observe the one corresponding to the treatment. See also the [Causal Inference Tutorial](https://bookdown.org/mike/data_analysis/sec-causal-inference.html) and [Python Causality Handbook (Ch. 2)](https://matheusfacure.github.io/python-causality-handbook/02-Randomised-Experiments.html) for accessible introductions.

### Assignment Mechanism

The **assignment mechanism** describes the process by which units come to receive a particular treatment. In an RCT the mechanism is known and controlled by the experimenter. In observational data, treatment is instead determined by factors such as self-selection, physician decisions, or policy rules — and these factors may themselves be related to the outcome ([Wooldridge, 2012](papers/2012%20Wooldridge%20-%20Introductory%20Econometrics.pdf)). Understanding (or modelling) the assignment mechanism is the central challenge of causal inference from observational data, and it is what the identification assumptions (consistency, positivity, exchangeability) are designed to address.

### Observational Data
Causal inference from observational data relies on the idea that, under the assumptions of the **Rubin Causal Model** ([Rosenbaum & Rubin, 1983](https://doi.org/10.1093/biomet/70.1.41)), an observational study can be regarded as a *conditionally randomized experiment*. Under the assumptions of ignorability, the observed data represent the essential features of a randomized experiment, enabling the identification and consistent estimation of causal effects. 

### Confounding

A **confounder** is a variable that causally influences both the treatment assignment and the outcome. When confounders are present but not adjusted for, the observed association between $T$ and $Y$ is a mixture of the true causal effect and the spurious association induced by the confounder — this is **confounding bias** ([Wooldridge, 2012](papers/2012%20Wooldridge%20-%20Introductory%20Econometrics.pdf); [Angrist & Pischke, 2015](papers/Joshua%20D.%20Angrist%2C%20J%C3%B6rn-Steffen%20Pischke%20-%20Mastering%20%27Metrics_%20The%20Path%20from%20Cause%20to%20Effect-Princeton%20University%20Press%20(2015).pdf)). For a visual tutorial on confounding via Simpson's Paradox, see [this simulation walkthrough](https://www.biostatistics.ca/when-data-lies-simpsons-paradox-a-step-by-step-simulation-code-notebook/).

$$
\underbrace{\mathbb{E}[Y \mid T=1] - \mathbb{E}[Y \mid T=0]}_{\text{observed difference}} \;=\; \underbrace{\mathbb{E}[Y(1) - Y(0)]}_{\text{causal effect (ATE)}} \;+\; \underbrace{\text{bias}}_{\text{due to confounding}}
$$

The goal of causal inference methods (matching, weighting, regression adjustment, etc.) is to eliminate this bias by appropriately adjusting for the confounders $X$.

### Identifiability

A causal effect is **identifiable** if it can be expressed purely in terms of the observed data distribution, given a set of structural assumptions.

The key distinction is between a **causal estimand** — defined via potential outcomes (e.g. $\mathbb{E}[Y(1) - Y(0)]$) — and a **statistical estimand** — a quantity computable from the observed data (e.g. $\mathbb{E}[Y \mid T=1, X] - \mathbb{E}[Y \mid T=0, X]$). Identifiability is the bridge: the assumptions of consistency, positivity, and exchangeability allow us to equate the causal estimand with a statistical estimand, making estimation possible. For a formal treatment, see [Oxford: Causal Assumptions](https://www.stats.ox.ac.uk/~evans/APTS/causassmp.html) and the [Assumptions Guide](https://www.uniqcret.com/post/causal-inference-assumptions-guide).


### Treatment Effect Estimation
* **Average Treatment Effect (ATE):** The population-level causal effect:
    $$\tau = \mathbb{E}[Y(1) - Y(0)]$$
* **Conditional Average Treatment Effect (CATE):** The effect for a specific subpopulation defined by characteristics $X$:
    $$\tau(x) = \mathbb{E}[Y(1) - Y(0) \mid X=x]$$
* **Average Treatment Effect on the Treated (ATT):** The effect specifically for those who received the intervention:
    $$\text{ATT} = \mathbb{E}[Y(1) - Y(0) \mid T=1]$$

For heterogeneous treatment effect estimation, see [Athey & Imbens (2016)](https://doi.org/10.1073/pnas.1510489113), [Wager & Athey (2018)](https://doi.org/10.1080/01621459.2017.1319839), and [Schmidt (2018)](papers/2018%20Schmidt%20-%20Heterogeneous.pdf).

### Propensity Score
The probability of receiving treatment given a set of observed covariates $X$, defined as:
$$\pi = \mathbb{P}(T=1|X=x)$$

The propensity score was introduced by [Rosenbaum & Rubin (1983)](https://doi.org/10.1093/biomet/70.1.41). For a practical introduction to propensity score methods, see [Austin (2011)](https://doi.org/10.1080/00273171.2011.568786).



---

**Resources:**
* [Assumptions Guide](https://www.uniqcret.com/post/causal-inference-assumptions-guide)
* [Introduction to Causal Inference (Brady Neal, 2020)](https://www.bradyneal.com/Introduction_to_Causal_Inference-Aug27_2020-Neal.pdf)
* [Python Causality Handbook](https://matheusfacure.github.io/python-causality-handbook/)
* [Causal ML Book](https://www.causalmlbook.com/)
