SPAARW2 plotting notebooks — ten-model version

Added models
------------
grw_global
    GRW-G: one globally estimated log-increment distribution.

ar1_s_globalinit
    AR(1)-GRW-S-G: globally fitted initialization with stagewise AR(1)
    dynamics.

Expected upstream links
-----------------------
From SPAARW2/plot/input:

    ln -sfn ../../prepare/output prepare
    ln -sfn ../../simulate/output simulate

The simulation output must contain trajectories.npy for all desired models.
The autoregressive notebook additionally reads copied parameter tables from
simulate/output/<model>/parameters/.

Outputs
-------
Figures:
    SPAARW2/plot/output/figures/

CSV summaries:
    SPAARW2/plot/output/results/

Notes
-----
The hurdle diagnostics remain restricted to the three hurdle models.
The Zhang histogram and representative-trajectory grids expand dynamically
to accommodate the empirical panel plus all ten simulated models.
