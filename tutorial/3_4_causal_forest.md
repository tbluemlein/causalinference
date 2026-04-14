# Causal Forests

(sec:cf)=
We additionally introduce causal forests that ensure a stronger degree of personalization in treatment effect estimation using adaptive nearest neighborhood estimation. Similarly as for random forests {cite:p}`breimann2001rf`, the CATEs in this specific ensemble method of causal forests is estimated by a combination of the estimations of the weak learners, i.e. causal trees that are estimated $B$ times. In addition, principles such as random split selection and recursive binary splitting are the same here as for random forests {cite:p}`athey2018grf`. However, the CATEs are not calculated as simple averages over $B$ causal trees but by a weighted average over the local patient neighborhood.

```{prf:algorithm} Causal Forest
:label: alg-causalforest
:class: dropdown

**Inputs** Patient history $\mathbf{H}_T \in \mathcal{H}_T$, observed final outcome $Y \in \mathcal{Y}_{T+1}$

**Outputs** Estimated CATE $\hat{\tau}(\mathbf{h}_t)$

1. For every tree $b = 1, \ldots, B$:
	1. Split data into *construction* and *estimation* sets *(For honesty)*
	2. While partition of construction data is possible: *(Maximize heterogeneity)*

		1. Create partition into two subpopulations

	3. Determine leaves $\mathcal{L}$ based on estimation data *(Stopping criterion applies)*
	4. For every leaf $\ell \in \mathcal{L}$:

		1. Estimate the CATE $\hat{\tau}^{(\ell,b)}(\mathbf{h}_t)$ on estimation data

	5. Return CATE $\hat{\tau}^{(\ell,b)}(\mathbf{h}_t)$
2. Calculate weights $\alpha^{(i)}(\mathbf{h}_t)$ *(Forest proximity weights)*
3. Calculate final CATE $\hat{\tau}(\mathbf{h}_t)$ *(Weighted average)*
4. Return CATE $\hat{\tau}(\mathbf{h}_t)$
```

Fitting $B$ causal trees, we repeat the separation step into a construction data set and an estimation data set repeatedly for every causal tree. Hence, every single weak learner is fitted on different subsamples of the observational data set. This ensures *honesty* in the ensemble setting as well, when the individual causal trees are composed to a causal forest. Every causal tree again recursively builds a partition into binary splits of the entire patient population based on the construction set. Then, it estimates the CATEs in the leaves $\ell^{(b)}$ based on the estimation set. After $B$ causal trees have been built, the weights required to compose the weighted average of CATEs are calculated for every observation as

\begin{equation}
    \alpha^{(j)}(\mathbf{h}_t)=\frac{1}{B}\sum_{b=1}^{B}\frac{\mathbb{1}\{\mathbf{H}_t^{(j)}\in\ell^{(b)}(\mathbf{h}_t)\}}{\left|\ell^{(b)}(\mathbf{h}_t)\right|}.
\end{equation}

The weights indicate how often another patient $j\not = i$ with history $\mathbf{H}^{(j)}_t$ falls in the same leaf as the patient of interest $i$ with the history $\mathbf{h}_t$ across the trees in the forest. The more often the patients are in the same leaf, the closer they are to each other and the higher is the weight of patient when estimating the treatment effect of the observation with a given patient history and outcome.

The causal forest is hence not used to construct the final estimate of CATE as average over all single estimations but rather for adaptive neighborhood matching of each individual observation. The actual CATE is then calculated locally as a weighted average over its nearest neighbors, i.e. similar patients {cite:p}`athey2018grf`, as

\begin{equation}
    \hat{\tau}(\mathbf{h}_t)=\frac{\sum_{j=1}^n \alpha^{(j)}(\mathbf{h}_t)(Y^{(j)}-\hat{Y}^{(-j)})(A_t^{(j)}-\hat{\pi}^{(-j)}(\mathbf{h}_t))}{ \sum \alpha^{(j)}(\mathbf{h}_t)(A_t^{(j)}-\hat{\pi}^{(-j)}(\mathbf{h}_t))^2}.
\end{equation}

To construct the neighborhood for each single patient $i$, weights are calculated for every other patient $j\not = i$. Note that $\hat{Y}^{(-j)}$ and $\hat{\pi}^{(-j)}(\mathbf{h}_t)$ are calculated out-of-bag, meaning that information about patient $j$ was not used for their estimation. We refer to {cite:t}`Athey.2018` for more details on the estimation procedure. To assign an observation to a leaf $\ell^{(b)}$ in iteration $b$, the set of covariates can vary across patients to determine the path, as causal forests share the property with random forests to randomly select the set of possible covariates at each split {cite:p}`breimann2001rf`. Amongst this set, the splitting covariate that maximizes heterogeneity in treatment effects amongst the subgroups, is chosen on a data-driven basis. This allows the path to vary per leaf $\ell$ and per iteration $b$.
