import numpy as np
import matplotlib.pyplot as plt

# Adatsor

x = np.array(
    [441.75, 250.5, 424.25, 247.5, 345.25, 424.0, 257.25, 422.0, 243.5, 384.75, 300.75]
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
        -0.44055750816159434,
        -0.39115881572604416,
        -0.4418448730010383,
        -0.3964713728404311,
        -0.4206100263398404,
        -0.4433895088716759,
        -0.39307441045003183,
        -0.4395014504183946,
        -0.38551982472716734,
        -0.4331231192913692,
        -0.4098904773250945,
    ]
)

# Elsőfokú polinomiális illeszkedés (lineáris illeszkedés)
degree = 1
coefficients = np.polyfit(x, y, degree)

# Az egyenes egyenlete
m = coefficients[0]  # meredekség
b = coefficients[1]  # y tengely metszéspont

# Az egyenes egyenlete
equation = f"y = {m:.2f}x + {b:.2f}"
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
