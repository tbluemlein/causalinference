# Concepts of Causal Inference

## Association is not Causation

A central lesson of statistics is that **correlation does not imply causation**. Two variables can be strongly associated without one causing the other. Classic examples include the correlation between ice cream sales and drowning rates (both driven by summer weather) or the correlation between the number of firefighters at a fire and the damage caused (both driven by fire severity).

In **actuarial science**, this distinction is especially consequential. Insurance data is inherently observational: policyholders are not randomly assigned to risk factors or interventions. A pricing model may find that policyholders who purchase additional coverage have higher claim rates — but this likely reflects **adverse selection** (high-risk individuals self-selecting into more coverage), not a causal effect of coverage on claims.

Confusing association with causation leads to flawed decisions:
- **Pricing:** Adjusting premiums based on a spurious predictor introduces cross-subsidisation.
- **Interventions:** A wellness programme that *appears* to reduce claims may simply attract healthier policyholders (**healthy user bias**).
- **Reserving:** Trend extrapolations based on confounded associations can systematically over- or under-reserve.

Causal inference provides the tools to move beyond "what predicts $Y$?" to "what happens to $Y$ if we intervene on $T$?" — the question that matters for decision-making ([Angrist & Pischke, 2015](https://doi.org/10.2307/j.ctt5vhbqm); [Python Causality Handbook, Ch. 1](https://matheusfacure.github.io/python-causality-handbook/01-Introduction-To-Causality.html)).

## Treatments

A **treatment** (or intervention) is the variable whose causal effect we want to study. We denote it $T$.

In the simplest **binary** setting, $T \in \{0, 1\}$, where $T=1$ indicates that the unit received the active treatment and $T=0$ indicates control (no treatment, placebo, or standard of care). The framework generalises to **multi-valued** ($T \in \{0,1,\dots,K\}$) and **continuous** treatments ($T \in \mathbb{R}$), though most of this tutorial focuses on the binary case.

A treatment must be a **well-defined intervention**: something that could, at least in principle, be manipulated or assigned to a unit. This is sometimes called the *"no causation without manipulation"* principle ([Rubin, 1974](https://doi.org/10.1037/h0037350); [Angrist & Pischke, 2015](https://doi.org/10.2307/j.ctt5vhbqm)). Vague or immutable attributes (e.g. "being older" or "being male") are problematic because it is unclear what it would mean to intervene on them, making the potential outcomes ill-defined.

## Randomized Controlled Trials
The **"gold standard"** for causal inference is the Randomized Controlled Trial (RCT). Randomization in treatment assignment ensures that treatment and control groups are as similar as possible, eliminating confounding and ensuring the treatment $T$ is independent of potential outcomes ([Rubin, 1974](https://doi.org/10.1037/h0037350); [Angrist & Pischke, 2015](https://doi.org/10.2307/j.ctt5vhbqm)).

## Fundamental Problem of Causal Inference
Using binary treatments, every unit $i$ has two **potential outcomes** — $Y_i(1)$ under treatment and $Y_i(0)$ under control — but only one can ever be observed. The observed outcome is the **factual**; the outcome under the alternative treatment is the **counterfactual**. Since we cannot reset time to see what would have happened to the same unit under a different treatment, it is impossible to directly calculate individual treatment effects $\tau_i = Y_i(1) - Y_i(0)$. This fundamental identification problem was formalised by [Rubin (1974)](https://doi.org/10.1037/h0037350) and is discussed in detail in [Angrist & Pischke (2015, Ch. 1)](https://doi.org/10.2307/j.ctt5vhbqm).

## Potential Outcome Framework 
The potential outcomes framework ([Rubin, 1974](https://doi.org/10.1037/h0037350)) posits that for every unit, there are multiple outcomes that could happen, but we only ever observe the one corresponding to the treatment. See also the [Causal Inference Tutorial](https://bookdown.org/mike/data_analysis/sec-causal-inference.html) and [Python Causality Handbook (Ch. 2)](https://matheusfacure.github.io/python-causality-handbook/02-Randomised-Experiments.html) for accessible introductions.

### Notation

Throughout this tutorial we adopt the following conventions. Let $D = \{(X_i, T_i, Y_i)\}_{i=1}^{n}$ denote the observed dataset, where for each unit $i$:

| Symbol | Meaning |
|--------|---------|
| $X$ | Observed covariates (patient/policyholder characteristics) |
| $T$ | Treatment assignment ($T \in \{0,1\}$ in the binary case) |
| $Y$ | Observed outcome |
| $Y(1), Y(0)$ | Potential outcomes under treatment and control |
| $C$ | Confounder (variable affecting both $T$ and $Y$) |
| $M$ | Mediator (variable on the causal path from $T$ to $Y$) |
| $\pi(x)$ | Propensity score: $\pi(x) = \mathbb{P}(T=1 \mid X=x)$ |

### Assignment Mechanism

The **assignment mechanism** describes the process by which units come to receive a particular treatment. In an RCT the mechanism is known and controlled by the experimenter. In observational data, treatment is instead determined by factors such as self-selection, physician decisions, or policy rules — and these factors may themselves be related to the outcome ([Wooldridge, 2012](https://doi.org/10.1016/C2011-0-05506-1)). Understanding (or modelling) the assignment mechanism is the central challenge of causal inference from observational data, and it is what the identification assumptions (consistency, positivity, exchangeability) are designed to address.

### Observational Data
Causal inference from observational data relies on the idea that, under the assumptions of the **Rubin Causal Model** ([Rosenbaum & Rubin, 1983](https://doi.org/10.1093/biomet/70.1.41)), an observational study can be regarded as a *conditionally randomized experiment*. Under the assumptions of ignorability, the observed data $D$ represent the essential features of a randomized experiment, enabling the identification and consistent estimation of causal effects. 

### Confounding

A **confounder** $C$ is a variable that causally influences both the treatment assignment $T$ and the outcome $Y$. When confounders are present but not adjusted for, the observed association between $T$ and $Y$ is a mixture of the true causal effect and the spurious association induced by the confounder — this is **confounding bias** ([Wooldridge, 2012](https://doi.org/10.1016/C2011-0-05506-1); [Angrist & Pischke, 2015](https://doi.org/10.2307/j.ctt5vhbqm)). For a visual tutorial on confounding via Simpson's Paradox, see [this simulation walkthrough](https://www.biostatistics.ca/when-data-lies-simpsons-paradox-a-step-by-step-simulation-code-notebook/).

$$
\underbrace{\mathbb{E}[Y \mid T=1] - \mathbb{E}[Y \mid T=0]}_{\text{observed difference}} \;=\; \underbrace{\mathbb{E}[Y(1) - Y(0)]}_{\text{causal effect (ATE)}} \;+\; \underbrace{\text{bias}}_{\text{due to confounding}}
$$

The goal of causal inference methods (matching, weighting, regression adjustment, etc.) is to eliminate this bias by appropriately adjusting for the confounders.

### Identifiability

A causal effect is **identifiable** if it can be expressed purely in terms of the observed data distribution, given a set of structural assumptions.

The key distinction is between a **causal estimand** — defined via potential outcomes (e.g. $\mathbb{E}[Y(1) - Y(0)]$) — and a **statistical estimand** — a quantity computable from the observed data (e.g. $\mathbb{E}[Y \mid T=1, X] - \mathbb{E}[Y \mid T=0, X]$). Identifiability is the bridge: the assumptions of consistency, positivity, and exchangeability allow us to equate the causal estimand with a statistical estimand, making estimation possible. For a formal treatment, see [Oxford: Causal Assumptions](https://www.stats.ox.ac.uk/~evans/APTS/causassmp.html) and the [Assumptions Guide](https://www.uniqcret.com/post/causal-inference-assumptions-guide).



For heterogeneous treatment effect estimation, see [Athey & Imbens (2016)](https://doi.org/10.1073/pnas.1510489113), [Wager & Athey (2018)](https://doi.org/10.1080/01621459.2017.1319839), and [Schmidt (2018)](https://doi.org/10.48550/arXiv.1810.13237).

### Propensity Score
The probability of receiving treatment given a set of observed covariates $X$, defined as:
$$\pi(x) = \mathbb{P}(T=1 \mid X=x)$$

The propensity score was introduced by [Rosenbaum & Rubin (1983)](https://doi.org/10.1093/biomet/70.1.41). For a practical introduction to propensity score methods, see [Austin (2011)](https://doi.org/10.1080/00273171.2011.568786).



---

**Resources:**
* [Assumptions Guide](https://www.uniqcret.com/post/causal-inference-assumptions-guide)
* [Introduction to Causal Inference (Brady Neal, 2020)](https://www.bradyneal.com/Introduction_to_Causal_Inference-Aug27_2020-Neal.pdf)
* [Python Causality Handbook](https://matheusfacure.github.io/python-causality-handbook/)
* [Causal ML Book](https://www.causalmlbook.com/)
