grw_x[0] = x0

for t in range(20):
    grw_x[t + 1] = grw_x[t] * gamma[t]