# Causal Inference Tutorial: Brainstorming
## Useful Links
### Theory
- [Oxford: Causal Assumptions](https://www.stats.ox.ac.uk/~evans/APTS/causassmp.html)
- [Tutorial on Causal Inference](https://bookdown.org/mike/data_analysis/sec-causal-inference.html)
- [Causal Assumptions](https://www.uniqcret.com/post/causal-inference-assumptions-guide)
- [QuantCo Blog Article: MetaLearners for CATE Estimation](https://tech.quantco.com/blog/metalearners)
- [Confounding Tutorial: Simpson's Paradoxon](https://www.biostatistics.ca/when-data-lies-simpsons-paradox-a-step-by-step-simulation-code-notebook/) 

### Data Sets and Potential Use Cases
- [French Motor TPL Claims Data Set](https://www.kaggle.com/datasets/karansarpal/fremtpl2-french-motor-tpl-insurance-claims/data)
- [Medical Cost Data Set](https://www.kaggle.com/datasets/mirichoi0218/insurance)
- [CausalML: Interpretation of causal trees](https://causalml.readthedocs.io/en/stable/examples/causal_trees_interpretation.html)
- [Interpretation of causal forests](https://lorentzen.ch/index.php/2024/09/02/explaining-a-causal-forest/) (Waterfall Plot, SHAP Values)
- [Insurance Fraud Data Set](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/4954928053318020/1058911316420443/167703932442645/latest.html) Fraud 

## Actuarial Use Cases
- Pricing: Estimate how product features (e.g., deductibles, limits, telematics devices) cause changes in claim cost or behavior; introduce discrimination measures to tackle fairness (in insurance pricing)
- Underwriting: Identify which risk factors drive losses, not just correlate
- Claims management: Quantify impact of interventions (e.g., early triage, litigation management, driver training) using causal forests for HTE estimation
- Reserving: Assess causal drivers of development patterns (e.g., policy changes, inflation)
- Customer Management: Predict lapse probability: Test whether retention campaigns cause persistency improvements

### Methodology and Practical Applicability
| **Objective**           | **Causal Question**                                  | **Outcome**                                    |
| ----------------------- | ---------------------------------------------------- | ---------------------------------------------- |
| Loss ratio optimization | “Does a $500 deductible reduce expected loss costs?” | Quantified causal reduction (%)                |
| Behavioral response     | “Do customers churn more when deductible increases?” | Estimate causal churn elasticity               |
| Segmentation            | “Which customers tolerate higher deductibles?”       | Personalized pricing & product design          |
| Policy simulation       | “What if all customers had $250 more deductible?”    | Counterfactual simulation for pricing strategy |


### Approaches
| **Approach**                         | **What It Does**                                                                                                               | **When to Use It**                                | **Libraries / Tools**       |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------- | --------------------------- |
| **Propensity Score Matching (PSM)**  | Match policyholders with similar risk profiles, differing only in deductible presence                                          | Non-random assignment of deductibles              | `causalml`, `DoWhy`         |
| **Difference-in-Differences (DiD)**  | Compare before/after introduction of deductibles between affected and unaffected groups                                        | Deductibles introduced at a specific time         | `statsmodels`, `EconML`     |
| **Instrumental Variables (IV)**      | Use an external “instrument” (e.g., regional rule, agent behavior) that influences deductibles but not claim outcomes directly | When unobserved confounders exist                 | `linearmodels`, `econml.iv` |
| **Causal Forests / Uplift Modeling** | Estimate heterogeneous treatment effects — how different segments respond to deductible introduction                           | You want to know *for whom* deductibles work best | `EconML`, `grf`, `causalml` |
| **Regression Discontinuity (RD)**    | Exploit a deductible rule threshold (e.g., cutoff by vehicle value)                                                            | Deductible changes apply near a boundary          | `rdd`, `DoWhy`              |

## References
https://matheusfacure.github.io/python-causality-handbook/02-Randomised-Experiments.html


