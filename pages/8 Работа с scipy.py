import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, optimize, interpolate
st.page_link("./app.py", label="Вернуться на главную")
st.title("🧮 Работа с SciPy")

st.markdown("""
Библиотека **SciPy** используется для научных и инженерных расчётов.  
Ниже показаны примеры:
- численного интегрирования;
- нахождения корней уравнений;
- интерполяции данных.
""")

# --- Интегрирование ---
st.header("1️⃣ Численное интегрирование")

f = lambda x: np.sin(x) ** 2
res, err = integrate.quad(f, 0, np.pi)
st.write(f"∫ sin²(x) dx от 0 до π = {res:.4f} (погрешность ≈ {err:.1e})")

x = np.linspace(0, np.pi, 200)
y = f(x)
fig1, ax1 = plt.subplots()
ax1.plot(x, y, label="sin²(x)")
ax1.fill_between(x, y, alpha=0.3)
ax1.set_title("Интегрирование sin²(x)")
ax1.legend()
st.pyplot(fig1)

# --- Нахождение корня ---
st.header("2️⃣ Нахождение корня уравнения")

eq = lambda x: np.cos(x) - x
root = optimize.root_scalar(eq, bracket=[0, 1])
st.write(f"Решение уравнения cos(x) = x → x ≈ {root.root:.5f}")

x = np.linspace(0, 1, 100)
fig2, ax2 = plt.subplots()
ax2.plot(x, np.cos(x), label="cos(x)")
ax2.plot(x, x, label="y=x")
ax2.scatter(root.root, np.cos(root.root), color="red", zorder=5, label="корень")
ax2.legend()
ax2.set_title("Нахождение корня cos(x) = x")
st.pyplot(fig2)

# --- Интерполяция ---
st.header("3️⃣ Интерполяция данных")

x_data = np.linspace(0, 10, 8)
y_data = np.sin(x_data)
interp = interpolate.interp1d(x_data, y_data, kind='cubic')

x_new = np.linspace(0, 10, 200)
y_new = interp(x_new)

fig3, ax3 = plt.subplots()
ax3.plot(x_data, y_data, 'o', label="исходные точки")
ax3.plot(x_new, y_new, '-', label="кубическая интерполяция")
ax3.legend()
ax3.set_title("Интерполяция функции sin(x)")
st.pyplot(fig3)


