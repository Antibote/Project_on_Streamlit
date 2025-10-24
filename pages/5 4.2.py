import streamlit as st
import numpy as np
from scipy.optimize import bisect, root
import matplotlib.pyplot as plt
st.page_link("./app.py", label="Вернуться на главную")
st.set_page_config(page_title="Метод Ньютона", layout="centered")

# Меню
page = st.sidebar.radio(
    "Выберите раздел:",
    ["Аналитическое решение", "Решение без SciPy", "Решение с SciPy (одномерное)", "Решение с SciPy (система)"]
)

# --- АНАЛИТИЧЕСКОЕ РЕШЕНИЕ ---
if page == "Аналитическое решение":
    st.title("Аналитическое решение задачи 4.2")

    st.markdown(r"""
    ### 4. Нелинейные уравнения и системы

    Напишите программу для нахождения решения системы нелинейных уравнений  
    \( F(x) = 0 \) методом Ньютона при **численном вычислении матрицы Якоби**.

    С её помощью найдите приближённое решение системы:

    $$
    \begin{cases}
    (3 + 2x_1)x_1 - 2x_2 = 3, \\
    (3 + 2x_i)x_i - x_{i-1} - 2x_{i+1} = 2, \quad i = 2, 3, \ldots, n-1, \\
    (3 + 2x_n)x_n - x_{n-1} = 4,
    \end{cases}
    $$

    и сравните его с **точным решением**

    $$
    x_i = 1, \quad i = 1, 2, \ldots, n.
    $$

    #### Теоретические сведения

    Метод Ньютона для решения системы \( F(x) = 0 \) задаётся итерационной формулой:

    $$
    x^{(k+1)} = x^{(k)} - J^{-1}(x^{(k)}) F(x^{(k)}),
    $$

    где \( J(x) \) — матрица Якоби функции \( F(x) \), элементы которой вычисляются численно по формуле конечных разностей:

    $$
    J_{ij}(x) \approx \frac{F_i(x + h e_j) - F_i(x)}{h}, \quad h \ll 1.
    $$

    Для данной системы численный расчёт проводится до достижения заданной точности
    \( \varepsilon = 10^{-10} \) или максимального числа итераций \( k = 1000 \).
    """)

    st.success("В этом разделе приведено аналитическое описание метода и постановка задачи.")


# --- РЕШЕНИЕ БЕЗ SCIPY ---
elif page == "Решение без SciPy":
    st.title("Решение системы методом Ньютона")

    def f(x):
        n = len(x)
        F = np.zeros(n)
        F[0] = (3 + 2 * x[0]) * x[0] - 2 * x[1] - 3
        for i in range(1, n - 1):
            F[i] = (3 + 2 * x[i]) * x[i] - x[i - 1] - 2 * x[i + 1] - 2
        F[n - 1] = (3 + 2 * x[n - 1]) * x[n - 1] - x[n - 2] - 4
        return F

    def Jacobi_matrix(x, h=1e-8):
        n = len(x)
        J = np.zeros((n, n))
        F_x = f(x)
        for i in range(n):
            x_h = x.copy()
            x_h[i] += h
            F_x_h = f(x_h)
            J[:, i] = (F_x_h - F_x) / h
        return J

    def Newton_method(x, eps, k):
        norms = []
        for i in range(k):
            F = f(x)
            norms.append(np.linalg.norm(F))
            if np.linalg.norm(F) < eps:
                return x, i + 1, norms
            J = Jacobi_matrix(x)
            try:
                dx = np.linalg.solve(J, -F)
            except np.linalg.LinAlgError:
                return None, i, norms
            x += dx
            if np.linalg.norm(dx) < eps:
                return x, i + 1, norms
        return None, k, norms

    n = st.number_input("Введите размерность системы (n):", min_value=2, max_value=20, value=4, step=1)
    n = st.slider("Введите размерность системы (n):", 2, 20, 4)
    if st.button("Решить"):
        x0 = np.zeros(n)
        x, iterations, norms = Newton_method(x0, eps=1e-10, k=1000)

        if x is not None:
            st.success(f"Сошлось за {iterations} итераций")
            st.write("**Приближённое решение:**", x)
            st.write(f"**Невязка:** {np.linalg.norm(f(x)):.2e}")
            exact = np.ones(n)
            st.write(f"**Погрешность относительно точного решения:** {np.linalg.norm(x - exact):.2e}")

            # Визуализация сходимости
            plt.figure(figsize=(6, 3))
            plt.semilogy(norms, marker='o')
            plt.title("Сходимость метода Ньютона")
            plt.xlabel("Итерация")
            plt.ylabel("‖F(x)‖")
            st.pyplot(plt)
        else:
            st.error("Метод не сошёлся")

# --- РЕШЕНИЕ С SCIPY (ОДНОМЕРНОЕ) ---
elif page == "Решение с SciPy (одномерное)":
    st.title("Решение с помощью SciPy (bisect)")
    st.markdown("Пример нахождения корня уравнения $f(x) = x^3 - 2x - 5$ методом бисекции.")

    def f(x):
        return x**3 - 2*x - 5

    a, b = -5, 5
    root_val = bisect(f, a, b)
    st.write(f"**Корень уравнения:** {root_val:.5f}")
    st.write(f"Проверка: f({root_val:.5f}) = {f(root_val):.2e}")

    x = np.linspace(-5, 5, 400)
    y = f(x)
    plt.figure(figsize=(6, 4))
    plt.axhline(0, color='gray', lw=1)
    plt.plot(x, y, label='f(x)')
    plt.scatter(root_val, f(root_val), color='red', zorder=5, label='Корень')
    plt.legend()
    st.pyplot(plt)

# --- РЕШЕНИЕ С SCIPY (СИСТЕМА) ---
elif page == "Решение с SciPy (система)":
    st.title("Решение системы с помощью SciPy (scipy.optimize.root)")

    def f(x):
        n = len(x)
        F = np.zeros(n)
        F[0] = (3 + 2 * x[0]) * x[0] - 2 * x[1] - 3
        for i in range(1, n - 1):
            F[i] = (3 + 2 * x[i]) * x[i] - x[i - 1] - 2 * x[i + 1] - 2
        F[n - 1] = (3 + 2 * x[n - 1]) * x[n - 1] - x[n - 2] - 4
        return F


    n = st.slider("Выберите значение:", 2, 15, 5)
    method_name = st.selectbox("Выберите метод SciPy:", ["Метод Пауэлла", "Метод Левенберга-Марквардта", "Метод Крылова"])
    if method_name == "Метод Пауэлла":
        method = "hybr"
    elif method_name == "Метод Левенберга-Марквардта":
        method = "lm"
    else:
        method = "krylov"
    if st.button("Решить систему"):
        #Начальное приближение
        x0 = np.zeros(n)
        sol = root(f, x0, method=method)
        if sol.success:
            st.success(f"Решение найдено ({method}) за {sol.nfev} вызовов функции")
            st.write("**Приближённое решение:**", sol.x)
            st.write(f"**Невязка:** {np.linalg.norm(sol.fun):.2e}")

            exact = np.ones(n)
            error = np.linalg.norm(sol.x - exact)
            st.write(f"**Погрешность относительно точного решения:** {error:.2e}")
        else:
            st.error(f"Не удалось найти решение: {sol.message}")
