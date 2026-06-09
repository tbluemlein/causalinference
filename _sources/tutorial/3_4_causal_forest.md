# Causal Forests

(sec:cf)=
We additionally introduce causal forests that ensure a stronger degree of personalization in treatment effect estimation using adaptive nearest neighbourhood estimation. Similarly as for random forests {cite:p}`breimann2001rf`, the CATEs in this specific ensemble method of causal forests are estimated by a combination of the estimations of the weak learners, i.e. causal trees that are estimated $B$ times. In addition, principles such as random split selection and recursive binary splitting are the same here as for random forests {cite:p}`athey2018grf`. However, the CATEs are not calculated as simple averages over $B$ causal trees but by a weighted average over the local patient neighbourhood.

```{prf:algorithm} Causal Forest
:label: alg-causalforest
:class: dropdown

**Inputs** Covariates $X \in \mathcal{X}$, treatment $T \in \{0,1\}$, observed outcome $Y \in \mathcal{Y}$

**Outputs** Estimated CATE $\hat{\tau}(x)$

1. For every tree $b = 1, \ldots, B$:
	1. Split data into *construction* and *estimation* sets *(For honesty)*
	2. While partition of construction data is possible: *(Maximize heterogeneity)*

		1. Create partition into two subpopulations

	3. Determine leaves $\mathcal{L}$ based on estimation data *(Stopping criterion applies)*
	4. For every leaf $\ell \in \mathcal{L}$:

		1. Estimate the CATE $\hat{\tau}^{(\ell,b)}(x)$ on estimation data

	5. Return CATE $\hat{\tau}^{(\ell,b)}(x)$
2. Calculate weights $\alpha^{(i)}(x)$ *(Forest proximity weights)*
3. Calculate final CATE $\hat{\tau}(x)$ *(Weighted average)*
4. Return CATE $\hat{\tau}(x)$
```

Fitting $B$ causal trees, we repeat the separation step into a construction data set and an estimation data set repeatedly for every causal tree. Hence, every single weak learner is fitted on different subsamples of the observational data set. This ensures *honesty* in the ensemble setting as well, when the individual causal trees are composed to a causal forest. Every causal tree again recursively builds a partition into binary splits of the entire patient population based on the construction set. Then, it estimates the CATEs in the leaves $\ell^{(b)}$ based on the estimation set. After $B$ causal trees have been built, the weights required to compose the weighted average of CATEs are calculated for every observation as

\begin{equation}
    \alpha^{(j)}(x)=\frac{1}{B}\sum_{b=1}^{B}\frac{\mathbb{1}\{X^{(j)}\in\ell^{(b)}(x)\}}{\left|\ell^{(b)}(x)\right|}.
\end{equation}

The weights indicate how often another patient $j\not = i$ with covariates $X^{(j)}$ falls in the same leaf as the patient of interest $i$ with covariates $x$ across the trees in the forest. The more often the patients are in the same leaf, the closer they are to each other and the higher is the weight of patient when estimating the treatment effect of the observation with given covariates and outcome.

The causal forest is hence not used to construct the final estimate of CATE as average over all single estimations but rather for adaptive neighbourhood matching of each individual observation. The actual CATE is then calculated locally as a weighted average over its nearest neighbours, i.e. similar patients {cite:p}`athey2018grf`, as

\begin{equation}
    \hat{\tau}(x)=\frac{\sum_{j=1}^n \alpha^{(j)}(x)(Y^{(j)}-\hat{Y}^{(-j)})(T^{(j)}-\hat{\pi}^{(-j)}(x))}{ \sum \alpha^{(j)}(x)(T^{(j)}-\hat{\pi}^{(-j)}(x))^2}.
\end{equation}

To construct the neighbourhood for each single patient $i$, weights are calculated for every other patient $j\not = i$. Note that $\hat{Y}^{(-j)}$ and $\hat{\pi}^{(-j)}(x)$ are calculated out-of-bag, meaning that information about patient $j$ was not used for their estimation. We refer to {cite:t}`Athey.2018` for more details on the estimation procedure. To assign an observation to a leaf $\ell^{(b)}$ in iteration $b$, the set of covariates can vary across patients to determine the path, as causal forests share the property with random forests to randomly select the set of possible covariates at each split {cite:p}`breimann2001rf`. Amongst this set, the splitting covariate that maximizes heterogeneity in treatment effects amongst the subgroups, is chosen on a data-driven basis. This allows the path to vary per leaf $\ell$ and per iteration $b$.
