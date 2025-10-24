import streamlit as st
st.page_link("./app.py", label="Вернуться на главную")
st.title("Компоновка страницы")

st.markdown("""
Streamlit позволяет легко размещать элементы **в колонках и вкладках**.
""")

# Колонки
st.subheader("Колонки")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Температура", "23°C", "+1°C")
with col2:
    st.metric("Влажность", "45%", "-2%")
with col3:
    st.metric("Давление", "760 мм рт. ст.", "+5")

# Вкладки
st.subheader("Вкладки")
tab1, tab2 = st.tabs(["График", "Таблица"])

with tab1:
    st.line_chart({"y": [1, 3, 2, 4, 3, 5]})
with tab2:
    st.table({"A": [1, 2, 3], "B": [4, 5, 6]})


