log_gamma_emp = np.log(df_traj_all.pubs_adj_next) - np.log(df_traj_all.pubs_adj)
log_gamma_emp = log_gamma_emp[np.isfinite(log_gamma_emp)]
loc, scale = laplace.fit(log_gamma_emp)