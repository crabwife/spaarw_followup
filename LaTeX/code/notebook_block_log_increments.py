grx_incs = (grw_logx[1:] - grw_logx[:-1]).ravel()
loc, scale = stats.laplace.fit(grx_incs)