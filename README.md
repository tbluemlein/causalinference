# Causal Inference Tutorial

This tutorial demonstrates how we can leverage modern causal machine learning (ML) and data science algorithms to infer causal effects from observational data. While standard ML excels at predicting outcomes, it often remains "causally blind" to the true levers of risk. By moving beyond passive risk measurement toward active and interventional risk management, we explore methods how to quantify causal treatment effects to achieve intelligent risk mitigation. This endeavour is illustrated on a simulated health data set of longitudinal health data and on a second dataset that contains driver training assignments in a motor insurance context where we apply different causal inference methodologies to estimate heterogeneous treatment effects and derive fair interventions.

## Introduction and overview
This study has been carried out for the working group "Data Science" of the Swiss Association of Actuaries SAV, see [https://www.actuarialdatascience.org](https://www.actuarialdatascience.org). The historical responsibility of the actuary has always been to ensure financial and societal stability. By building a collective of insureds, insurance ensures that unforeseeable events do not destabilize society. Traditionally, we relied on identifying historical correlations in claims data to categorize and understand risk. With increasing availability of real-time data, advanced ML methods can perform predictive analytics, i.e., forecast disease trajectories or large losses.

Today, in the era of AI, actuarial data science evolves towards prescriptive analytics and intelligent disaster management. Causal inference empowers this transition. It allows us to leverage modern AI algorithms to infer causal effects from observational data. While predictive models identify which factors are associated with loss, true risk management requires understanding the causal effect of an intervention: "If we implement this preventative measure, by how much will we actually reduce the expected loss?".

By identifying true causal drivers rather than mere symptoms, we move from passive risk measurement to active risk mitigation. We can then actively prevent losses before they occur or engage in intelligent disaster management, i.e., trigger interventions that act as true levers for long-term health and financial stability.  Furthermore, by isolating these causal effects, we can eliminate systemic biases and ensure that insurance pricing is not only statistically robust but ethically fair. This is our next step in ensuring a more stable and just society.

## Organisation
TODO: ToC and links to chapters

## Useful Links
### Theory
- [Oxford: Causal Assumptions](https://www.stats.ox.ac.uk/~evans/APTS/causassmp.html)
- [Tutorial on Causal Inference](https://bookdown.org/mike/data_analysis/sec-causal-inference.html)
- [Causal Assumptions](https://www.uniqcret.com/post/causal-inference-assumptions-guide)
- [QuantCo Blog Article: MetaLearners for CATE Estimation](https://tech.quantco.com/blog/metalearners)
- [Confounding Tutorial: Simpson's Paradoxon](https://www.biostatistics.ca/when-data-lies-simpsons-paradox-a-step-by-step-simulation-code-notebook/) 
- [Causality Handbook](https://matheusfacure.github.io/python-causality-handbook/02-Randomised-Experiments.html)

### Data Sets and Potential Use Cases
- [French Motor TPL Claims Data Set](https://www.kaggle.com/datasets/karansarpal/fremtpl2-french-motor-tpl-insurance-claims/data)
- [Medical Cost Data Set](https://www.kaggle.com/datasets/mirichoi0218/insurance)
- [CausalML: Interpretation of causal trees](https://causalml.readthedocs.io/en/stable/examples/causal_trees_interpretation.html)
- [Interpretation of causal forests](https://lorentzen.ch/index.php/2024/09/02/explaining-a-causal-forest/) (Waterfall Plot, SHAP Values)
- [Insurance Fraud Data Set](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/4954928053318020/1058911316420443/167703932442645/latest.html) Fraud 




