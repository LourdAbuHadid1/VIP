def fit_linear(x, y):
    """
    x: list of X values (concentration, µg/mL)
    y: list of Y values (peak area)
    Returns (m, b, r2) for the model Y = m*X + b
    """

    n = len(x)

    # sum(x)
    sx = 0.0
    for xi in x:
        sx += float(xi)

    # sum(y)
    sy = 0.0
    for yi in y:
        sy += float(yi)

    # sum(x^2)
    sxx = 0.0
    for xi in x:
        sxx += float(xi) * float(xi)

    # sum(xy)
    sxy = 0.0
    for i in range(n):
        sxy += float(x[i]) * float(y[i])

    denom = n * sxx - sx * sx
    if denom == 0:
        raise ValueError("Need variation in X for a fit.")

    # slope and intercept
    m = (n * sxy - sx * sy) / denom
    b = (sy - m * sx) / n

    # calculate R²
    y_pred = [m*float(xi) + b for xi in x]
    y_mean = sy / n
    ss_tot = sum((float(yi) - y_mean)**2 for yi in y)
    ss_res = sum((float(yi) - ypi)**2 for yi, ypi in zip(y, y_pred))
    r2 = 1 - ss_res / ss_tot

    return m, b, r2
