# SPAARW follow-up

A reproducible comparison of random-walk, autoregressive, hurdle, and self-exciting models of scientific productivity.

This repository contains my follow-up to [*Scientific Productivity as a Random Walk*](https://arxiv.org/abs/2309.04414). I reproduce the data preparation used by Zhang et al., rebuild their principal random-walk benchmarks, and then test the stochastic architecture more aggressively than the original paper did.

The central question is not whether scientific-productivity trajectories are noisy. They plainly are. The question is whether current productivity is a sufficient state from which to generate the future.

In this dataset, it is not.

The repository therefore proceeds from arithmetic and geometric random walks, through fitted autoregressive and hurdle models, to **SE-Hurdle-S**, a scholar-agnostic self-exciting hurdle model with an explicitly decaying memory of prior productivity.

## What this repository does

The pipeline:

1. imports and prepares the adjusted-productivity data used by Zhang et al.;
2. fits a common set of stochastic benchmark models;
3. generates simulated 21-year productivity trajectories;
4. evaluates every architecture against the same empirical diagnostics; and
5. tests whether productivity history contains information that is absent from current productivity alone.

I do not treat agreement with one marginal distribution as evidence that a model has recovered the underlying process. Models are compared jointly on annual productivity, increments, inactivity, cumulative productivity, rank mobility, temporal dependence, and career-level distributions.

## Data

The canonical input is:

```text
import/input/adjusted_productivity.csv
```

It is derived from the data pipeline in the original [`faculty-trajectories`](https://github.com/samzhang111/faculty-trajectories) repository.

I follow the original study’s main sample restrictions:

* at least three cumulative adjusted publications by career age 5;
* PhD year of 1980 or later;
* at most 21 observed career years; and
* complete zero-indexed trajectories from career year 0 through 20 where a full panel is required.

Annual adjusted productivity is denoted by (q_t). Log-space models use

[
\log(q_t + 0.49),
]

which permits zero-productivity years without silently dropping them.

Most stagewise models use the career stages

[
{0},\qquad {1,\ldots,4},\qquad
{5,\ldots,7},\qquad
{8,\ldots,20}.
]

ARW4 retains its original stage specification for direct comparison with the source model.

## Models

### Reproduced baselines

* **ARW4** — a reimplementation of the most developed arithmetic random walk in the original project. Productivity is drawn from a nonnegative truncated Laplace distribution whose mode depends on current productivity.
* **Unfitted-GRW** — the illustrative geometric random walk from the original work, initialized at (q_0=4) with normally distributed multiplicative log shocks.

### Fitted random-walk and autoregressive benchmarks

* **GRW-G** — a geometric random walk with globally fitted log-increment parameters.
* **GRW-Y** — a geometric random walk with yearwise fitted log-increment parameters.
* **AR(1)-GRW-Y** — a first-order log-space autoregression fitted separately by transition year.
* **AR(1)-GRW-S** — the same architecture fitted over the four canonical career stages.
* **AR(1)-GRW-S-G** — the retained stagewise AR(1) comparison with global initialization.

### Hurdle models

The hurdle architectures separate two distinct quantities:

1. the **extensive margin**, or whether a scholar publishes at all; and
2. the **intensive margin**, or how much the scholar publishes conditional on publishing.

The benchmark hurdle models are:

* **Hurdle-AR(1)-GRW-S** — stagewise activity transitions followed by a positive-productivity AR(1);
* **Hurdle-AR(1)-GRW-S-P** — adds productivity-dependent dropout; and
* **Hurdle-AR(3)-GRW-S-P** — extends the positive-productivity equation to three lags, using lower-order warm-up dynamics after a restart.

These models substantially improve the treatment of zero years, but they remain finite-order Markov architectures.

### SE-Hurdle-S

SE-Hurdle-S replaces a fixed collection of recent lags with a normalized, exponentially decaying summary of earlier productivity:

[
H_t =
\frac{
\displaystyle\sum_{k=0}^{t-2}
\rho^{,t-2-k}\log(1+q_k)
}{
\displaystyle\sum_{k=0}^{t-2}
\rho^{,t-2-k}
}.
]

The immediately preceding productivity (q_{t-1}) remains an explicit predictor. (H_t) therefore measures information in the earlier trajectory rather than counting the current state twice.

Within each career stage, SE-Hurdle-S estimates:

* a logistic activity equation for whether (q_t>0); and
* a conditional positive-productivity equation for (\log q_t).

Both equations may depend on current productivity, activity or restart status, and decayed productivity history. The history coefficients are constrained to be nonnegative in the final self-exciting specification. All parameters are shared across scholars within a stage; there are no scholar-specific latent effects.

The memory-decay parameter (\rho) is selected by cross-validated predictive likelihood rather than set by hand.

## Current empirical result

The retained results support three related conclusions.

First, the empirical process fails a discretized Chapman–Kolmogorov check for first-order Markov sufficiency. The observed two-step discrepancy is approximately (0.128), compared with a Markov-null 95% upper bound of approximately (0.062), with permutation (p\approx0.001).

Second, adding productivity history improves out-of-sample prediction at every tested horizon. Across one-, two-, and five-year forecasts, history reduces mean absolute error by approximately 5.6–8.9% for log productivity and percentile rank. The corresponding rank-correlation gains are also consistently positive.

Third, the self-exciting model recovers temporal rank persistence that is nearly absent from the stagewise Hurdle-AR(1) benchmark:

| Quantity                                | Empirical | Hurdle-AR(1)-S | SE-Hurdle-S |
| --------------------------------------- | --------: | -------------: | ----------: |
| Terminal rank persistence               |     0.202 |          0.003 |       0.198 |
| Rank-persistence curve RMSE             |         — |          0.268 |       0.039 |
| Cross-validated negative log likelihood |         — |          1.353 |       1.082 |

The selected decay is currently

[
\hat\rho = 0.6664,
]

corresponding to a memory half-life of approximately 1.71 years.

These are empirical model-comparison results, not causal identification of a unique mechanism. The narrower conclusion is that current annual productivity is an inadequate state representation for these trajectories, and that a simple decayed-history statistic repairs several failures of the first-order models at once.

## Diagnostics

The repository evaluates models using:

* annual mean, median, variance, and zero fraction;
* raw- and log-productivity moment trajectories;
* raw- and log-increment trajectories;
* pooled and stagewise Laplace fits;
* exponential-power fits to raw increments;
* cumulative-productivity lognormal Q–Q plots;
* first-year productivity and canonical mean trajectories;
* year-of-maximum-productivity distributions;
* cumulative productivity by career year 5;
* distributions of zero years and run lengths;
* conditional dropout and restart behavior;
* rank persistence, rank displacement, and decile mixing;
* top-(k) persistence and pairwise rank inversions;
* Chapman–Kolmogorov tests;
* flexible nearest-neighbor Markov simulations;
* cross-validated predictive gains from history; and
* bootstrap intervals for the fitted history coefficients.

The point of this collection is to expose architectures that reproduce one conspicuous feature while failing elsewhere.

## Repository structure

Each main task follows an `input/src/output` layout.

```text
import/
    Import the adjusted-productivity data and reproduce the
    original sample restrictions.

prepare/
    Construct the modeling panel, stage labels, transformed
    variables, and empirical summaries.

fit/
    Estimate parameters for the random-walk, autoregressive,
    and hurdle benchmark models.

simulate/
    Generate reproducible 21-year trajectories and save model
    metadata, parameter tables, and annual summaries.

plot/
    Run the common benchmark diagnostics and produce comparative
    figures and result tables.

self_exciting/
    Fit and simulate SE-Hurdle-S, test Markov sufficiency, and run
    the history-specific validation suite.
```

The compact tracked self-exciting notebook is:

```text
self_exciting/src/SE_Hurdle_S_notebook.ipynb
```

The larger working notebook is intentionally excluded from version control. Selected figures and result tables from the complete analysis are retained under:

```text
self_exciting/output/
```

Likewise, `plot/output/` contains the retained common-model diagnostics, including both paper-facing and exploratory figures.

## Reproduction

The notebooks were developed under Python 3.13. They use:

```text
numpy
pandas
scipy
matplotlib
seaborn
scikit-learn
jupyter
```

A minimal installation is:

```bash
python -m pip install numpy pandas scipy matplotlib seaborn scikit-learn jupyter
```

This is research code rather than a packaged Python library. There is currently no environment lockfile or single command that executes the entire project.

Run the benchmark pipeline in this order:

```text
1. import/src/import.ipynb
2. prepare/src/prepare.ipynb
3. fit/src/fit.ipynb
4. simulate/src/simulate.ipynb
5. plot/src/01_autoregressive_parameters.ipynb
6. plot/src/02_qq_plots.ipynb
7. plot/src/03_laplace.ipynb
8. plot/src/04_count_trajectories.ipynb
9. plot/src/05_delta_trajectories.ipynb
10. plot/src/06_zhang_remaining_rank_mixing_selected.ipynb
```

Then run:

```text
self_exciting/src/SE_Hurdle_S_notebook.ipynb
```

SE-Hurdle-S requires the prepared trajectory panel but does not require the benchmark simulations.

The notebooks use paths relative to their task directories. Run each notebook with its corresponding `src/` directory as the working directory, and make sure the preceding task’s outputs are available under the next task’s `input/`.

Simulations use fixed seeds and currently generate 10,000 trajectories per benchmark model. Large fitted and simulated intermediates are generally excluded from version control; selected final figures and compact result tables are retained.

## Scope

This repository is not an argument that one stochastic model fully explains scientific careers. It is an attempt to identify which pieces of temporal structure are required before a generative model can reproduce the data without relying on scholar-specific parameters.

The main result is a departure from a memoryless random-walk account, not a departure from stochastic explanation. Scientific productivity remains highly variable and usefully modeled as a stochastic process, but the process carries history.
