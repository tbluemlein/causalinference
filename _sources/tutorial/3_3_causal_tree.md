# Causal Trees

(sec:ct)=
Our first approach to infer heterogeneous treatment effects is based on causal trees. In contrast to modelling the effect of the treatment on the potential outcome effect linearly, we rely on the idea of {cite:t}`athey2016recursive`. {prf:ref}`alg-causaltree` shows their procedure according to which a causal tree estimates heterogeneous treatment effects from patient history $\mathbf{H}_T$ and an observed final outcome $Y$.

```{prf:algorithm} Causal Tree
:label: alg-causaltree
:class: dropdown

**Inputs** Patient history $\mathbf{H}_T \in \mathcal{H}_T$, observed final outcome $Y \in \mathcal{Y}_{T+1}$

**Outputs** Estimated CATE $\hat{\tau}^{(\ell)}(\mathbf{h}_t)$

1. Subsample data and split into *construction* and *estimation* sets *(Honesty)*
2. While partition of construction data is still possible: *(Stopping criterion applies)*
	1. Create partition into two subpopulations maximizing heterogeneity
3. Map estimation data into determined tree leaves $\mathcal{L}$
4. For every leaf $\ell \in \mathcal{L}$:
	1. Estimate local CATE $\hat{\tau}^{(\ell)}(\mathbf{h}_t)$ using estimation data
5. Return CATE $\hat{\tau}^{(\ell)}(\mathbf{h}_t)$
```

Similar to CART {cite:p}`Breimann1984cart`, a causal tree partitions the sample into subgroups. It creates a partition of the patient population into subpopulations (i.e., leaves $\ell\in\mathcal{L}$) using recursive binary splitting. In contrast to a decision tree, a causal tree estimates the treatment effect $\hat{\tau}$ directly by modelling the contrast in potential outcomes rather than modelling both potential outcomes and then taking their contrast. Since a covariate that affects the expected outcome $\mathbb{E}[Y\mid\mathbf{H}_t=\mathbf{h}_t]$ does not necessarily affect the treatment effect and vice versa, the splitting criterion is chosen with respect to covariates that actually cause treatment effect heterogeneity, as explained below.

For each split, the outcome-covariate pair is determined such that it maximizes the weighted difference $n_L\cdot n_R\cdot (\hat{\tau}_L-\hat{\tau}_R)^2$ where $n_L$ denotes the number of observations assigned to the left node and $n_R$ the number of observations that are assigned to right node. The first two factors, $n_L$ and $n_R$ make sure that the two sides are well balanced and the squared difference makes sure that the treatment effects between the two subpopulations are as heterogeneous as possible. A constant, hence homogeneous, treatment effect is assumed across all observations within the respective subpopulation aggregated in a leaf. We denote $\mathbb{E}[Y^{(-i)}\mid\mathbf{H}_t=\mathbf{h}_t])=\hat{Y}^{(-i)}$:

\begin{align}
     \hat{\tau}_L\leftarrow lm\left((Y^{(i)}-\hat{Y}^{(-i)})\sim(A_t^{(i)}-\hat{\pi}^{(-i)}(\mathbf{h}_t^{(i)})):\mathbf{h}_t^{(i)}\in L\right) \\
     \hat{\tau}_R\leftarrow  lm\left((Y^{(i)}-\hat{Y}^{(-i)})\sim(A_t^{(i)}-\hat{\pi}^{(-i)}(\mathbf{h}_t^{(i)})):\mathbf{h}_t^{(i)}\in R\right)
\end{align}

The stopping criterion of further partitioning the population into subgroups is usually pre-specified by hyperparameters such as the minimum number of observations per leaf, a threshold for the weighted difference in the resulting treatment effects or a difference in sizes between the resulting nodes in terms of control and treatment group. If one of these minimum requirements is not met due to an additional split, the partitioning process is stopped and the algorithm intermediately returns the partition of $\mathcal{L}$. Given this partition, the estimation step is executed to get CATEs that basically are differences in outcomes for treatment and control observations. In every leaf $\ell$, there are both treated and untreated patients. Hence, the CATE is estimated as

\begin{equation}
    \hat{\tau}^{(\ell)}(\mathbf{h})=\frac{\sum_{\{i:A=0,\mathbf{h}\in \ell\}}Y^{(i)}}{\left|\{i:A=0,\mathbf{h}\in \ell\}\right|}-\frac{\sum_{\{i:A=1,\mathbf{h}\in \ell\}}Y^{(i)}}{\left|\{i:A=1,\mathbf{h}\in \ell\}\right|}
\end{equation}

The underlying assumptions are that in each leaf, the treatment effect is the same across all observations in the leaf and the leaves are small enough that the $(Y,A_t)$ pairs of each observation in a leaf behave as they have come from a RCT: This requires that $A_t$ is randomly distributed across the observations in the leaf based on the patient history and the outcome $Y$ is independent of the assigned treatment $A_t$.

To ensure unbiased estimates of CATEs, the principle of *honesty* is introduced for causal trees and causal forests {cite:p}`athey2016recursive`. A method is called honest if the entire sample of patients is split into two parts, one for tree construction and one to estimate the treatment effects within the leaves. Hence, model selection is decoupled from model estimation. This addresses the post-selection inference problem and ensures unbiased estimates of CATEs.

The method is regarded doubly robust since we apply inverse propensity score weighting at every step $t$: We combine the outcome model and propensity score model to reduce the sensitivity to misspecifications. Even if only one of the two is well specified, the resulting CATE estimator is more robust. This is necessary in presence of observational data, where the treatment is not assigned randomly.

With a causal tree, we estimate heterogeneous treatment effects, differentiating by subgroups. We additionally introduce causal forests that ensure a stronger degree of personalization in treatment effect estimation using adaptive nearest neighborhood estimation.
