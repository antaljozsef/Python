import numpy as np
import matplotlib.pyplot as plt

# Adatsor

x = np.array(
    [
        188.0,
        244.75,
        289.5,
        364.5,
        417.0,
        201.25,
        259.0,
        312.25,
        368.0,
        409.0,
        183.75,
        234.25,
        282.75,
        338.75,
        374.0,
    ]
)

"""y = np.array(
    [
        -440.56,
        -391.16,
        -441.84,
        -396.47,
        -420.61,
        -443.39,
        -393.08,
        -439.51,
        -385.54,
        -433.11,
        -409.89,
    ]
)"""

y = np.array(
    [
        -0.366641395,
        -0.352046278,
        -0.333293443,
        -0.319577714,
        -0.301942004,
        -0.370464731,
        -0.353256546,
        -0.336103572,
        -0.315962823,
        -0.303312669,
        -0.371691739,
        -0.349471146,
        -0.335670331,
        -0.319407919,
        -0.307463068,
    ]
)

# Elsőfokú polinomiális illeszkedés (lineáris illeszkedés)
degree = 1
coefficients = np.polyfit(x, y, degree)

# Az egyenes egyenlete
m = coefficients[0]  # meredekség
b = coefficients[1]  # y tengely metszéspont

# Az egyenes egyenlete
equation = f"y = {m:.16f}x + {b:.16f}"
print(equation)

# Illesztett polinom
p = np.poly1d(coefficients)

# Illesztett értékek számítása
x_fit = np.linspace(min(x), max(x), 100)
y_fit = p(x_fit)

# Adatok ábrázolása és illesztett polinom ábrázolása
plt.scatter(x, y, label="Adatok", color="blue")
plt.plot(x_fit, y_fit, label="Illesztett polinom", color="red")
plt.xlabel("X Arucco")
plt.ylabel("X Robot")
plt.legend()
plt.grid(True)
plt.title("Polinomiális illeszkedés")
plt.show()
