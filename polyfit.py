import numpy as np
import matplotlib.pyplot as plt

# Adatsor

x = np.array(
    [
        368.5,
        310.0,
        241.25,
        176.5,
        103.25,
        389.5,
        315.75,
        247.75,
        189.0,
        126.25,
        367.5,
        296.75,
        237.75,
        170.75,
        114.0,
    ]
)

y = np.array(
    [
        -0.3955725783745615,
        -0.3800970759384862,
        -0.3655088448956039,
        -0.3499194214512725,
        -0.33078171332556816,
        -0.3992877046043505,
        -0.38544794058336646,
        -0.36568955871881187,
        -0.35380679836262874,
        -0.3384318289441144,
        -0.39718550762708543,
        -0.38138089206839026,
        -0.3666537502123128,
        -0.3504408483754513,
        -0.3364516655030855,
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
