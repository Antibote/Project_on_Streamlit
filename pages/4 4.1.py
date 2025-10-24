import streamlit as st
import math
import numpy as np
from scipy.optimize import bisect

st.page_link("./app.py", label="Вернуться на главную")
st.set_page_config(page_title="Метод бисекции", layout="centered")

page = st.sidebar.radio(
    "Выберите раздел:",
    ["Аналитическое решение", "Решение без scipy", "Решение с SciPy"]
)

# АНАЛИТИЧЕСКОЕ РЕШЕНИЕ

if page == "Аналитическое решение":
    st.title("Аналитическое решение уравнения методом бисекции")
    st.markdown("Найти корень уравнения:")

    st.latex(r"f(x) = (1 + x^{2})e^{-x} + \sin(x) = 0")

    st.markdown("на интервале [0; 10].")

    # Определение функции
    def f(x):
        return (1 + x**2) * math.exp(-x) + math.sin(x)

    # --- Проверка знаков ---
    st.header("1 Проверка знаков на концах интервала")

    x0, x1 = 0, 10
    f0, f1 = f(x0), f(x1)

    st.latex(r"f(0) = (1 + 0^2)e^0 + \sin(0) = 1 > 0")
    st.latex(r"f(10) = (1 + 10^2)e^{-10} + \sin(10) \approx 0.00045 - 0.545 = -0.5445 < 0")

    st.markdown("""
    Следовательно, \( f(0) > 0 \) и \( f(10) < 0 \),  
    по теореме о промежуточных значениях уравнение имеет хотя бы один корень на [0; 10].
    """)

    # --- Метод бисекции ---
    st.header("2 Метод бисекции")

    st.markdown("Ищем количество корней и точки смены знака.")
    st.latex(r"f'(x) = 2xe^{-x} - (1+x^2)e^{-x} + \cos(x) = (-x^2 + 2x - 1)e^{-x} + \cos(x)")
    st.latex(r"= -e^{-x}(x - 1)^2 + \cos(x)")

    a, b = 0, 10
    eps = 0.001
    iteration = 0
    steps = []

    while (b - a) / 2 > eps:
        c = (a + b) / 2
        iteration += 1
        fc = f(c)
        steps.append((iteration, a, b, c, fc))
        if fc == 0:
            break
        elif f(a) * fc < 0:
            b = c
        else:
            a = c

    root = (a + b) / 2

    st.markdown(f"""
    После {iteration} итераций методом бисекции получаем:  
    Корень примерно равен {root:.4f}
    """)

    st.header("3 Ход вычислений")

    st.dataframe(
        {
            "Итерация": [s[0] for s in steps],
            "a": [round(s[1], 4) for s in steps],
            "b": [round(s[2], 4) for s in steps],
            "c": [round(s[3], 4) for s in steps],
            "f(c)": [round(s[4], 6) for s in steps],
        }
    )

    st.success(f"Найденный корень: x ≈ {root:.4f}")
    st.caption("Задача решена методом бисекции по аналитическим выкладкам.")

# ---------------------------------------------------------------------
# РЕШЕНИЕ БЕЗ SCIPY
# ---------------------------------------------------------------------
elif page == "Решение без scipy":
    st.title("Решение уравнения без использования scipy")
    st.markdown("Реализация метода бисекции с автоматическим поиском интервалов смены знака.")

    # --- Определение функций ---
    def f(x):
        """Функция уравнения: (1+x^2)e^(-x) + sin(x)"""
        return (1 + x**2) * math.exp(-x) + math.sin(x)

    def bisection(f, a, b, eps=1e-8, max_iter=1000):
        """Метод бисекций"""
        if f(a) * f(b) > 0:
            return None
        for i in range(max_iter):
            c = (a + b) / 2
            if abs(f(c)) < eps or (b - a) < eps:
                return c
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
        return (a + b) / 2

    def find_sign_changes(f, start, end, step=0.1):
        """Автоматически находит интервалы смены знака функции"""
        intervals = []
        x_prev = start
        f_prev = f(x_prev)
        x = x_prev + step
        while x <= end:
            f_current = f(x)
            if f_prev * f_current <= 0:
                intervals.append((x_prev, x))
            x_prev = x
            f_prev = f_current
            x += step
        return intervals

    # --- Основная программа ---
    st.header("1 Поиск интервалов смены знака")

    intervals = find_sign_changes(f, 0, 10, 0.1)
    if not intervals:
        st.error("Интервалы смены знака не найдены.")
    else:
        st.write("Найдены интервалы:")
        for i, (a, b) in enumerate(intervals):
            st.write(f"Интервал {i+1}: [{a:.2f}, {b:.2f}] — f(a)={f(a):.3f}, f(b)={f(b):.3f}")

        st.header("2 Поиск корней методом бисекции")

        roots = []
        for a, b in intervals:
            root = bisection(f, a, b)
            if root is not None:
                roots.append(root)
                st.write(f"Корень ≈ {root:.8f}, f(x) = {f(root):.2e}")

        st.success(f"Найдено корней на интервале [0, 10]: {len(roots)}")
        if roots:
            st.markdown(
                "Корни: " + ", ".join([f"{r:.5f}" for r in roots])
            )


# ---------------------------------------------------------------------
# РЕШЕНИЕ С SCIPY
# ---------------------------------------------------------------------
elif page == "Решение с SciPy":
    st.title("Решение с использованием SciPy")
    st.markdown("""
    Здесь используется готовая функция `bisect` из `scipy.optimize`,  
    которая реализует тот же метод бисекций, но с оптимизацией и проверками.
    """)

    def f(x):
        return (1 + x**2) * np.exp(-x) + np.sin(x)

    x_values = np.linspace(0, 10, 1000)
    roots = []

    for i in range(len(x_values) - 1):
        a, b = x_values[i], x_values[i + 1]
        if f(a) * f(b) < 0:
            root = bisect(f, a, b)
            if not roots or abs(root - roots[-1]) > 1e-4:
                roots.append(root)

    if roots:
        st.success(f"Найдено корней: {len(roots)}")
        for r in roots:
            st.write(f"x = {r:.6f}, f(x) = {f(r):.2e}")
    else:
        st.error("Корни на интервале [0, 10] не найдены.")