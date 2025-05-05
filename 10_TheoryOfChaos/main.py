import numpy as np
import matplotlib.pyplot as plt


r_values = np.linspace(0, 4, 1000)
iterations = 1000
last = 100

x = 1e-5
x_list = []
r_list = []

for r in r_values:
    x = 0.5
    for i in range(iterations - last):
        x = r * x * (1 - x)
    for i in range(last):
        x = r * x * (1 - x)
        r_list.append(r)
        x_list.append(x)

plt.figure(figsize=(10, 6))
plt.plot(r_list, x_list, ',k', alpha=0.25)
plt.title("Bifurcation diagram")
plt.xlabel("Parameter r")
plt.ylabel("x")
plt.grid(True, linewidth=0.5, linestyle='dotted')
plt.tight_layout()
plt.show()
