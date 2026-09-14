import numpy as np, scipy, scipy.signal, sys
x = np.linspace(0, 1, 500); y = 4.2 - 0.8 * x ** 1.3 + 0.01 * np.sin(40 * x)
np.save(sys.argv[1], scipy.signal.savgol_filter(y, 11, 3))
