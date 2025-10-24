import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, signal

# --- Навигация ---
st.page_link("./app.py", label="⬅ Вернуться на главную")

# --- Заголовок ---
st.title("Научная графика")

st.markdown("""
Эта страница демонстрирует построение научных графиков с использованием **NumPy**, **SciPy** и **Matplotlib**.
""")

# --- 1. График функции ---
st.header("Построение функции sin(x) и её производной")

x = np.linspace(0, 2 * np.pi, 400)
y = np.sin(x)
dy = np.cos(x)  # производная sin(x)

fig1, ax1 = plt.subplots()
ax1.plot(x, y, label="sin(x)")
ax1.plot(x, dy, '--', label="cos(x) — производная")
ax1.set_xlabel("x")
ax1.set_ylabel("Значение функции")
ax1.set_title("Функция sin(x) и её производная")
ax1.legend()
st.pyplot(fig1)

# --- 2. Интегрирование ---
st.header("Интегрирование функции sin²(x)")

f = lambda x: np.sin(x) ** 2
integral, error = integrate.quad(f, 0, np.pi)
st.write(f"∫ sin²(x) dx от 0 до x = {integral:.4f} (погрешность ≈ {error:.1e})")

x_vals = np.linspace(0, np.pi, 200)
y_vals = f(x_vals)
fig2, ax2 = plt.subplots()
ax2.plot(x_vals, y_vals, color="tab:orange", label="sin²(x)")
ax2.fill_between(x_vals, y_vals, alpha=0.3)
ax2.set_title("Интегрирование функции sin²(x)")
ax2.legend()
st.pyplot(fig2)

# --- 3. Пример обработки сигнала ---
st.header("Фильтрация сигнала")

# создаем зашумленный сигнал
t = np.linspace(0, 1, 500)
signal_clean = np.sin(2 * np.pi * 5 * t)
noise = 0.3 * np.random.randn(500)
signal_noisy = signal_clean + noise

# применяем фильтр (низкочастотный)
b, a = signal.butter(4, 0.1)
signal_filtered = signal.filtfilt(b, a, signal_noisy)

fig3, ax3 = plt.subplots()
ax3.plot(t, signal_noisy, label="Шумный сигнал", alpha=0.9)
ax3.plot(t, signal_filtered, label="Отфильтрованный сигнал", linewidth=2)
ax3.set_xlabel("Время (с)")
ax3.set_ylabel("Амплитуда")
ax3.set_title("Фильтрация сигнала с помощью SciPy")
ax3.legend()
st.pyplot(fig3)

