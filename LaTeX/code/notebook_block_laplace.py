T, N = 21, 10000          # time steps, number of walks
mu, sigma = 0, 0.5        # drift, volatility of log-growth
x0 = 4.0                    # initial level

eps = np.random.laplace(loc=mu, scale=sigma, size=(T, N))
grw_logx = np.log(x0) + np.cumsum((mu - 0.5*sigma**2) + eps, axis=0)
grw_x = np.exp(grw_logx)            # x[t, i] is level of walk i at time t