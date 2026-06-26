PDP-structured repo for followup to Scientific Productivity as a Random Walk (https://arxiv.org/pdf/2309.04414).<br />
<br />
I import and prepare data exactly as done by Zhang et al per their repo at https://github.com/samzhang111/faculty-trajectories<br />
<br />
I fit and simulate seven models:<br />
  <br />
  <br />
  ARW4, an exact copy of Zhang et al's most developed arithmetic random walk, a truncated Laplace model<br />
  <br />
  GRW, an exact copy of Zhang et al's illustrative unfitted geometric random walk with shocks ɣ ~ N(0,1/4), x_0 = 4<br />
  <br />
  GRW-Y, my first foray into fitted GRWs, a lognormal random walk with yearwise-fitted normal parameters<br />
  <br />
  AR(1)-GRW-Y, a first-order autoregressive model with yearwise refitting of σ², a, and β<br />
  <br />
  AR(1)-GRW-S, a first-order autoregressive model with stagewise refitting of σ², a, and β, following the stages [0], [1-4], [5-7], [8-20] and directly scientifically comparable to ARW4<br />
  <br />
  Hurdle-AR(1)-S, a version of AR(1)-GRW-S in which both intensive and extensive margins are modeled seperately, with a Bernoullian hurdle for publishing/not publishing coming before computation of quantity<br />
  <br />
  Hurdle-AR(1)-S-P, a version of Hurdle-AR(1)-S in which the probability of dropout is dependent on the previous years' productivity, that is, Pr(bₜ₊₁ = 0 | bₜ = 0, qₜ)<br />
  <br />
  <br />
After fitting and simulation, I run diagnostics and plot several of them, including:<br />
  <br />
  <br />
  Trajectories of mean, median, and variance of real-count and log-space productivity and delta-productivity<br />
  <br />
  Rank-mixing<br />
  <br />
  Laplace fits<br />
  <br />
  Autoregressive parameter trends<br />
  <br />
  Lognormal cumulative QQs<br />
  <br />
  CDFs<br />
  <br />
  <br />
These diagnostics are drawn from SPAARW and the unpublished follow-up to SPAARW<br />
<br />
My findings are available as a slide deck and a formal report in the project root<br />
<br />
This repo is dependent on Python 3.13<br />
<br />
It can be run in its entirety with no extra dependencies<br />
