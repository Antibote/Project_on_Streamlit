import streamlit as st
import math
import numpy as np
from scipy.optimize import bisect
import matplotlib.pyplot as plt

st.page_link("./app.py", label="Вернуться на главную")
st.set_page_config(page_title="Метод бисекции", layout="centered")

page = st.sidebar.radio(
    "Выберите раздел:",
    ["Аналитическое решение", "Решение без scipy", "Решение с SciPy"]
)

# АНАЛИТИЧЕСКОЕ РЕШЕНИЕ

if page == "Аналитическое решение":
    # контейнер стабилизирует вывод
    with st.container():
        st.title("Аналитическое решение уравнения методом бисекции")
        st.markdown("Найти корень уравнения на интервале $[0,10]$:")

        # единый LaTeX-блок вместо множества вызовов st.latex
        st.markdown(
            r"""
            $$
            f(x) = (1 + x^{2})e^{-x} + \sin(x) = 0
            $$
            """
        )

        st.header("1. Проверка знаков на концах интервала")
        x0, x1 = 0, 10

        def f(x):
            return (1 + x**2) * math.exp(-x) + math.sin(x)

        f0, f1 = f(x0), f(x1)

        st.markdown(
            r"""
            Рассчитаем значения функции в концах:
            $$
            f(0) = (1 + 0^2)e^{0} + \sin(0) = 1 > 0
            $$
            $$
            f(10) = (1 + 10^2)e^{-10} + \sin(10) \approx 0.00045 - 0.545 \approx -0.5445 < 0
            $$
            Следовательно, по теореме о промежуточных значениях существует хотя бы один корень на $[0,10]$.
            """
        )

        st.header("2. Метод бисекции — идея и производная")
        st.markdown(
            r"""
            Для анализа поведения функции полезно знать производную:
            $$
            f'(x) = 2x e^{-x} - (1+x^2)e^{-x} + \cos x
            = -e^{-x}(x-1)^2 + \cos x.
            $$
            """
        )

        # Для краткости — выводим заранее известный результат:
        st.markdown("Найденный корень (примерно):")
        st.markdown(
        r"""
        $$
        x \approx 3.5443
        $$
        """)



# РЕШЕНИЕ БЕЗ SCIPY

elif page == "Решение без scipy":
    import matplotlib.pyplot as plt

    st.title("Решение уравнения без использования SciPy")
    st.markdown("Реализация метода бисекции с автоматическим поиском интервалов смены знака и визуализацией.")

    # --- Определение функций ---
    def f(x):
        return (1 + x**2) * math.exp(-x) + math.sin(x)

    def bisection(f, a, b, eps=1e-8, max_iter=1000):
        """Метод бисекций с логом итераций"""
        if f(a) * f(b) > 0:
            return None, []
        steps = []
        for i in range(max_iter):
            c = (a + b) / 2
            fc = f(c)
            steps.append((i + 1, a, b, c, fc))
            if abs(fc) < eps or (b - a) < eps:
                return c, steps
            if f(a) * fc < 0:
                b = c
            else:
                a = c
        return (a + b) / 2, steps

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

    # --- Ввод параметров пользователем ---
    st.header("1. Настройка параметров поиска")
    step = st.slider("Шаг для поиска интервалов:", 0.01, 1.0, 0.1, 0.01)
    eps = st.number_input("Точность ε:", value=1e-8, format="%.1e")

    # --- Поиск интервалов ---
    st.header("2. Поиск интервалов смены знака")
    intervals = find_sign_changes(f, 0, 10, step)

    if not intervals:
        st.error("Интервалы смены знака не найдены.")
    else:
        st.write(f"Найдено интервалов: {len(intervals)}")
        intervals_text = "\n".join(
            [f"- Интервал {i+1}: [{a:.2f}, {b:.2f}] — f(a)={f(a):.3f}, f(b)={f(b):.3f}"
             for i, (a, b) in enumerate(intervals)]
        )
        st.markdown(intervals_text)

        # --- Поиск корней ---
        st.header("3. Поиск корней методом бисекции")
        roots = []
        for a, b in intervals:
            root, steps = bisection(f, a, b, eps)
            if root is not None:
                roots.append((root, steps))
                st.success(f"Корень ≈ {root:.4f}, f(x) = {f(root):.2e}")

                st.expander(f"Показать ход вычислений для [{a:.2f}, {b:.2f}]").dataframe(
                    {
                        "Итерация": [s[0] for s in steps],
                        "a": [round(s[1], 6) for s in steps],
                        "b": [round(s[2], 6) for s in steps],
                        "c": [round(s[3], 6) for s in steps],
                        "f(c)": [round(s[4], 8) for s in steps],
                    }
                )

        if roots:
            st.markdown("**Найденные корни:** " + ", ".join([f"{r[0]:.6f}" for r in roots]))

            # --- График функции и корней ---
            st.header("4. Визуализация")
            x_vals = np.linspace(0, 10, 1000)
            y_vals = [(1 + x**2) * np.exp(-x) + np.sin(x) for x in x_vals]

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(x_vals, y_vals, label="f(x)")
            ax.axhline(0, color="black", linestyle="--", linewidth=1)
            for r, _ in roots:
                ax.plot(r, f(r), "ro", label=f"x ≈ {r:.3f}")
            ax.set_title("График функции и найденные корни")
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
        else:
            st.warning("Корни не найдены на выбранном интервале.")


# РЕШЕНИЕ С SCIPY

elif page == "Решение с SciPy":
    st.title("Решение с использованием SciPy")
    st.markdown("""
    Здесь используется готовая функция `bisect` из `scipy.optimize`,  
    которая реализует тот же метод бисекций, но с оптимизацией и проверками.
    """)

    def f(x):
        return (1 + x**2) * np.exp(-x) + np.sin(x)

    # --- Поиск корней ---
    x_values = np.linspace(0, 10, 1000)
    roots = []

    for i in range(len(x_values) - 1):
        a, b = x_values[i], x_values[i + 1]
        if f(a) * f(b) < 0:
            root = bisect(f, a, b)
            if not roots or abs(root - roots[-1]) > 1e-4:
                roots.append(root)

    # --- Вывод результатов ---
    if roots:
        st.success(f"Найдено корней: {len(roots)}")
        for r in roots:
            st.write(f"x = {r:.6f}, f(x) = {f(r):.2e}")
    else:
        st.error("Корни на интервале [0, 10] не найдены.")

    # --- Построение графика ---
    st.header("График функции f(x) и найденные корни")

    y_values = f(x_values)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_values, y_values, label=r"$f(x) = (1+x^2)e^{-x} + \sin(x)$", linewidth=2)
    ax.axhline(0, color='black', linewidth=1, linestyle='--')

    if roots:
        ax.scatter(roots, [f(r) for r in roots], color='red', s=60, label="Найденные корни")

    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("График функции и найденные корни (SciPy)")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
