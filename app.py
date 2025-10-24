import streamlit as st

st.set_page_config(page_title="Streamlit Demo", page_icon="📘", layout="wide")

st.title("📘 Демонстрация возможностей Streamlit")

st.markdown("""
## Добро пожаловать! 👋

Это интерактивное приложение демонстрирует основные возможности **Streamlit** —  
от простого вывода текста до построения сложных научных визуализаций и численных расчётов с **SciPy**.
""")

st.info("Используйте левое меню (sidebar) или ссылки ниже для перехода к разделам.")

st.divider()
st.header("🗂 Оглавление")

cols = st.columns(2)

with cols[0]:
    st.page_link("pages/1 Работа с текстом.py", label="Работа с текстом")
    st.page_link("pages/2 Элементы графического интерфейса.py", label="Элементы интерфейса")
    st.page_link("pages/3 Компоновка страницы.py", label="Компоновка страницы")
    st.page_link("pages/4 4.1.py", label="Задание 4.1")

with cols[1]:
    st.page_link("pages/5 4.2.py", label="Задание 4.2")
    st.page_link("pages/6 Работа с таблицами.py", label="Работа с таблицами")
    st.page_link("pages/7 Работа с научной графикой.py", label="Научная графика")
    st.page_link("pages/8 Работа с scipy.py", label="Работа с SciPy")

st.divider()
st.caption("Разработано в демонстрационных целях для изучения Streamlit и Python-библиотек.")

st.success("Можно делать такие штуки, как сообщения об успехе")
st.info("Реализовано информационное сообщение. Пусть тут будет упоминание работы с сайд-баром")
