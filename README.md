# Causal Inference Tutorial

This tutorial demonstrates how we can leverage modern causal machine learning (ML) and data science algorithms to infer causal effects from observational data. While standard ML excels at predicting outcomes, it often remains "causally blind" to the true levers of risk. By moving beyond passive risk measurement toward active and interventional risk management, we explore methods how to quantify causal treatment effects to achieve intelligent risk mitigation. This endeavour is illustrated on a simulated health data set of longitudinal health data and on a second dataset that contains driver training assignments in a motor insurance context where we apply different causal inference methodologies to estimate heterogeneous treatment effects and derive fair interventions.

## Introduction and overview
This study has been carried out for the working group "Data Science" of the Swiss Association of Actuaries SAV, see [https://www.actuarialdatascience.org](https://www.actuarialdatascience.org). The historical responsibility of the actuary has always been to ensure financial and societal stability. By building a collective of insureds, insurance ensures that unforeseeable events do not destabilize society. Traditionally, we relied on identifying historical correlations in claims data to categorize and understand risk. With increasing availability of real-time data, advanced ML methods can perform predictive analytics, i.e., forecast disease trajectories or large losses.

Today, in the era of AI, actuarial data science evolves towards prescriptive analytics and intelligent disaster management. Causal inference empowers this transition. It allows us to leverage modern AI algorithms to infer causal effects from observational data. While predictive models identify which factors are associated with loss, true risk management requires understanding the causal effect of an intervention: "If we implement this preventative measure, by how much will we actually reduce the expected loss?".

By identifying true causal drivers rather than mere symptoms, we move from passive risk measurement to active risk mitigation. We can then actively prevent losses before they occur or engage in intelligent disaster management, i.e., trigger interventions that act as true levers for long-term health and financial stability.  Furthermore, by isolating these causal effects, we can eliminate systemic biases and ensure that insurance pricing is not only statistically robust but ethically fair. This is our next step in ensuring a more stable and just society.

## Organisation

The tutorial guides the reader from foundational concepts, identificazion and infetence of causal effects, to the validation of causal conclusions.

```{mermaid}
graph LR
    A["1. Concepts"] --> B["2. Identification"]
    B --> C["3. Inference"]
    C --> D["4. Sensitivity"]
    style A fill:#4a90d9,color:#fff
    style B fill:#e74c3c,color:#fff
    style C fill:#f5a623,color:#fff
    style D fill:#27ae60,color:#fff
```

**Stage 1 — {doc}`tutorial/1_concepts`:** Introduces the language of causal inference — treatments, potential outcomes, counterfactuals, confounding — and motivates why association is not causation, especially in actuarial applications.

**Stage 2 — {doc}`tutorial/2_identification`:** Establishes *when* causal effects can be recovered from observational data. This requires verifying the causal assumptions and using graphical models to select correct adjustment sets.
- {doc}`tutorial/2_1_assumptions` — Consistency, SUTVA, positivity, exchangeability, and how to detect violations.
- {doc}`tutorial/2_2_graphical_models` — DAGs, d-separation, backdoor and frontdoor criteria, causal discovery.
- {doc}`tutorial/2_3_debias` — Catalogue of biases (confounding, selection, collider) and mitigation strategies.

**Stage 3 — {doc}`tutorial/3_inference`:** Covers *how* to estimate causal effects once identification is established. Methods range from classical propensity score approaches to modern machine learning estimators.
- {doc}`tutorial/3_1_propensity` — Propensity score matching and inverse probability weighting.
- {doc}`tutorial/3_2_Regression_Approaches` — Double machine learning and instrumental variables / 2SLS.
- {doc}`tutorial/3_3_causal_tree` — Causal trees for heterogeneous treatment effect discovery.
- {doc}`tutorial/3_4_causal_forest` — Causal forests for individualised treatment effect estimation.
- {doc}`tutorial/3_5_bayesian` — Bayesian causal inference with BART and Bayesian Causal Forests.

**Stage 4 — {doc}`tutorial/4_sensitivity`:** Validates causal conclusions by assessing their robustness to untestable assumptions. Covers balance diagnostics, placebo tests, E-values, Rosenbaum bounds, and partial $R^2$ sensitivity analysis.
